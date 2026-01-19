# RoleRadar Configuration Guide

## Overview

RoleRadar now supports **configurable search roles** and **flexible scheduling** to search for opportunities at custom times throughout the day. This guide explains how to configure these features.

## Quick Start

### Default Configuration

By default, RoleRadar searches for 8 security/compliance roles at 3 times daily:
- **8:00 AM EST**
- **12:00 PM EST**  
- **3:00 PM EST**

Default roles:
- Security Engineer
- Compliance Officer
- GRC Analyst
- Chief Information Security Officer (CISO)
- Data Protection Officer (DPO)
- Security Leadership
- Security Architect
- InfoSec Director

## Configuration Methods

### Method 1: Environment Variables (.env file)

Edit your `.env` file to customize roles and schedules:

```bash
# Set timezone (see https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
TIMEZONE=America/New_York

# Set search roles (JSON array format)
SEARCH_ROLES=["security engineer", "compliance officer", "CISO", "GRC analyst"]

# Set scheduled times (JSON array, 24-hour format)
SCHEDULE_TIMES=["08:00", "12:00", "15:00"]
```

#### Example Configurations

**Search 3 times a day:**
```bash
SCHEDULE_TIMES=["08:00", "12:00", "15:00"]
```

**Search every 4 hours (6 times):**
```bash
SCHEDULE_TIMES=["06:00", "10:00", "14:00", "18:00", "22:00", "02:00"]
```

**Search only once at 9 AM:**
```bash
SCHEDULE_TIMES=["09:00"]
```

**Search for different roles:**
```bash
SEARCH_ROLES=["security engineer", "compliance officer", "privacy officer", "data scientist"]
```

### Method 2: Configuration Manager CLI

Use the `config_manager.py` script to manage configuration at runtime:

#### Display Current Configuration

```bash
python config_manager.py show
```

Output:
```
╔══════════════════════════════════════════════════════════╗
║                 Current Configuration                    ║
╚══════════════════════════════════════════════════════════╝

Timezone: America/New_York

Search Roles (8):
  1. security engineer
  2. compliance officer
  3. GRC analyst
  4. Chief Information Security Officer (CISO)
  5. data protection officer (DPO)
  6. security leadership
  7. security architect
  8. InfoSec director

Scheduled Search Times (3):
  • 08:00 America/New_York
  • 12:00 America/New_York
  • 15:00 America/New_York

Total Search Queries: 16
```

#### Set Roles

Replace entire role list:

```bash
python config_manager.py set-roles "security engineer, compliance officer, privacy officer"
```

#### Add a Role

```bash
python config_manager.py add-role "CISO"
```

#### Remove a Role

```bash
python config_manager.py remove-role "security architect"
```

#### Set Schedule Times

Replace entire schedule:

```bash
python config_manager.py set-schedule "06:00, 10:00, 14:00, 18:00"
```

#### Add a Scheduled Time

```bash
python config_manager.py add-time "21:00"
```

#### Remove a Scheduled Time

```bash
python config_manager.py remove-time "15:00"
```

#### Export Configuration

Save current configuration to JSON:

```bash
python config_manager.py export backup-config.json
```

#### Import Configuration

Load configuration from JSON file:

```bash
python config_manager.py import backup-config.json
```

## Advanced Configuration

### Role Examples

**For AI/ML Security Specialists:**
```bash
python config_manager.py set-roles "ML engineer, AI engineer, prompt engineer, AI safety officer"
```

**For Startups/Scale-ups:**
```bash
python config_manager.py set-roles "DevSecOps engineer, cloud security architect, infrastructure engineer"
```

**For Enterprise Environments:**
```bash
python config_manager.py set-roles "CISO, information security director, security architect, principal security engineer"
```

### Schedule Examples

**Morning-only searches:**
```bash
python config_manager.py set-schedule "06:00, 09:00, 12:00"
```

