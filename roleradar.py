#!/usr/bin/env python3
"""Main CLI application for RoleRadar."""

import argparse
import sys
from src.roleradar.database import db_service
from src.roleradar.services import TavilySearchService, ProcessingService
from src.roleradar.dashboard import create_app
from src.roleradar.config import config


def init_database():
    """Initialize database tables."""
    print("Initializing database...")
    db_service.create_tables()
    print("Database initialized successfully!")


def run_search():
    """Run daily search for opportunities."""
    print("Running daily search...")
    
    try:
        tavily = TavilySearchService()
        results = tavily.daily_search()
        
        total_results = sum(len(r) for r in results.values())
        print(f"\nSearch completed! Found {total_results} results across {len(results)} queries.")
        
        for query, query_results in results.items():
            print(f"  - {query}: {len(query_results)} results")
        
        print("\nProcessing results...")
        processor = ProcessingService()
        processor.process_unprocessed_results(limit=100)
        print("Processing completed!")
        
    except Exception as e:
        print(f"Error during search: {e}")
        sys.exit(1)


def run_processing():
    """Process unprocessed search results."""
    print("Processing unprocessed results...")
    
    try:
        processor = ProcessingService()
        processor.process_unprocessed_results(limit=100)
        print("Processing completed!")
    except Exception as e:
        print(f"Error during processing: {e}")
        sys.exit(1)


def run_dashboard():
    """Run the web dashboard."""
    print(f"Starting dashboard on http://{config.FLASK_HOST}:{config.FLASK_PORT}")
    app = create_app()
    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=False
    )


def show_stats():
    """Show statistics about the database."""
    from src.roleradar.models import Company, Opportunity, HiringSignal
    
    print("\n=== RoleRadar Statistics ===\n")
    
    with db_service.get_session() as session:
        total_companies = session.query(Company).count()
        total_opps = session.query(Opportunity).filter_by(is_active=True).count()
        total_signals = session.query(HiringSignal).count()
        
        print(f"Companies tracked: {total_companies}")
        print(f"Active opportunities: {total_opps}")
        print(f"Hiring signals: {total_signals}")
        
        if total_companies > 0:
            print("\nTop 5 Companies by Score:")
            top_companies = session.query(Company).order_by(
                Company.score.desc()
            ).limit(5).all()
            
            for i, company in enumerate(top_companies, 1):
                print(f"  {i}. {company.name}: {company.score:.1f}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="RoleRadar - Security & Compliance Opportunity Tracker"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Init command
    subparsers.add_parser('init', help='Initialize database')
    
    # Search command
    subparsers.add_parser('search', help='Run daily search for opportunities')
    
    # Process command
    subparsers.add_parser('process', help='Process unprocessed search results')
    
    # Dashboard command
    subparsers.add_parser('dashboard', help='Run web dashboard')
    
    # Stats command
    subparsers.add_parser('stats', help='Show database statistics')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'init':
        init_database()
    elif args.command == 'search':
        run_search()
    elif args.command == 'process':
        run_processing()
    elif args.command == 'dashboard':
        run_dashboard()
    elif args.command == 'stats':
        show_stats()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
