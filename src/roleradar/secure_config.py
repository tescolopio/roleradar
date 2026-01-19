"""Secure configuration storage with encryption for RoleRadar."""

import os
import json
import getpass
from pathlib import Path
from typing import Any, Optional, Dict
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class SecureConfigStore:
    """Encrypted configuration storage."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize secure config store.
        
        Args:
            config_path: Path to encrypted config file. Defaults to ~/.roleradar/config.enc
        """
        if config_path is None:
            config_dir = Path.home() / ".roleradar"
            config_dir.mkdir(exist_ok=True, mode=0o700)  # Owner only
            self.config_path = config_dir / "config.enc"
        else:
            self.config_path = Path(config_path)
            self.config_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        
        self._cipher: Optional[Fernet] = None
        self._config_data: Dict[str, Any] = {}
        self._master_password: Optional[str] = None
    
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Derive encryption key from password using PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,  # OWASP recommendation
        )
        return kdf.derive(password.encode())
    
    def _get_cipher(self, password: str, salt: bytes) -> Fernet:
        """Get Fernet cipher from password."""
        key = self._derive_key(password, salt)
        return Fernet(Fernet.generate_key()[:len(key)] + key[:32 - len(Fernet.generate_key()[:len(key)])])
    
    def initialize(self, master_password: Optional[str] = None) -> bool:
        """
        Initialize configuration with master password.
        
        Args:
            master_password: Master password for encryption. If None, prompts user.
        
        Returns:
            bool: True if successful
        """
        if self.config_path.exists():
            # Load existing config
            return self.unlock(master_password)
        else:
            # Create new config
            if master_password is None:
                print("\n🔐 Setting up secure configuration storage")
                print("=" * 60)
                master_password = getpass.getpass("Create master password: ")
                confirm = getpass.getpass("Confirm master password: ")
                
                if master_password != confirm:
                    print("❌ Passwords do not match")
                    return False
                
                if len(master_password) < 8:
                    print("❌ Password must be at least 8 characters")
                    return False
            
            self._master_password = master_password
            self._config_data = self._get_default_config()
            return self.save()
    
    def unlock(self, master_password: Optional[str] = None) -> bool:
        """
        Unlock existing configuration.
        
        Args:
            master_password: Master password. If None, prompts user.
        
        Returns:
            bool: True if successfully unlocked
        """
        if not self.config_path.exists():
            print("❌ No configuration found. Run initialize first.")
            return False
        
        if master_password is None:
            master_password = getpass.getpass("Enter master password: ")
        
        try:
            with open(self.config_path, 'rb') as f:
                encrypted_data = f.read()
            
            # First 32 bytes are the salt
            salt = encrypted_data[:32]
            encrypted_config = encrypted_data[32:]
            
            # Derive key and decrypt
            key = self._derive_key(master_password, salt)
            import base64
            fernet_key = base64.urlsafe_b64encode(key)
            cipher = Fernet(fernet_key)
            
            decrypted_data = cipher.decrypt(encrypted_config)
            self._config_data = json.loads(decrypted_data.decode())
            self._master_password = master_password
            self._cipher = cipher
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to unlock configuration: {str(e)}")
            return False
    
    def save(self) -> bool:
        """
        Save configuration to encrypted file.
        
        Returns:
            bool: True if successful
        """
        if self._master_password is None:
            print("❌ Not initialized. Call initialize() first.")
            return False
        
        try:
            # Generate random salt
            import os as _os
            salt = _os.urandom(32)
            
            # Derive key and create cipher
            key = self._derive_key(self._master_password, salt)
            import base64
            fernet_key = base64.urlsafe_b64encode(key)
            cipher = Fernet(fernet_key)
            
            # Encrypt config data
            config_json = json.dumps(self._config_data, indent=2)
            encrypted_data = cipher.encrypt(config_json.encode())
            
            # Write salt + encrypted data
            with open(self.config_path, 'wb') as f:
                f.write(salt + encrypted_data)
            
            # Set file permissions to owner only
            os.chmod(self.config_path, 0o600)
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to save configuration: {str(e)}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config_data.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """
        Set configuration value and save.
        
        Args:
            key: Configuration key
            value: Configuration value
        
        Returns:
            bool: True if successful
        """
        self._config_data[key] = value
        return self.save()
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration data (non-sensitive view)."""
        # Return copy without exposing internal reference
        return self._config_data.copy()
    
    def update(self, config_dict: Dict[str, Any]) -> bool:
        """
        Update multiple configuration values.
        
        Args:
            config_dict: Dictionary of key-value pairs to update
        
        Returns:
            bool: True if successful
        """
        self._config_data.update(config_dict)
        return self.save()
    
    def change_password(self, new_password: str) -> bool:
        """
        Change master password.
        
        Args:
            new_password: New master password
        
        Returns:
            bool: True if successful
        """
        if len(new_password) < 8:
            print("❌ Password must be at least 8 characters")
            return False
        
        old_password = self._master_password
        self._master_password = new_password
        
        if self.save():
            return True
        else:
            self._master_password = old_password
            return False
    
    def export_to_json(self, filepath: str, include_sensitive: bool = False) -> bool:
        """
        Export configuration to JSON file.
        
        Args:
            filepath: Output file path
            include_sensitive: Include API keys and passwords
        
        Returns:
            bool: True if successful
        """
        try:
            export_data = self._config_data.copy()
            
            if not include_sensitive:
                # Mask sensitive data
                sensitive_keys = ['TAVILY_API_KEY', 'GROQ_API_KEY', 'DB_PASSWORD', 
                                'REDIS_PASSWORD', 'FLASK_SECRET_KEY']
                for key in sensitive_keys:
                    if key in export_data:
                        export_data[key] = "***REDACTED***"
            
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            print(f"✓ Configuration exported to {filepath}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to export configuration: {str(e)}")
            return False
    
    def import_from_json(self, filepath: str) -> bool:
        """
        Import configuration from JSON file.
        
        Args:
            filepath: Input file path
        
        Returns:
            bool: True if successful
        """
        try:
            with open(filepath, 'r') as f:
                import_data = json.load(f)
            
            self._config_data.update(import_data)
            
            if self.save():
                print(f"✓ Configuration imported from {filepath}")
                return True
            else:
                return False
            
        except Exception as e:
            print(f"❌ Failed to import configuration: {str(e)}")
            return False
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration structure."""
        return {
            # API Keys - to be set by user
            "TAVILY_API_KEY": "",
            "GROQ_API_KEY": "",
            
            # Database
            "DB_HOST": "localhost",
            "DB_PORT": 5433,
            "DB_NAME": "roleradar",
            "DB_USER": "roleradar",
            "DB_PASSWORD": "",
            
            # Redis
            "REDIS_HOST": "localhost",
            "REDIS_PORT": 6379,
            "REDIS_PASSWORD": "",
            
            # Flask
            "FLASK_SECRET_KEY": os.urandom(32).hex(),
            "FLASK_HOST": "0.0.0.0",
            "FLASK_PORT": 5000,
            
            # Timezone
            "TIMEZONE": "America/New_York",
            
            # Search Roles
            "SEARCH_ROLES": [
                "security engineer",
                "compliance officer",
                "GRC analyst",
                "Chief Information Security Officer (CISO)",
                "data protection officer (DPO)",
                "security leadership",
                "security architect",
                "InfoSec director",
            ],
            
            # Schedule Times
            "SCHEDULE_TIMES": ["08:00", "12:00", "15:00"],
            
            # Scoring Weights
            "SCORING_WEIGHTS": {
                "explicit_job_posting": 0.4,
                "hiring_signals": 0.3,
                "company_growth": 0.2,
                "recent_activity": 0.1,
            }
        }
    
    def is_configured(self) -> bool:
        """Check if all required configuration is set."""
        required_keys = ["TAVILY_API_KEY", "GROQ_API_KEY"]
        return all(self.get(key) for key in required_keys)
    
    def get_database_url(self) -> str:
        """Build DATABASE_URL from components."""
        if self.get("DATABASE_URL"):
            return self.get("DATABASE_URL")
        
        db_user = self.get("DB_USER", "roleradar")
        db_pass = self.get("DB_PASSWORD", "")
        db_host = self.get("DB_HOST", "localhost")
        db_port = self.get("DB_PORT", 5433)
        db_name = self.get("DB_NAME", "roleradar")
        
        return f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


# Global instance
_secure_config: Optional[SecureConfigStore] = None


def get_secure_config() -> SecureConfigStore:
    """Get global secure config instance."""
    global _secure_config
    if _secure_config is None:
        _secure_config = SecureConfigStore()
    return _secure_config
