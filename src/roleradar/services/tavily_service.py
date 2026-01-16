"""Tavily search service for discovering opportunities."""

from typing import List, Dict, Any
from datetime import datetime
from tavily import TavilyClient
from ..config import config
from ..models import SearchResult
from ..database import db_service


class TavilySearchService:
    """Service for performing targeted searches using Tavily API."""
    
    def __init__(self, api_key=None):
        """Initialize Tavily search service."""
        self.api_key = api_key or config.TAVILY_API_KEY
        if not self.api_key:
            raise ValueError("Tavily API key is required")
        self.client = TavilyClient(api_key=self.api_key)
    
    def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Perform a search using Tavily.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of search results
        """
        try:
            response = self.client.search(
                query=query,
                max_results=max_results,
                search_depth="advanced",
                include_domains=[],
                exclude_domains=[]
            )
            
            results = response.get("results", [])
            return results
        except Exception as e:
            print(f"Error performing search for '{query}': {e}")
            return []
    
    def daily_search(self, queries: List[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Perform daily targeted searches for security, compliance, and GRC opportunities.
        
        Args:
            queries: List of search queries (uses default if not provided)
            
        Returns:
            Dictionary mapping queries to their results
        """
        if queries is None:
            queries = config.SEARCH_QUERIES
        
        all_results = {}
        
        for query in queries:
            print(f"Searching: {query}")
            results = self.search(query, max_results=10)
            all_results[query] = results
            
            # Store raw results in database
            self._store_search_results(query, results)
        
        return all_results
    
    def _store_search_results(self, query: str, results: List[Dict[str, Any]]):
        """Store search results in database."""
        with db_service.get_session() as session:
            for result in results:
                # Check if result already exists by URL
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
                        retrieved_date=datetime.utcnow(),
                        processed=False
                    )
                    session.add(search_result)
    
    def get_unprocessed_results(self, limit: int = 50) -> List[SearchResult]:
        """Get unprocessed search results from database."""
        with db_service.get_session() as session:
            results = session.query(SearchResult).filter_by(
                processed=False
            ).limit(limit).all()
            
            # Detach from session
            session.expunge_all()
            return results
    
    def mark_as_processed(self, result_id: int):
        """Mark a search result as processed."""
        with db_service.get_session() as session:
            result = session.query(SearchResult).get(result_id)
            if result:
                result.processed = True
