#!/usr/bin/env python3
"""Secure configuration manager for RoleRadar - manage credentials securely."""

import argparse
import json
import sys
import getpass
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from roleradar.secure_config import SecureConfigStore


def display_current_config(store: SecureConfigStore, show_sensitive: bool = False):
    """Display current configuration."""
    print("\n╔" + "═"*70 + "╗")
    print("║" + " RoleRadar Secure Configuration".center(70) + "║")
    print("╚" + "═"*70 + "╝\n")
    
    config_data = store.get_all()
    
    print("🔐 Security Status: ENCRYPTED")
    print(f"📍 Storage: {store.config_path}")
    print()
    
    print("⚙️  Application Settings")
    print("─" * 70)
    print(f"Timezone: {config_data.get('TIMEZONE')}")
    print(f"Flask Host: {config_data.get('FLASK_HOST')}:{config_data.get('FLASK_PORT')}")
    print()
    
    print("🔍 Search Configuration")
    print("─" * 70)
    roles = config_data.get('SEARCH_ROLES', [])
    print(f"Search Roles ({len(roles)}):")
    for i, role in enumerate(roles, 1):
        print(f"  {i}. {role}")
    
    times = config_data.get('SCHEDULE_TIMES', [])
    print(f"\nScheduled Search Times ({len(times)}):")
    for time_slot in times:
        print(f"  • {time_slot} {config_data.get('TIMEZONE')}")
    print()
    
    print("🔑 API Keys & Credentials")
    print("─" * 70)
    
    # Show API keys status
    tavily_key = config_data.get('TAVILY_API_KEY', '')
    groq_key = config_data.get('GROQ_API_KEY', '')
    
    if show_sensitive:
        print(f"Tavily API Key: {tavily_key if tavily_key else '❌ NOT SET'}")
        print(f"Groq API Key: {groq_key if groq_key else '❌ NOT SET'}")
    else:
        tavily_status = "✅ SET" if tavily_key else "❌ NOT SET"
        groq_status = "✅ SET" if groq_key else "❌ NOT SET"
        print(f"Tavily API Key: {tavily_status}")
        print(f"Groq API Key: {groq_status}")
    
    print()
    print("💾 Database Configuration")
    print("─" * 70)
    db_host = config_data.get('DB_HOST', '')
    db_port = config_data.get('DB_PORT', '')
    db_name = config_data.get('DB_NAME', '')
    db_user = config_data.get('DB_USER', '')
    db_pass = config_data.get('DB_PASSWORD', '')
    
    print(f"Host: {db_host}:{db_port}")
    print(f"Database: {db_name}")
    print(f"User: {db_user}")
    if show_sensitive:
        print(f"Password: {db_pass if db_pass else '❌ NOT SET'}")
    else:
        print(f"Password: {'✅ SET' if db_pass else '❌ NOT SET'}")
    
    print()
    
    # Configuration completeness check
    required_set = bool(tavily_key and groq_key)
    if required_set:
        print("✅ All required credentials are configured")
    else:
        print("⚠️  Some required credentials are missing")
        if not tavily_key:
            print("   • Tavily API Key required")
        if not groq_key:
            print("   • Groq API Key required")
    print()


def initialize_config():
    """Initialize new secure configuration."""
    print("\n🔐 RoleRadar Secure Configuration Setup")
    print("═" * 70)
    print()
    
    store = SecureConfigStore()
    
    # Check if already exists
    if store.config_path.exists():
        print(f"⚠️  Configuration already exists at: {store.config_path}")
        response = input("Overwrite existing configuration? (yes/no): ")
        if response.lower() != 'yes':
            print("Aborted.")
            return False
    
    # Initialize with password
    if not store.initialize():
        return False
    
    print("\n✅ Secure configuration initialized!")
    print(f"📍 Configuration stored at: {store.config_path}")
    print()
    
    # Prompt for API keys
    print("Let's set up your API credentials...")
    print()
    
    tavily_key = input("Enter Tavily API Key (press Enter to skip): ").strip()
    if tavily_key:
        store.set("TAVILY_API_KEY", tavily_key)
        print("✅ Tavily API Key saved")
    
    groq_key = input("Enter Groq API Key (press Enter to skip): ").strip()
    if groq_key:
        store.set("GROQ_API_KEY", groq_key)
        print("✅ Groq API Key saved")
    
    print()
    
    # Database credentials
    print("Database Configuration (press Enter to use defaults):")
    db_pass = getpass.getpass("Database Password [leave empty for default]: ")
    if db_pass:
        store.set("DB_PASSWORD", db_pass)
        print("✅ Database password saved")
    
    redis_pass = getpass.getpass("Redis Password [leave empty for default]: ")
    if redis_pass:
        store.set("REDIS_PASSWORD", redis_pass)
        print("✅ Redis password saved")
    
    print()
    print("✅ Secure configuration setup complete!")
    print()
    print("Next steps:")
    print("  1. Run 'python secure_config_manager.py show' to view configuration")
    print("  2. Use 'python secure_config_manager.py set-key' to update credentials")
    print("  3. Start RoleRadar - it will automatically use secure storage")
    print()
    
    return True


