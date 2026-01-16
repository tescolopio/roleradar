"""Database models for RoleRadar."""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


def utc_now():
    """Get current UTC time."""
    return datetime.now(timezone.utc)


class Company(Base):
    """Company entity model."""
    
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    domain = Column(String(255))
    industry = Column(String(255))
    size = Column(String(100))
    location = Column(String(255))
    description = Column(Text)
    score = Column(Float, default=0.0)
    last_updated = Column(DateTime, default=utc_now, onupdate=utc_now)
    created_at = Column(DateTime, default=utc_now)
    
    # Relationships
    opportunities = relationship("Opportunity", back_populates="company")
    signals = relationship("HiringSignal", back_populates="company")
    
    def __repr__(self):
        return f"<Company(name='{self.name}', score={self.score})>"


class Opportunity(Base):
    """Job opportunity model."""
    
    __tablename__ = "opportunities"
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    title = Column(String(255), nullable=False)
    role_type = Column(String(100))  # security, compliance, GRC
    description = Column(Text)
    url = Column(String(512))
    location = Column(String(255))
    is_active = Column(Boolean, default=True)
    posted_date = Column(DateTime)
    discovered_date = Column(DateTime, default=utc_now)
    last_seen = Column(DateTime, default=utc_now, onupdate=utc_now)
    
    # Relationships
    company = relationship("Company", back_populates="opportunities")
    
    def __repr__(self):
        return f"<Opportunity(title='{self.title}', company='{self.company.name if self.company else 'N/A'}')>"


class HiringSignal(Base):
    """Hiring signal detection model."""
    
    __tablename__ = "hiring_signals"
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    signal_type = Column(String(100))  # expansion, funding, breach, compliance_news
    description = Column(Text)
    source_url = Column(String(512))
    confidence = Column(Float, default=0.0)
    detected_date = Column(DateTime, default=utc_now)
    
    # Relationships
    company = relationship("Company", back_populates="signals")
    
    def __repr__(self):
        return f"<HiringSignal(type='{self.signal_type}', company='{self.company.name if self.company else 'N/A'}')>"


class SearchResult(Base):
    """Raw search result storage."""
    
    __tablename__ = "search_results"
    
    id = Column(Integer, primary_key=True)
    query = Column(String(255), nullable=False)
    title = Column(String(512))
    content = Column(Text)
    url = Column(String(512))
    score = Column(Float)
    published_date = Column(String(100))
    retrieved_date = Column(DateTime, default=utc_now)
    processed = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<SearchResult(title='{self.title}', query='{self.query}')>"
