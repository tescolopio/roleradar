"""Database service for RoleRadar."""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
import os
from ..models import Base
from ..config import config


class DatabaseService:
    """Database service for managing SQL database operations."""
    
    def __init__(self, database_url=None):
        """Initialize database service with fallback support."""
        self.database_url = database_url or config.DATABASE_URL
        self.is_sqlite = False
        self.engine = self._create_engine()
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def _create_engine(self):
        """Create engine with PostgreSQL fallback to SQLite."""
        try:
            # Try PostgreSQL first
            if self.database_url.startswith('postgresql'):
                print(f"🔄 Attempting to connect to PostgreSQL: {self.database_url[:40]}...")
                engine = create_engine(self.database_url, echo=False)
                # Test connection
                with engine.connect() as conn:
                    conn.execute("SELECT 1")
                print("✅ PostgreSQL connection successful")
                return engine
            if self.database_url.startswith('sqlite:///'):
                # Extract path and create directories if needed
                import os
                
                # Handle sqlite:////absolute/path vs sqlite:///relative/path
                path_str = self.database_url.replace('sqlite:///', '')
                if path_str.startswith('/'):
                    # It's an absolute path (sqlite:////...)
                    db_path = path_str
                else:
                    # It's a relative path
                    db_path = os.path.abspath(path_str)
                    
                db_dir = os.path.dirname(db_path)
                if db_dir and not os.path.exists(db_dir):
                    try:
                        os.makedirs(db_dir, exist_ok=True)
                        print(f"📁 Created database directory: {db_dir}")
                    except OSError as e:
                        print(f"⚠️ Could not create database directory {db_dir}: {e}")
                        print("📦 Falling back to local roleradar.db")
                        self.database_url = "sqlite:///roleradar.db"
            
            # Use provided URL as-is
            return create_engine(self.database_url, echo=False)
        except Exception as pg_error:
            # Fall back to SQLite
            print(f"⚠️  PostgreSQL connection failed: {str(pg_error)[:60]}...")
            print("📦 Falling back to SQLite for local development")
            
            # Prefer shared volume path when available (works with Docker compose)
            sqlite_path = os.getenv("SQLITE_FALLBACK_URL", "sqlite:///roleradar.db")
            self.database_url = sqlite_path
            self.is_sqlite = True
            
            # Create SQLite engine with connection pooling disabled for file-based DB
            engine = create_engine(
                sqlite_path,
                echo=False,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool
            )
            
            # Enable SQLite foreign keys
            @event.listens_for(engine, "connect")
            def set_sqlite_pragma(dbapi_conn, connection_record):
                cursor = dbapi_conn.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
            
            print(f"✅ Using SQLite: {sqlite_path}")
            return engine
    
    
    def get_status(self):
        """Get database connection status."""
        if self.is_sqlite:
            return {"type": "SQLite", "path": self.database_url, "status": "ready"}
        else:
            return {"type": "PostgreSQL", "url": self.database_url[:40] + "...", "status": "ready"}
    
    def create_tables(self):
        """Create all database tables."""
        Base.metadata.create_all(bind=self.engine)
    
    def drop_tables(self):
        """Drop all database tables."""
        Base.metadata.drop_all(bind=self.engine)
    
    @contextmanager
    def get_session(self) -> Session:
        """Get a database session with context manager."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_config_value(self, key: str, default=None):
        """
        Get a configuration value from the database.

        Args:
            key: Configuration key
            default: Default value if key doesn't exist

        Returns:
            Configuration value (JSON decoded) or default
        """
        import json
        from ..models import ConfigurationSetting

        with self.get_session() as session:
            setting = session.query(ConfigurationSetting).filter_by(key=key).first()
            if setting:
                try:
                    return json.loads(setting.value)
                except json.JSONDecodeError:
                    return setting.value
            return default

    def set_config_value(self, key: str, value, description: str = None):
        """
        Set a configuration value in the database.

        Args:
            key: Configuration key
            value: Configuration value (will be JSON encoded if not string)
            description: Optional description of the setting
        """
        import json
        from ..models import ConfigurationSetting

        # Serialize value to JSON if needed
        if isinstance(value, (dict, list)):
            value_str = json.dumps(value)
        elif isinstance(value, str):
            value_str = value
        else:
            value_str = str(value)

        with self.get_session() as session:
            setting = session.query(ConfigurationSetting).filter_by(key=key).first()
            if setting:
                setting.value = value_str
                if description:
                    setting.description = description
            else:
                setting = ConfigurationSetting(
                    key=key,
                    value=value_str,
                    description=description
                )
                session.add(setting)
            session.commit()


# Global database service instance
db_service = DatabaseService()