def migrate_from_env():
    """Migrate configuration from .env file to secure storage."""
    print("\n🔄 Migrating from .env to secure storage")
    print("═" * 70)
    print()
    
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ .env file not found")
        return False
    
    # Load .env
    from dotenv import dotenv_values
    env_vars = dotenv_values(".env")
    
    store = SecureConfigStore()
    
    if store.config_path.exists():
        print(f"⚠️  Secure configuration already exists")
        response = input("Merge with existing configuration? (yes/no): ")
        if response.lower() != 'yes':
            print("Aborted.")
            return False
        
        if not store.unlock():
            return False
    else:
        if not store.initialize():
            return False
    
    # Migrate credentials
    migrated = []
    
    keys_to_migrate = [
        'TAVILY_API_KEY', 'GROQ_API_KEY',
        'DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD',
        'REDIS_HOST', 'REDIS_PORT', 'REDIS_PASSWORD',
        'FLASK_SECRET_KEY', 'FLASK_HOST', 'FLASK_PORT',
        'TIMEZONE'
    ]
    
    for key in keys_to_migrate:
        if key in env_vars and env_vars[key]:
            # Handle type conversions
            value = env_vars[key]
            if key in ['DB_PORT', 'REDIS_PORT', 'FLASK_PORT']:
                try:
                    value = int(value)
                except ValueError:
                    pass
            
            store.set(key, value)
            migrated.append(key)
    
    # Migrate JSON arrays
    if 'SEARCH_ROLES' in env_vars:
        try:
            roles = json.loads(env_vars['SEARCH_ROLES'])
            store.set('SEARCH_ROLES', roles)
            migrated.append('SEARCH_ROLES')
        except json.JSONDecodeError:
            pass
    
    if 'SCHEDULE_TIMES' in env_vars:
        try:
            times = json.loads(env_vars['SCHEDULE_TIMES'])
            store.set('SCHEDULE_TIMES', times)
            migrated.append('SCHEDULE_TIMES')
        except json.JSONDecodeError:
            pass
    
    print(f"\n✅ Successfully migrated {len(migrated)} configuration values")
    print()
    print("Migrated keys:")
    for key in migrated:
        print(f"  • {key}")
    
    print()
    print("⚠️  IMPORTANT: Your credentials are now securely encrypted!")
    print()
    print("Recommended next steps:")
    print("  1. Verify migration: python secure_config_manager.py show")
    print("  2. Backup .env file: cp .env .env.backup")
    print("  3. Remove sensitive data from .env (keep only non-sensitive defaults)")
    print()
    
    return True


def set_key(store: SecureConfigStore, key: str, value: str = None):
    """Set a configuration key."""
    if value is None:
        # Prompt for value
        if 'PASSWORD' in key.upper() or 'KEY' in key.upper() or 'SECRET' in key.upper():
            value = getpass.getpass(f"Enter value for {key}: ")
        else:
            value = input(f"Enter value for {key}: ")
    
    # Handle type conversions
    if key in ['DB_PORT', 'REDIS_PORT', 'FLASK_PORT']:
        try:
            value = int(value)
        except ValueError:
            print(f"❌ Invalid port number")
            return False
    
    if store.set(key, value):
        print(f"✅ {key} updated successfully")
        return True
    else:
        print(f"❌ Failed to update {key}")
        return False


def set_roles(store: SecureConfigStore, roles_str: str):
    """Set search roles from comma-separated string."""
    roles = [role.strip() for role in roles_str.split(",")]
    roles = [r for r in roles if r]
    
    if not roles:
        print("❌ No valid roles provided")
        return False
    
    if store.set("SEARCH_ROLES", roles):
        print(f"\n✅ Updated search roles to {len(roles)} roles:")
        for i, role in enumerate(roles, 1):
            print(f"  {i}. {role}")
        return True
    else:
        return False


