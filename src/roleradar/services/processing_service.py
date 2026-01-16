"""Processing service for analyzing search results and updating database."""

from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
from sqlalchemy import desc
from ..models import Company, Opportunity, HiringSignal, SearchResult
from ..models.graph import GraphDatabase
from ..database import db_service
from .tavily_service import TavilySearchService
from .groq_service import GroqAnalysisService


class ProcessingService:
    """Service for processing search results and updating database."""
    
    def __init__(self):
        """Initialize processing service."""
        self.tavily = TavilySearchService()
        self.groq = GroqAnalysisService()
        self.graph = GraphDatabase()
    
    def process_unprocessed_results(self, limit: int = 20):
        """Process unprocessed search results."""
        results = self.tavily.get_unprocessed_results(limit=limit)
        
        print(f"Processing {len(results)} unprocessed results...")
        
        for result in results:
            try:
                self._process_single_result(result)
                self.tavily.mark_as_processed(result.id)
            except Exception as e:
                print(f"Error processing result {result.id}: {e}")
    
    def _process_single_result(self, result: SearchResult):
        """Process a single search result."""
        # Combine title and content for analysis
        text = f"{result.title}\n{result.content}"
        
        # Extract entities
        entities = self.groq.extract_entities(text)
        
        company_name = entities.get("company_name")
        if not company_name:
            print(f"No company found in result {result.id}")
            return
        
        # Get or create company
        with db_service.get_session() as session:
            company = session.query(Company).filter_by(name=company_name).first()
            
            if not company:
                company = Company(
                    name=company_name,
                    industry=entities.get("industry"),
                    location=entities.get("location"),
                    description=result.content[:500] if result.content else None
                )
                session.add(company)
                session.flush()
                
                # Add to graph database
                self.graph.add_company(company.id, name=company_name)
            
            # Check if this is a job posting
            job_title = entities.get("job_title")
            if job_title:
                # Check if an active opportunity with this title already exists
                existing_opp = session.query(Opportunity).filter_by(
                    company_id=company.id,
                    title=job_title,
                    is_active=True
                ).first()
                
                if not existing_opp:
                    opportunity = Opportunity(
                        company_id=company.id,
                        title=job_title,
                        role_type=entities.get("role_type"),
                        description=result.content,
                        url=result.url,
                        location=entities.get("location"),
                        is_active=True,
                        discovered_date=datetime.now(timezone.utc)
                    )
                    session.add(opportunity)
                    session.flush()
                    
                    # Add to graph database
                    self.graph.add_opportunity(
                        opportunity.id,
                        company.id,
                        title=job_title,
                        role_type=entities.get("role_type")
                    )
            
            # Detect hiring signals
            signals = self.groq.detect_hiring_signals(text, company_name)
            
            if signals.get("has_signal") and signals.get("confidence", 0) > 0.5:
                # Check if signal already exists for this company, type, and source URL
                existing_signal = session.query(HiringSignal).filter_by(
                    company_id=company.id,
                    signal_type=signals.get("signal_type"),
                    source_url=result.url
                ).first()
                
                if not existing_signal:
                    signal = HiringSignal(
                        company_id=company.id,
                        signal_type=signals.get("signal_type"),
                        description=signals.get("description"),
                        source_url=result.url,
                        confidence=signals.get("confidence", 0.0),
                        detected_date=datetime.now(timezone.utc)
                    )
                    session.add(signal)
                    session.flush()
                    
                    # Add to graph database
                    self.graph.add_signal(
                        signal.id,
                        company.id,
                        signals.get("signal_type"),
                        description=signals.get("description")
                    )
            
            # Update company score
            self._update_company_score(session, company.id)
    
    def _update_company_score(self, session, company_id: int):
        """Update company score based on opportunities and signals."""
        company = session.query(Company).get(company_id)
        if not company:
            return
        
        # Count active opportunities
        active_opps = session.query(Opportunity).filter_by(
            company_id=company_id,
            is_active=True
        ).count()
        
        # Get recent signals
        recent_signals = session.query(HiringSignal).filter_by(
            company_id=company_id
        ).filter(
            HiringSignal.detected_date > datetime.now(timezone.utc) - timedelta(days=90)
        ).all()
        
        # Prepare data for scoring
        company_data = {
            "active_opportunities": active_opps,
            "signals": [
                {
                    "confidence": s.confidence,
                    "type": s.signal_type
                }
                for s in recent_signals
            ],
            "has_funding": any(s.signal_type == "funding" for s in recent_signals),
            "has_expansion": any(s.signal_type == "expansion" for s in recent_signals),
            "recent_activity": len(recent_signals) > 0
        }
        
        # Calculate score
        company.score = self.groq.score_company(company_data)
        company.last_updated = datetime.now(timezone.utc)
    
    def get_top_companies(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get top companies by score."""
        with db_service.get_session() as session:
            companies = session.query(Company).order_by(
                desc(Company.score)
            ).limit(limit).all()
            
            result = []
            for company in companies:
                result.append({
                    "id": company.id,
                    "name": company.name,
                    "score": company.score,
                    "location": company.location,
                    "active_opportunities": len([o for o in company.opportunities if o.is_active]),
                    "signals_count": len(company.signals)
                })
            
            return result
    
    def get_active_opportunities(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get active job opportunities."""
        with db_service.get_session() as session:
            opportunities = session.query(Opportunity).filter_by(
                is_active=True
            ).order_by(
                desc(Opportunity.discovered_date)
            ).limit(limit).all()
            
            result = []
            for opp in opportunities:
                result.append({
                    "id": opp.id,
                    "title": opp.title,
                    "company_name": opp.company.name if opp.company else "Unknown",
                    "company_score": opp.company.score if opp.company else 0,
                    "role_type": opp.role_type,
                    "location": opp.location,
                    "url": opp.url,
                    "discovered_date": opp.discovered_date.isoformat() if opp.discovered_date else None
                })
            
            return result
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get summary data for dashboard."""
        with db_service.get_session() as session:
            total_companies = session.query(Company).count()
            total_opportunities = session.query(Opportunity).filter_by(is_active=True).count()
            total_signals = session.query(HiringSignal).filter(
                HiringSignal.detected_date > datetime.now(timezone.utc) - timedelta(days=90)
            ).count()
            
            top_companies = self.get_top_companies(limit=10)
            recent_opportunities = self.get_active_opportunities(limit=10)
            
            # Get summary from Groq
            summary_text = self.groq.summarize_results(top_companies, max_results=10)
            
            return {
                "total_companies": total_companies,
                "total_opportunities": total_opportunities,
                "total_signals": total_signals,
                "top_companies": top_companies,
                "recent_opportunities": recent_opportunities,
                "summary": summary_text,
                "last_updated": datetime.now(timezone.utc).isoformat()
            }
