#!/usr/bin/env python3
"""Demo script to populate RoleRadar with sample data."""

from datetime import datetime, timedelta
from src.roleradar.database import db_service
from src.roleradar.models import Company, Opportunity, HiringSignal
from src.roleradar.models.graph import GraphDatabase


def populate_demo_data():
    """Populate database with demo data."""
    print("Populating RoleRadar with demo data...\n")
    
    # Initialize database
    db_service.create_tables()
    
    # Create graph database
    graph = GraphDatabase()
    
    # Sample companies
    companies_data = [
        {
            "name": "TechCorp Security",
            "domain": "techcorpsec.com",
            "industry": "Cybersecurity",
            "size": "500-1000",
            "location": "San Francisco, CA",
            "description": "Leading cybersecurity provider with enterprise solutions",
            "score": 85.0
        },
        {
            "name": "CloudGuard Systems",
            "domain": "cloudguard.io",
            "industry": "Cloud Security",
            "size": "100-500",
            "location": "Austin, TX",
            "description": "Cloud-native security platform for modern enterprises",
            "score": 78.5
        },
        {
            "name": "ComplianceFirst Inc",
            "domain": "compliancefirst.com",
            "industry": "RegTech",
            "size": "50-100",
            "location": "New York, NY",
            "description": "Compliance automation for financial services",
            "score": 72.0
        },
        {
            "name": "DataProtect Solutions",
            "domain": "dataprotect.com",
            "industry": "Data Security",
            "size": "200-500",
            "location": "Seattle, WA",
            "description": "Data protection and privacy solutions",
            "score": 68.0
        },
        {
            "name": "RiskManage Pro",
            "domain": "riskmanagepro.com",
            "industry": "GRC",
            "size": "100-200",
            "location": "Chicago, IL",
            "description": "Enterprise risk management platform",
            "score": 65.5
        }
    ]
    
    # Sample opportunities
    opportunities_data = [
        {
            "company": "TechCorp Security",
            "title": "Chief Information Security Officer (CISO)",
            "role_type": "security",
            "description": "Lead security strategy for Fortune 500 clients",
            "location": "San Francisco, CA",
            "url": "https://example.com/jobs/ciso"
        },
        {
            "company": "TechCorp Security",
            "title": "Security Compliance Manager",
            "role_type": "compliance",
            "description": "Manage SOC2, ISO27001 compliance programs",
            "location": "Remote",
            "url": "https://example.com/jobs/compliance-mgr"
        },
        {
            "company": "CloudGuard Systems",
            "title": "Senior Security Engineer",
            "role_type": "security",
            "description": "Build cloud security infrastructure",
            "location": "Austin, TX",
            "url": "https://example.com/jobs/sec-eng"
        },
        {
            "company": "ComplianceFirst Inc",
            "title": "GRC Analyst",
            "role_type": "GRC",
            "description": "Support GRC program for fintech clients",
            "location": "New York, NY",
            "url": "https://example.com/jobs/grc-analyst"
        },
        {
            "company": "DataProtect Solutions",
            "title": "Data Protection Officer",
            "role_type": "compliance",
            "description": "Lead GDPR and data privacy initiatives",
            "location": "Seattle, WA",
            "url": "https://example.com/jobs/dpo"
        },
        {
            "company": "CloudGuard Systems",
            "title": "Compliance Director",
            "role_type": "compliance",
            "description": "Build compliance program from ground up",
            "location": "Remote",
            "url": "https://example.com/jobs/compliance-dir"
        }
    ]
    
    # Sample hiring signals
    signals_data = [
        {
            "company": "TechCorp Security",
            "signal_type": "funding",
            "description": "Raised $50M Series C to expand security services",
            "confidence": 0.9
        },
        {
            "company": "TechCorp Security",
            "signal_type": "expansion",
            "description": "Opening new office in London, expanding team by 40%",
            "confidence": 0.85
        },
        {
            "company": "CloudGuard Systems",
            "signal_type": "funding",
            "description": "Secured $25M Series B from top VCs",
            "confidence": 0.88
        },
        {
            "company": "CloudGuard Systems",
            "signal_type": "product_launch",
            "description": "Launching new AI-powered threat detection platform",
            "confidence": 0.82
        },
        {
            "company": "ComplianceFirst Inc",
            "signal_type": "regulatory",
            "description": "New regulations creating demand for compliance tools",
            "confidence": 0.75
        },
        {
            "company": "DataProtect Solutions",
            "signal_type": "breach",
            "description": "Recent data breaches in industry driving demand",
            "confidence": 0.7
        }
    ]
    
    with db_service.get_session() as session:
        # Add companies
        company_map = {}
        for comp_data in companies_data:
            company = Company(**comp_data)
            session.add(company)
            session.flush()
            company_map[comp_data["name"]] = company
            graph.add_company(company.id, name=company.name)
            print(f"✓ Added company: {company.name}")
        
        # Add opportunities
        for opp_data in opportunities_data:
            company = company_map[opp_data["company"]]
            opportunity = Opportunity(
                company_id=company.id,
                title=opp_data["title"],
                role_type=opp_data["role_type"],
                description=opp_data["description"],
                location=opp_data["location"],
                url=opp_data["url"],
                is_active=True,
                posted_date=datetime.utcnow() - timedelta(days=5),
                discovered_date=datetime.utcnow() - timedelta(days=2)
            )
            session.add(opportunity)
            session.flush()
            graph.add_opportunity(opportunity.id, company.id, title=opportunity.title)
            print(f"  ✓ Added opportunity: {opportunity.title} at {company.name}")
        
        # Add signals
        for signal_data in signals_data:
            company = company_map[signal_data["company"]]
            signal = HiringSignal(
                company_id=company.id,
                signal_type=signal_data["signal_type"],
                description=signal_data["description"],
                confidence=signal_data["confidence"],
                source_url="https://example.com/news",
                detected_date=datetime.utcnow() - timedelta(days=3)
            )
            session.add(signal)
            session.flush()
            graph.add_signal(signal.id, company.id, signal.signal_type)
            print(f"  ✓ Added signal: {signal_data['signal_type']} for {company.name}")
    
    print("\n" + "="*60)
    print("Demo data populated successfully!")
    print("="*60)
    print("\nRun 'python roleradar.py dashboard' to view the results")
    print("or 'python roleradar.py stats' to see statistics")


if __name__ == "__main__":
    populate_demo_data()
