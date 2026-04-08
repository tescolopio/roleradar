from .tavily_service import TavilySearchService
from .brave_service import BraveSearchService
from ..config import config

def get_search_service():
    """Return the configured search service."""
    if getattr(config, "TAVILY_API_KEY", None):
        return TavilySearchService()
    return BraveSearchService()
