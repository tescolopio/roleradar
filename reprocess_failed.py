#!/usr/bin/env python3
"""Reprocess all search results that failed with mixtral errors."""

from src.roleradar.database.service import db_service
from src.roleradar.models import SearchResult
from src.roleradar.services.processing_service import ProcessingService

def reprocess_failed_results():
    """Reprocess all results that failed with mixtral model errors."""

    with db_service.get_session() as session:
        # Find all results with mixtral errors
        failed = session.query(SearchResult).filter(
            SearchResult.processing_error.like('%mixtral%')
        ).all()

        print(f"Found {len(failed)} results with old mixtral errors")

        if len(failed) == 0:
            print("No failed results to reprocess!")
            return

        # Clear errors and mark as unprocessed
        for result in failed:
            result.processing_error = None
            result.extracted_company = None
            result.extracted_job_title = None
            result.extracted_role_type = None
            result.extracted_location = None
            result.extracted_keywords = None
            result.processed = False
            result.processed_date = None

        session.commit()
        print(f"✓ Cleared {len(failed)} results, marked as unprocessed")

    # Now process them
    processor = ProcessingService()
    count = processor.process_unprocessed_results(limit=len(failed))
    print(f"✓ Reprocessed {count} results successfully!")

if __name__ == "__main__":
    reprocess_failed_results()
