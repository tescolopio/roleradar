"""Configuration management for RoleRadar with secure storage."""

import os
import json
import sys
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Try to load from .env for backward compatibility (non-sensitive only)
load_dotenv()

# Import secure config store
from .secure_config import get_secure_config


class Config:
    """Application configuration with secure credential storage."""
    
    def __init__(self):
        """Initialize configuration from secure storage."""
        self._secure_store = None
        self._initialized = False
        self._load_config()
    
    def _load_config(self):
        """Load configuration from secure storage or .env fallback."""
        # Check if secure config exists
        config_dir = Path.home() / ".roleradar"
        secure_config_path = config_dir / "config.enc"
        
        if secure_config_path.exists():
            # Use secure storage
            self._secure_store = get_secure_config()
            if not self._secure_store.unlock():
                print("⚠️  Failed to unlock secure configuration")
                print("Falling back to environment variables...")
                self._load_from_env()
            else:
                self._load_from_secure()
                self._initialized = True
        else:
            # Fallback to environment variables
            self._load_from_env()
            
            # Prompt to migrate to secure storage
            if os.getenv("TAVILY_API_KEY") or os.getenv("GROQ_API_KEY"):
                print("\n⚠️  API keys detected in environment variables")
                print("For better security, run: python secure_config_manager.py init")
                print("This will migrate your credentials to encrypted storage.\n")
    
    def _load_from_secure(self):
        """Load configuration from secure storage."""
        store = self._secure_store
        
        # API Keys
        self.TAVILY_API_KEY = store.get("TAVILY_API_KEY", "")
        self.GROQ_API_KEY = store.get("GROQ_API_KEY", "")
        
        # Database
        self.DATABASE_URL = store.get_database_url()
        
        # Flask
        self.FLASK_SECRET_KEY = store.get("FLASK_SECRET_KEY", os.urandom(32).hex())
        self.FLASK_HOST = store.get("FLASK_HOST", "0.0.0.0")
        self.FLASK_PORT = int(store.get("FLASK_PORT", 5000))
        
        # Timezone
        self.TIMEZONE = store.get("TIMEZONE", "America/New_York")
        
        # Search roles and schedule
        self.SEARCH_ROLES = store.get("SEARCH_ROLES", self._get_default_roles())
        self.SCHEDULE_TIMES = store.get("SCHEDULE_TIMES", ["08:00", "12:00", "15:00"])
        
        # Scoring weights
        self.SCORING_WEIGHTS = store.get("SCORING_WEIGHTS", {
            "explicit_job_posting": 0.4,
            "hiring_signals": 0.3,
            "company_growth": 0.2,
            "recent_activity": 0.1,
        })
    
    def _load_from_env(self):
        """Load configuration from environment variables (legacy/fallback)."""
        # API Keys
        self.TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
        
        # Database
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///roleradar.db")
        
        # Flask
        self.FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
        self.FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
        self.FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
        
        # Timezone for scheduling
        self.TIMEZONE = os.getenv("TIMEZONE", "America/New_York")
        # Timezone for scheduling
        self.TIMEZONE = os.getenv("TIMEZONE", "America/New_York")
        
        # Search settings
        self.SEARCH_ROLES = self._get_default_roles()
        
        # Get roles from environment variable (JSON format) if available
        _roles_env = os.getenv("SEARCH_ROLES", "")
        if _roles_env:
            try:
                self.SEARCH_ROLES = json.loads(_roles_env)
            except json.JSONDecodeError:
                pass
        
        # Scheduled times for searches (24-hour format)
        self.SCHEDULE_TIMES = ["08:00", "12:00", "15:00"]
        _schedule_times_env = os.getenv("SCHEDULE_TIMES", "")
        if _schedule_times_env:
            try:
                self.SCHEDULE_TIMES = json.loads(_schedule_times_env)
            except json.JSONDecodeError:
                pass
        
        # Scoring weights
        self.SCORING_WEIGHTS = {
            "explicit_job_posting": 0.4,
            "hiring_signals": 0.3,
            "company_growth": 0.2,
            "recent_activity": 0.1,
        }
    
    def _get_default_roles(self):
        """Get default search roles."""
        return [
            "security engineer",
            "compliance officer",
            "GRC analyst",
            "Chief Information Security Officer (CISO)",
            "data protection officer (DPO)",
            "security leadership",
            "security architect",
            "InfoSec director",
        ]
    
    @property
    def SEARCH_QUERIES(self):
        """Generate search queries from roles."""
        return [f"{role} job openings" for role in self.SEARCH_ROLES] + [
            f"{role} hiring" for role in self.SEARCH_ROLES
        ]
    
    def update_search_roles(self, roles: list):
        """
        Update search roles at runtime.
        
        Args:
            roles: List of role titles to search for
        """
        self.SEARCH_ROLES = roles
        
        # Save to secure storage if available
        if self._secure_store:
            self._secure_store.set("SEARCH_ROLES", roles)
        else:
            # Fallback to environment variable
            os.environ["SEARCH_ROLES"] = json.dumps(roles)
    
    def update_schedule_times(self, times: list):
        """
        Update scheduled search times at runtime.
        
        Args:
            times: List of times in HH:MM format (24-hour)
        """
        self.SCHEDULE_TIMES = sorted(times)
        
        # Save to secure storage if available
        if self._secure_store:
            self._secure_store.set("SCHEDULE_TIMES", times)
        else:
            # Fallback to environment variable
            os.environ["SCHEDULE_TIMES"] = json.dumps(times)
    
    def get_config_dict(self):
        """Get current configuration as a dictionary."""
        return {
            "timezone": self.TIMEZONE,
            "search_roles": self.SEARCH_ROLES,
            "schedule_times": self.SCHEDULE_TIMES,
            "search_queries_count": len(self.SEARCH_QUERIES),
            "using_secure_storage": self._initialized,
        }
    
    def is_secure_mode(self):
        """Check if using secure storage."""
        return self._initialized


config = Config()
