"""Database models for RoleRadar."""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Boolean, Date
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
    processed_date = Column(DateTime)
    
    # Extraction tracking - shows what AI extracted
    extracted_company = Column(String(255))
    extracted_job_title = Column(String(255))
    extracted_role_type = Column(String(100))
    extracted_location = Column(String(255))
    extracted_keywords = Column(Text)  # JSON array as string
    
    # Signal tracking - shows what hiring signals were detected
    detected_signal = Column(Boolean, default=False)
    signal_type = Column(String(100))
    signal_confidence = Column(Float)
    signal_description = Column(Text)
    
    # Error tracking - shows any processing issues
    processing_error = Column(Text)
    
    def __repr__(self):
        return f"<SearchResult(title='{self.title}', query='{self.query}')>"


class UserOpportunityTracking(Base):
    """User tracking for opportunities."""
    __tablename__ = 'user_opportunity_tracking'

    id = Column(Integer, primary_key=True)
    opportunity_id = Column(Integer, ForeignKey('opportunities.id', ondelete='CASCADE'), nullable=False)
    status = Column(String(50), default='interested')
    notes = Column(Text)
    favorite = Column(Boolean, default=False)
    applied_date = Column(DateTime(timezone=True))
    last_updated = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    # Relationship
    opportunity = relationship('Opportunity', backref='tracking')

    def __repr__(self):
        return f"<UserOpportunityTracking(opportunity_id={self.opportunity_id}, status='{self.status}')>"


class ConfigurationSetting(Base):
    """Persistent configuration settings storage."""
    __tablename__ = 'configuration_settings'

    id = Column(Integer, primary_key=True)
    key = Column(String(255), nullable=False, unique=True, index=True)
    value = Column(Text, nullable=False)  # JSON encoded value
    description = Column(Text)
    last_updated = Column(DateTime, default=utc_now, onupdate=utc_now)
    created_at = Column(DateTime, default=utc_now)

    def __repr__(self):
        return f"<ConfigurationSetting(key='{self.key}')>"


class APIUsageLog(Base):
    """Track API usage for monitoring and quota management."""
    __tablename__ = 'api_usage_logs'

    id = Column(Integer, primary_key=True)
    api_name = Column(String(50), nullable=False, index=True)  # 'tavily', 'groq'
    endpoint = Column(String(255))  # e.g., 'search', 'extract_entities'
    request_count = Column(Integer, default=1, nullable=False)
    date = Column(Date, nullable=False, index=True)
    hour = Column(Integer)  # 0-23 for hourly tracking
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    # Usage metadata
    query = Column(Text)  # The search query or prompt (first 500 chars)
    result_count = Column(Integer)  # Number of results returned
    error = Column(Text)  # Error message if failed

    def __repr__(self):
        return f"<APIUsageLog({self.api_name}, {self.date}, count={self.request_count})>"
