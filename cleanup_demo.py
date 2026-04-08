#!/usr/bin/env python3
"""Clean up demo data from the database."""

from src.roleradar.database import db_service
from src.roleradar.models import Company, Opportunity, HiringSignal, SearchResult

def cleanup_demo_data():
    """Remove all companies and related data."""
    with db_service.get_session() as session:
        # Count before deletion
        company_count = session.query(Company).count()
        opportunity_count = session.query(Opportunity).count()
        signal_count = session.query(HiringSignal).count()
        result_count = session.query(SearchResult).count()
        
        print(f"Removing demo data...")
        print(f"  Companies: {company_count}")
        print(f"  Opportunities: {opportunity_count}")
        print(f"  Hiring Signals: {signal_count}")
        print(f"  Search Results: {result_count}")
        
        # Delete in order of dependencies
        session.query(HiringSignal).delete()
        session.query(Opportunity).delete()
        session.query(SearchResult).delete()
        session.query(Company).delete()
        
        session.commit()
        print("\n✓ Demo data removed successfully!")
        print("  Ready for real Tavily searches")

if __name__ == "__main__":
    cleanup_demo_data()