def set_schedule(store: SecureConfigStore, times_str: str):
    """Set scheduled search times."""
    from datetime import datetime
    
    times = [t.strip() for t in times_str.split(",")]
    
    # Validate times
    invalid = []
    for t in times:
        try:
            datetime.strptime(t, "%H:%M")
        except ValueError:
            invalid.append(t)
    
    if invalid:
        print(f"❌ Invalid time format(s): {', '.join(invalid)}")
        print("Times must be in HH:MM format (24-hour)")
        return False
    
    times = sorted(times)
    
    if store.set("SCHEDULE_TIMES", times):
        print(f"\n✅ Updated schedule to {len(times)} time(s):")
        for time_slot in times:
            print(f"  • {time_slot}")
        return True
    else:
        return False


def change_password(store: SecureConfigStore):
    """Change master password."""
    print("\n🔐 Change Master Password")
    print("─" * 70)
    
    new_password = getpass.getpass("Enter new password: ")
    confirm = getpass.getpass("Confirm new password: ")
    
    if new_password != confirm:
        print("❌ Passwords do not match")
        return False
    
    if store.change_password(new_password):
        print("✅ Master password changed successfully")
        return True
    else:
        return False


def export_config(store: SecureConfigStore, filepath: str, include_sensitive: bool):
    """Export configuration to JSON."""
    return store.export_to_json(filepath, include_sensitive)


def import_config(store: SecureConfigStore, filepath: str):
    """Import configuration from JSON."""
    return store.import_from_json(filepath)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="RoleRadar Secure Configuration Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Initialize secure configuration
  python secure_config_manager.py init
  
  # Migrate from .env file
  python secure_config_manager.py migrate
  
  # View configuration
  python secure_config_manager.py show
  
  # Set API key
  python secure_config_manager.py set-key TAVILY_API_KEY
  
  # Update search roles
  python secure_config_manager.py set-roles "security engineer, CISO, GRC analyst"
  
  # Update schedule
  python secure_config_manager.py set-schedule "08:00, 12:00, 16:00"
  
  # Change master password
  python secure_config_manager.py change-password
  
  # Export configuration (without sensitive data)
  python secure_config_manager.py export config-backup.json
  
  # Export with sensitive data
  python secure_config_manager.py export config-backup.json --include-sensitive
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Init command
    subparsers.add_parser('init', help='Initialize secure configuration')
    
    # Migrate command
    subparsers.add_parser('migrate', help='Migrate from .env to secure storage')
    
    # Show command
    show_parser = subparsers.add_parser('show', help='Display current configuration')
    show_parser.add_argument('--show-sensitive', action='store_true',
                            help='Show sensitive values (API keys, passwords)')
    
    # Set-key command
    setkey_parser = subparsers.add_parser('set-key', help='Set configuration value')
    setkey_parser.add_argument('key', help='Configuration key name')
    setkey_parser.add_argument('value', nargs='?', help='Value (will prompt if not provided)')
    
    # Set-roles command
    setroles_parser = subparsers.add_parser('set-roles', help='Set search roles')
    setroles_parser.add_argument('roles', help='Comma-separated list of roles')
    
    # Set-schedule command
    setschedule_parser = subparsers.add_parser('set-schedule', help='Set schedule times')
    setschedule_parser.add_argument('times', help='Comma-separated times in HH:MM format')
    
    # Change-password command
    subparsers.add_parser('change-password', help='Change master password')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export configuration to JSON')
    export_parser.add_argument('filepath', help='Output file path')
    export_parser.add_argument('--include-sensitive', action='store_true',
                              help='Include sensitive values in export')
    
    # Import command
    import_parser = subparsers.add_parser('import', help='Import configuration from JSON')
    import_parser.add_argument('filepath', help='Input file path')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    # Handle commands
    if args.command == 'init':
        return 0 if initialize_config() else 1
    
    elif args.command == 'migrate':
        return 0 if migrate_from_env() else 1
    
    # For other commands, load existing config
    store = SecureConfigStore()
    
    if not store.config_path.exists():
        print("❌ No secure configuration found")
        print("Run: python secure_config_manager.py init")
        return 1
    
    if not store.unlock():
        return 1
    
    if args.command == 'show':
        display_current_config(store, args.show_sensitive)
        return 0
    
    elif args.command == 'set-key':
        return 0 if set_key(store, args.key, args.value) else 1
    
    elif args.command == 'set-roles':
        return 0 if set_roles(store, args.roles) else 1
    
    elif args.command == 'set-schedule':
        return 0 if set_schedule(store, args.times) else 1
    
    elif args.command == 'change-password':
        return 0 if change_password(store) else 1
    
    elif args.command == 'export':
        return 0 if export_config(store, args.filepath, args.include_sensitive) else 1
    
    elif args.command == 'import':
        return 0 if import_config(store, args.filepath) else 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