**Business hours (every 2 hours):**
```bash
python config_manager.py set-schedule "08:00, 10:00, 12:00, 14:00, 16:00"
```

**24/7 monitoring (every 6 hours):**
```bash
python config_manager.py set-schedule "00:00, 06:00, 12:00, 18:00"
```

## Time Zones

RoleRadar supports any IANA timezone. Set the `TIMEZONE` environment variable to your desired timezone:

Common timezones:
- `America/New_York` - Eastern Time
- `America/Chicago` - Central Time
- `America/Denver` - Mountain Time
- `America/Los_Angeles` - Pacific Time
- `America/Anchorage` - Alaska Time
- `Europe/London` - GMT/BST
- `Europe/Paris` - CET/CEST
- `Asia/Tokyo` - JST
- `Australia/Sydney` - AEDT/AEST
- `UTC` - Coordinated Universal Time

Full list: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

## Runtime Configuration

Roles and schedules can be changed while the scheduler is running. The scheduler will pick up changes:

1. Modify `.env` file or use `config_manager.py`
2. Changes take effect immediately (no restart needed)
3. Next scheduled job will use new configuration

## Search Query Generation

Search queries are automatically generated from your configured roles. For each role, RoleRadar creates two query variations:

- `"{role} job openings"`
- `"{role} hiring"`

**Example:** If you configure roles as `["security engineer", "CISO"]`, the searches will be:

1. "security engineer job openings"
2. "security engineer hiring"
3. "CISO job openings"
4. "CISO hiring"

## Configuration Persistence

Configuration changes are persisted in two ways:

1. **Environment Variables** (`.env` file) - Permanent storage
2. **Runtime Config** - Active for current scheduler session

To ensure changes persist across restarts:
- Edit `.env` directly, or
- Use `config_manager.py` commands (updates `.env` automatically)

## Monitoring

When the scheduler starts, it displays the active configuration:

```
╔══════════════════════════════════════════════════════════╗
║           RoleRadar Daily Scheduler                      ║
╚══════════════════════════════════════════════════════════╝

Configuration:
  Timezone: America/New_York
  Roles: security engineer, compliance officer, CISO, ...
  Daily searches: 3 times
  Times: 08:00, 12:00, 15:00

Running initial job...
...

Next scheduled runs:
  → 2026-01-19 08:00:00
  → 2026-01-19 12:00:00
  → 2026-01-19 15:00:00
```

## Troubleshooting

### Changes not taking effect

If configuration changes aren't reflected:
1. Check your `.env` file is in the correct location
2. Restart the scheduler: `Ctrl+C` to stop, then run `python scheduler.py` again
3. Verify changes with `python config_manager.py show`

### Invalid time format

Times must be in 24-hour `HH:MM` format:
- ✓ Valid: `08:00`, `14:30`, `23:59`, `00:00`
- ✗ Invalid: `8:00`, `2:30 PM`, `14.30`

### Empty roles or schedules

At least one role and one scheduled time must exist. You cannot remove all roles or times.

## API Usage

To programmatically configure RoleRadar in your code:

```python
from src.roleradar.config import config

# Update roles
config.update_search_roles([
    "security engineer",
    "compliance officer",
    "CISO",
])

# Update schedule times
config.update_schedule_times(["08:00", "12:00", "15:00"])

# Get current config as dict
current_config = config.get_config_dict()
print(current_config)
# Output: {
#     "timezone": "America/New_York",
#     "search_roles": ["security engineer", "compliance officer", "CISO"],
#     "schedule_times": ["08:00", "12:00", "15:00"],
#     "search_queries_count": 6
# }
```

## Community Sharing

To share your configuration with the community:

1. Export your configuration:
   ```bash
   python config_manager.py export my-config.json
   ```

2. Share the JSON file with others

3. They can import your configuration:
   ```bash
   python config_manager.py import my-config.json
   ```

Example configurations can be contributed to the `config-examples/` directory.
