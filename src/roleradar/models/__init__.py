"""Initialize models package."""

from .database import Base, Company, Opportunity, HiringSignal, SearchResult
from .graph import GraphDatabase

__all__ = [
    "Base",
    "Company",
    "Opportunity",
    "HiringSignal",
    "SearchResult",
    "GraphDatabase",
]
