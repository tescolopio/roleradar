#!/usr/bin/env python3
"""Configuration manager for RoleRadar - manage roles and schedules."""

import argparse
import json
import sys
from datetime import datetime
from src.roleradar.config import config


def validate_time_format(time_str: str) -> bool:
    """Validate time string is in HH:MM format."""
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False


def display_current_config():
    """Display current configuration."""
    print("\n╔" + "═"*58 + "╗")
    print("║" + " Current Configuration".center(58) + "║")
    print("╚" + "═"*58 + "╝\n")
    
    print(f"Timezone: {config.TIMEZONE}")
    print(f"\nSearch Roles ({len(config.SEARCH_ROLES)}):")
    for i, role in enumerate(config.SEARCH_ROLES, 1):
        print(f"  {i}. {role}")
    
    print(f"\nScheduled Search Times ({len(config.SCHEDULE_TIMES)}):")
    for time_slot in config.SCHEDULE_TIMES:
        print(f"  • {time_slot} {config.TIMEZONE}")
    
    print(f"\nTotal Search Queries: {len(config.SEARCH_QUERIES)}")
    print()


def set_roles(roles_str: str):
    """Set search roles from comma-separated string."""
    roles = [role.strip() for role in roles_str.split(",")]
    roles = [r for r in roles if r]  # Remove empty strings
    
    if not roles:
        print("Error: No valid roles provided")
        return False
    
    config.update_search_roles(roles)
    print(f"\n✓ Updated search roles to {len(roles)} roles")
    for i, role in enumerate(roles, 1):
        print(f"  {i}. {role}")
    print()
    return True


def set_schedule(times_str: str):
    """Set scheduled search times from comma-separated string."""
    times = [t.strip() for t in times_str.split(",")]
    
    # Validate all times
    invalid_times = []
    for t in times:
        if not validate_time_format(t):
            invalid_times.append(t)
    
    if invalid_times:
        print(f"Error: Invalid time format(s): {', '.join(invalid_times)}")
        print("Times must be in HH:MM format (24-hour), e.g., 08:00, 14:30")
        return False
    
    # Sort times
    times = sorted(times)
    config.update_schedule_times(times)
    print(f"\n✓ Updated scheduled times to {len(times)} time(s)")
    for time_slot in times:
        print(f"  • {time_slot}")
    print()
    return True


def add_role(role: str):
    """Add a single role to the search list."""
    role = role.strip()
    if not role:
        print("Error: Role cannot be empty")
        return False
    
    if role in config.SEARCH_ROLES:
        print(f"Role '{role}' already exists in configuration")
        return False
    
    new_roles = config.SEARCH_ROLES + [role]
    config.update_search_roles(new_roles)
    print(f"✓ Added role: {role}")
    return True


def remove_role(role: str):
    """Remove a single role from the search list."""
    role = role.strip()
    
    if role not in config.SEARCH_ROLES:
        print(f"Error: Role '{role}' not found in configuration")
        return False
    
    new_roles = [r for r in config.SEARCH_ROLES if r != role]
    if not new_roles:
        print("Error: Cannot remove all roles - at least one role must exist")
        return False
    
    config.update_search_roles(new_roles)
    print(f"✓ Removed role: {role}")
    return True


def add_schedule_time(time_str: str):
    """Add a single time to the schedule."""
    time_str = time_str.strip()
    
    if not validate_time_format(time_str):
        print(f"Error: Invalid time format '{time_str}'")
        print("Time must be in HH:MM format (24-hour), e.g., 08:00")
        return False
    
    if time_str in config.SCHEDULE_TIMES:
        print(f"Time '{time_str}' already exists in schedule")
        return False
    
    new_times = sorted(config.SCHEDULE_TIMES + [time_str])
    config.update_schedule_times(new_times)
    print(f"✓ Added scheduled time: {time_str}")
    return True


