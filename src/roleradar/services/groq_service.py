"""Groq service for entity extraction, scoring, and analysis."""

import json
from typing import Dict, Any, List
from groq import Groq
from ..config import config


class GroqAnalysisService:
    """Service for analyzing search results using Groq API."""
    
    def __init__(self, api_key=None):
        """Initialize Groq analysis service."""
        self.api_key = api_key or config.GROQ_API_KEY
        if not self.api_key:
            print("Warning: Groq API key not configured. Analysis functionality will be limited.")
            self.client = None
        else:
            self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.1-70b-versatile"
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """
        Extract entities from text including companies, job titles, and locations.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with extracted entities
        """
        if not self.client:
            print("Warning: Groq client not initialized. Returning empty entities.")
            return {
                "company_name": None,
                "job_title": None,
                "role_type": None,
                "location": None,
                "keywords": []
            }
        
        prompt = f"""Analyze the following text and extract structured information about job opportunities in security, compliance, or GRC roles.

Extract:
- company_name: Name of the company (if mentioned)
- job_title: Job title or role
- role_type: Classify as "security", "compliance", or "GRC"
- location: Job location
- keywords: List of relevant keywords (e.g., "CISO", "data protection", "risk management")

Text: {text}

Return ONLY a valid JSON object with these fields. If a field is not found, use null.
"""
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that extracts structured data from job postings and returns valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.1,
                max_tokens=500
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Try to extract JSON from the response
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            entities = json.loads(result_text)
            return entities
            
        except Exception as e:
            print(f"Error extracting entities: {e}")
            return {
                "company_name": None,
                "job_title": None,
                "role_type": None,
                "location": None,
                "keywords": []
            }
    
    def detect_hiring_signals(self, text: str, company_name: str) -> Dict[str, Any]:
        """
        Detect hiring signals from text about a company.
        
        Args:
            text: Text to analyze
            company_name: Name of the company
            
        Returns:
            Dictionary with hiring signals
        """
        if not self.client:
            return {
                "has_signal": False,
                "signal_type": "none",
                "confidence": 0.0,
                "description": ""
            }
        
        prompt = f"""Analyze the following text about {company_name} and identify hiring signals that suggest they may need security or compliance leadership.

Look for signals like:
- Company expansion or growth
- Recent funding rounds
- Security breaches or incidents
- New compliance requirements
- Regulatory changes affecting the company
- Product launches requiring security expertise

Text: {text}

Return ONLY a valid JSON object with:
- has_signal: boolean indicating if hiring signals were detected
- signal_type: one of ["expansion", "funding", "breach", "compliance_news", "regulatory", "product_launch", "none"]
- confidence: float between 0 and 1
- description: brief description of the signal

Return valid JSON only.
"""
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that analyzes company news for hiring signals and returns valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.2,
                max_tokens=300
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Try to extract JSON from the response
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            signals = json.loads(result_text)
            return signals
            
        except Exception as e:
            print(f"Error detecting hiring signals: {e}")
            return {
                "has_signal": False,
                "signal_type": "none",
                "confidence": 0.0,
                "description": ""
            }
    
    def score_company(self, company_data: Dict[str, Any]) -> float:
        """
        Score a company based on job postings and hiring signals.
        
        Args:
            company_data: Dictionary with company information including opportunities and signals
            
        Returns:
            Score between 0 and 100
        """
        score = 0.0
        weights = config.SCORING_WEIGHTS
        
        # Explicit job postings (weight: 0.4)
        num_active_jobs = company_data.get("active_opportunities", 0)
        if num_active_jobs > 0:
            score += min(num_active_jobs * 10, 40) * weights["explicit_job_posting"]
        
        # Hiring signals (weight: 0.3)
        signals = company_data.get("signals", [])
        if signals:
            avg_confidence = sum(s.get("confidence", 0) for s in signals) / len(signals)
            score += avg_confidence * 100 * weights["hiring_signals"]
        
        # Company growth indicators (weight: 0.2)
        if company_data.get("has_funding", False) or company_data.get("has_expansion", False):
            score += 50 * weights["company_growth"]
        
        # Recent activity (weight: 0.1)
        if company_data.get("recent_activity", False):
            score += 100 * weights["recent_activity"]
        
        return min(score, 100.0)
    
    def summarize_results(self, results: List[Dict[str, Any]], max_results: int = 10) -> str:
        """
        Summarize search results into a readable format.
        
        Args:
            results: List of search results with companies and opportunities
            max_results: Maximum number of results to include
            
        Returns:
            Formatted summary text
        """
        if not results:
            return "No results to summarize."
        
        if not self.client:
            return f"Found {len(results)} companies with opportunities. Configure Groq API key for detailed summaries."
        
        # Prepare summary data
        summary_items = []
        for result in results[:max_results]:
            # Support both formats: 'name' or 'company_name', 'active_opportunities' or 'opportunity_count'
            company_name = result.get('company_name') or result.get('name', 'Unknown')
            opp_count = result.get('opportunity_count') or result.get('active_opportunities', 0)
            score = result.get('score', 0)
            summary_items.append(f"- {company_name}: {opp_count} opportunities, score: {score:.1f}")
        
        summary_text = "\n".join(summary_items)
        
        prompt = f"""Create a brief executive summary of the following security, compliance, and GRC opportunities:

{summary_text}

Provide a 2-3 sentence summary highlighting:
1. The total number of opportunities found
2. Top companies or trends
3. Key insights for job seekers in security/compliance roles

Keep it concise and actionable.
"""
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that creates concise executive summaries."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.3,
                max_tokens=200
            )
            
            summary = response.choices[0].message.content.strip()
            return summary
            
        except Exception as e:
            print(f"Error creating summary: {e}")
            return f"Found {len(results)} companies with opportunities."
