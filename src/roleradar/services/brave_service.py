"""Brave search service for discovering opportunities."""

import requests
from typing import List, Dict, Any
from datetime import datetime, timezone
from ..config import config
from ..models import SearchResult
from ..database import db_service
from .api_tracker import APITracker

class BraveSearchService:
    """Service for performing targeted searches using Brave Search API."""
    
    def __init__(self, api_key=None):
        """Initialize Brave search service."""
        self.api_key = api_key or getattr(config, 'BRAVE_API_KEY', None)
        if not self.api_key:
            print("Warning: Brave API key not configured. Search functionality will be limited.")
            self.client = None
        else:
            self.client = requests.Session()
            self.client.headers.update({
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": self.api_key
            })
            
    def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Perform a search using Brave Search.

        Args:
            query: Search query string
            max_results: Maximum number of results to return

        Returns:
            List of search results
        """
        if not getattr(config, 'API_SEARCHES_ENABLED', True):
            print("⚠️  API searches are currently disabled in configuration.")
            return []

        if not self.client:
            print("Error: Brave client not initialized. Please configure BRAVE_API_KEY.")
            return []
        
        try:
            url = "https://api.search.brave.com/res/v1/web/search"
            params = {
                "q": query,
                "count": min(max_results, 20)  # Brave limits count to 20
            }
            
            response = self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            web_results = data.get("web", {}).get("results", [])
            
            results = []
            for r in web_results:
                results.append({
                    "title": r.get("title", ""),
                    "content": r.get("description", ""),
                    "url": r.get("url", ""),
                    "score": 0.5,  # Default score as Brave doesn't provide relevance score like Tavily
                    "published_date": r.get("age", "")
                })

            # Track API call
            APITracker.log_api_call(
                api_name='brave',
                endpoint='search',
                query=query,
                result_count=len(results)
            )

            return results[:max_results]
        except Exception as e:
            # Track failed call
            APITracker.log_api_call(
                api_name='brave',
                endpoint='search',
                query=query,
                error=str(e)
            )
            print(f"Error performing search for '{query}': {e}")
            return []
    
    def daily_search(self, queries: List[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Perform daily targeted searches.

        Args:
            queries: List of search queries (uses default if not provided)

        Returns:
            Dictionary mapping queries to their results
        """
        if not getattr(config, 'API_SEARCHES_ENABLED', True):
            print("⚠️  API searches are currently disabled. Skipping daily search.")
            return {}

        if queries is None:
            queries = getattr(config, 'SEARCH_QUERIES', [])
        
        all_results = {}
        
        for query in queries:
            print(f"Searching (Brave): {query}")
            results = self.search(query, max_results=10)
            all_results[query] = results
            
            self._store_search_results(query, results)
        
        return all_results
    
    def _store_search_results(self, query: str, results: List[Dict[str, Any]]):
        """Store search results in database."""
        with db_service.get_session() as session:
            for result in results:
                existing = session.query(SearchResult).filter_by(
                    url=result.get("url")
                ).first()
                
                if not existing:
                    search_result = SearchResult(
                        query=query,
                        title=result.get("title", "")[:512],
                        content=result.get("content", ""),
                        url=result.get("url", "")[:512],
                        score=result.get("score", 0.0),
                        published_date=result.get("published_date", ""),
                        retrieved_date=datetime.now(timezone.utc),
                        processed=False
                    )
                    session.add(search_result)
    
    def get_unprocessed_results(self, limit: int = 50) -> List[SearchResult]:
        """Get unprocessed search results from database."""
        with db_service.get_session() as session:
            results = session.query(SearchResult).filter_by(
                processed=False
            ).limit(limit).all()
            
            session.expunge_all()
            return results
    
    def mark_as_processed(self, result_id: int):
        """Mark a search result as processed."""
        with db_service.get_session() as session:
            result = session.query(SearchResult).get(result_id)
            if result:
                result.processed = True
