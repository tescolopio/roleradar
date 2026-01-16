"""Configuration management for RoleRadar."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration."""
    
    # API Keys
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///roleradar.db")
    
    # Flask
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
    FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
    
    # Search settings
    SEARCH_QUERIES = [
        "security engineer job openings",
        "compliance officer positions",
        "GRC analyst hiring",
        "Chief Information Security Officer CISO jobs",
        "data protection officer DPO hiring",
        "security leadership positions",
    ]
    
    # Scoring weights
    SCORING_WEIGHTS = {
        "explicit_job_posting": 0.4,
        "hiring_signals": 0.3,
        "company_growth": 0.2,
        "recent_activity": 0.1,
    }


config = Config()