def remove_schedule_time(time_str: str):
    """Remove a single time from the schedule."""
    time_str = time_str.strip()
    
    if time_str not in config.SCHEDULE_TIMES:
        print(f"Error: Time '{time_str}' not found in schedule")
        return False
    
    new_times = [t for t in config.SCHEDULE_TIMES if t != time_str]
    if not new_times:
        print("Error: Cannot remove all scheduled times - at least one time must exist")
        return False
    
    config.update_schedule_times(new_times)
    print(f"✓ Removed scheduled time: {time_str}")
    return True


def export_config(filename: str):
    """Export current configuration to JSON file."""
    config_data = {
        "timezone": config.TIMEZONE,
        "search_roles": config.SEARCH_ROLES,
        "schedule_times": config.SCHEDULE_TIMES,
        "exported_at": datetime.now().isoformat(),
    }
    
    try:
        with open(filename, 'w') as f:
            json.dump(config_data, f, indent=2)
        print(f"✓ Configuration exported to {filename}")
        return True
    except Exception as e:
        print(f"Error exporting configuration: {e}")
        return False


def import_config(filename: str):
    """Import configuration from JSON file."""
    try:
        with open(filename, 'r') as f:
            config_data = json.load(f)
        
        if "search_roles" in config_data:
            config.update_search_roles(config_data["search_roles"])
        
        if "schedule_times" in config_data:
            config.update_schedule_times(config_data["schedule_times"])
        
        print(f"✓ Configuration imported from {filename}")
        return True
    except Exception as e:
        print(f"Error importing configuration: {e}")
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="RoleRadar Configuration Manager"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Show current config
    subparsers.add_parser('show', help='Display current configuration')
    
    # Set roles
    set_roles_parser = subparsers.add_parser(
        'set-roles',
        help='Set search roles (comma-separated)'
    )
    set_roles_parser.add_argument(
        'roles',
        help='Comma-separated list of roles, e.g., "security engineer, CISO, compliance officer"'
    )
    
    # Add role
    add_role_parser = subparsers.add_parser('add-role', help='Add a single role')
    add_role_parser.add_argument('role', help='Role to add')
    
    # Remove role
    remove_role_parser = subparsers.add_parser('remove-role', help='Remove a single role')
    remove_role_parser.add_argument('role', help='Role to remove')
    
    # Set schedule
    set_schedule_parser = subparsers.add_parser(
        'set-schedule',
        help='Set search schedule times (comma-separated, HH:MM format)'
    )
    set_schedule_parser.add_argument(
        'times',
        help='Comma-separated times in 24-hour format, e.g., "08:00, 12:00, 15:00"'
    )
    
    # Add schedule time
    add_time_parser = subparsers.add_parser(
        'add-time',
        help='Add a single scheduled time'
    )
    add_time_parser.add_argument('time', help='Time in HH:MM format (24-hour)')
    
    # Remove schedule time
    remove_time_parser = subparsers.add_parser(
        'remove-time',
        help='Remove a single scheduled time'
    )
    remove_time_parser.add_argument('time', help='Time in HH:MM format (24-hour)')
    
    # Export
    export_parser = subparsers.add_parser('export', help='Export configuration to JSON file')
    export_parser.add_argument('filename', help='Output filename')
    
    # Import
    import_parser = subparsers.add_parser('import', help='Import configuration from JSON file')
    import_parser.add_argument('filename', help='Input filename')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    success = True
    
    if args.command == 'show':
        display_current_config()
    
    elif args.command == 'set-roles':
        success = set_roles(args.roles)
    
    elif args.command == 'add-role':
        success = add_role(args.role)
    
    elif args.command == 'remove-role':
        success = remove_role(args.role)
    
    elif args.command == 'set-schedule':
        success = set_schedule(args.times)
    
    elif args.command == 'add-time':
        success = add_time(args.time)
    
    elif args.command == 'remove-time':
        success = remove_time(args.time)
    
    elif args.command == 'export':
        success = export_config(args.filename)
    
    elif args.command == 'import':
        success = import_config(args.filename)
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
