#!/usr/bin/env python3
"""Scheduler for running daily searches automatically."""

import schedule
import time
from datetime import datetime
from src.roleradar.services import TavilySearchService, ProcessingService
from src.roleradar.database import db_service
from src.roleradar.config import config


def run_daily_job():
    """Run the daily search and processing job."""
    print(f"\n{'='*60}")
    print(f"Starting search job at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Searching for roles: {', '.join(config.SEARCH_ROLES)}")
    print(f"{'='*60}\n")
    
    try:
        # Initialize database if needed
        db_service.create_tables()
        
        # Run search
        print("Running searches...")
        tavily = TavilySearchService()
        results = tavily.daily_search()
        
        total_results = sum(len(r) for r in results.values())
        print(f"Found {total_results} results across {len(results)} queries")
        
        # Process results
        print("\nProcessing results...")
        processor = ProcessingService()
        processor.process_unprocessed_results(limit=100)
        
        print("\nSearch job completed successfully!")
        
    except Exception as e:
        print(f"Error in search job: {e}")


def schedule_jobs():
    """Schedule all configured search times."""
    # Clear any existing scheduled jobs
    schedule.clear()
    
    print(f"\nConfiguring {len(config.SCHEDULE_TIMES)} scheduled job(s):")
    for scheduled_time in config.SCHEDULE_TIMES:
        schedule.every().day.at(scheduled_time).do(run_daily_job)
        print(f"  ✓ Scheduled for {scheduled_time} {config.TIMEZONE}")
    
    print()


def display_next_runs():
    """Display the next scheduled run times."""
    print("\nNext scheduled runs:")
    for job in schedule.jobs:
        print(f"  → {job.next_run.strftime('%Y-%m-%d %H:%M:%S')}")
    print()


def main():
    """Main scheduler entry point."""
    print("╔" + "═"*58 + "╗")
    print("║" + " RoleRadar Daily Scheduler".center(58) + "║")
    print("╚" + "═"*58 + "╝")
    
    print(f"\nConfiguration:")
    print(f"  Timezone: {config.TIMEZONE}")
    print(f"  Roles: {', '.join(config.SEARCH_ROLES)}")
    print(f"  Daily searches: {len(config.SCHEDULE_TIMES)} times")
    print(f"  Times: {', '.join(config.SCHEDULE_TIMES)}")
    
    # Schedule all jobs
    schedule_jobs()
    
    # Run immediately on startup (optional - comment out if not desired)
    print("Running initial job...")
    run_daily_job()
    
    print("Press Ctrl+C to stop the scheduler\n")
    display_next_runs()
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScheduler stopped by user")
