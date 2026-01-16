#!/usr/bin/env python3
"""Scheduler for running daily searches automatically."""

import schedule
import time
from datetime import datetime
from src.roleradar.services import TavilySearchService, ProcessingService
from src.roleradar.database import db_service


def run_daily_job():
    """Run the daily search and processing job."""
    print(f"\n{'='*60}")
    print(f"Starting daily job at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    try:
        # Initialize database if needed
        db_service.create_tables()
        
        # Run search
        print("Running searches...")
        tavily = TavilySearchService()
        results = tavily.daily_search()
        
        total_results = sum(len(r) for r in results.values())
        print(f"Found {total_results} results")
        
        # Process results
        print("\nProcessing results...")
        processor = ProcessingService()
        processor.process_unprocessed_results(limit=100)
        
        print("\nDaily job completed successfully!")
        
    except Exception as e:
        print(f"Error in daily job: {e}")


def main():
    """Main scheduler entry point."""
    print("RoleRadar Daily Scheduler")
    print("=" * 60)
    print("Scheduled to run daily at 9:00 AM")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    # Schedule daily at 9 AM
    schedule.every().day.at("09:00").do(run_daily_job)
    
    # Also run immediately on startup
    print("\nRunning initial job...")
    run_daily_job()
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScheduler stopped by user")
