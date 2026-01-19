# RoleRadar Quick Reference Card

## View & Manage Configuration

```bash
# View current settings
python config_manager.py show

# Set all roles at once (comma-separated)
python config_manager.py set-roles "security engineer, CISO, compliance officer"

# Add a single role
python config_manager.py add-role "privacy officer"

# Remove a role
python config_manager.py remove-role "security architect"

# Set all schedule times
python config_manager.py set-schedule "08:00, 12:00, 15:00"

# Add a time slot
python config_manager.py add-time "18:00"

# Remove a time slot
python config_manager.py remove-time "12:00"
```

## Import/Export Configurations

```bash
# Export current config to file
python config_manager.py export my-config.json

# Import from file
python config_manager.py import my-config.json

# Use pre-built configs
python config_manager.py import config-examples/security-compliance-focus.json
python config_manager.py import config-examples/devops-infrastructure-focus.json
python config_manager.py import config-examples/privacy-data-protection-focus.json
python config_manager.py import config-examples/continuous-monitoring-24h.json
python config_manager.py import config-examples/startup-hiring-signals.json
```

## Core Commands

```bash
# Initialize database
python roleradar.py init

# Run one search
python roleradar.py search

# Process results
python roleradar.py process

# Show statistics
python roleradar.py stats

# Start dashboard
python roleradar.py dashboard
# Then visit: http://localhost:5000

# Start scheduler (uses configured times)
python scheduler.py
```

## Environment Variables (.env)

```bash
# Search Configuration
TIMEZONE=America/New_York
SEARCH_ROLES=["security engineer", "CISO", "compliance officer"]
SCHEDULE_TIMES=["08:00", "12:00", "15:00"]

# API Keys
TAVILY_API_KEY=your_key_here
GROQ_API_KEY=your_key_here

# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# Flask
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

## Common Configurations

### 3 Times Daily (Default)
```bash
python config_manager.py set-schedule "08:00, 12:00, 15:00"
```

### Every 4 Hours (6 times)
```bash
python config_manager.py set-schedule "00:00, 04:00, 08:00, 12:00, 16:00, 20:00"
```

### Business Hours Only (5 times)
```bash
python config_manager.py set-schedule "08:00, 10:00, 12:00, 14:00, 16:00"
```

### Once Daily
```bash
python config_manager.py set-schedule "09:00"
```

### Morning & Evening
```bash
python config_manager.py set-schedule "07:00, 19:00"
```

## Common Role Sets

### Security/Compliance Focus
```bash
python config_manager.py set-roles "security engineer, compliance officer, CISO, GRC analyst, DPO, security architect"
```

### DevOps/Infrastructure Focus
```bash
python config_manager.py set-roles "DevOps engineer, cloud architect, SRE, infrastructure engineer, platform engineer"
```

### Privacy Focus
```bash
python config_manager.py set-roles "privacy officer, DPO, privacy engineer, data governance specialist"
```

### Full Stack Development
```bash
python config_manager.py set-roles "full stack engineer, backend engineer, frontend engineer, DevOps engineer"
```

## Timezones (Quick Reference)

| Region | Timezone |
|--------|----------|
| Eastern US | `America/New_York` |
| Central US | `America/Chicago` |
| Mountain US | `America/Denver` |
| Pacific US | `America/Los_Angeles` |
| UK/GMT | `Europe/London` |
| Central Europe | `Europe/Paris` |
| Japan | `Asia/Tokyo` |
| Australia | `Australia/Sydney` |
| UTC | `UTC` |

Set timezone with:
```bash
# Edit .env
TIMEZONE=America/Los_Angeles
```

Full timezone list: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

## Workflow Examples

### Setup New Role Search

```bash
# 1. View current config
python config_manager.py show

# 2. Set new roles
python config_manager.py set-roles "blockchain engineer, web3 developer, smart contract engineer"

# 3. Adjust schedule if needed
python config_manager.py set-schedule "08:00, 16:00"

# 4. Verify
python config_manager.py show

# 5. Start scheduler
python scheduler.py
```

### Use Community Configuration

```bash
# 1. Import
python config_manager.py import config-examples/devops-infrastructure-focus.json

# 2. Customize if needed
python config_manager.py add-role "Kubernetes engineer"

# 3. Save your version
python config_manager.py export my-devops-config.json

# 4. Run
python scheduler.py
```

### Backup & Restore

```bash
# Backup before making changes
python config_manager.py export backup-$(date +%Y%m%d).json

# Make changes
python config_manager.py set-roles "new role 1, new role 2"

# Restore if needed
python config_manager.py import backup-20260119.json
```

## Time Format Guide

All times use 24-hour format: `HH:MM`

| Time | Format |
|------|--------|
| 8:00 AM | `08:00` |
| 12:00 PM (Noon) | `12:00` |
| 3:00 PM | `15:00` |
| 6:00 PM | `18:00` |
| 9:00 PM | `21:00` |
| Midnight | `00:00` |

## Help & Documentation

```bash
# Show all available commands
python config_manager.py -h

# Detailed configuration guide
cat CONFIGURATION.md

# Pre-built configurations
cat config-examples/README.md

# See all enhancements
cat ENHANCEMENTS.md
```

## Troubleshooting

**Q: Changes not taking effect?**
```bash
# Verify config was loaded
python config_manager.py show

# Restart scheduler (if running)
# Ctrl+C then: python scheduler.py
```

**Q: Invalid time error?**
Use 24-hour format: `08:00` not `8:00` or `8 AM`

**Q: Can't find config-examples?**
```bash
ls -la config-examples/
# or
cd /mnt/d/roleradar/config-examples
```

**Q: Reset to defaults?**
```bash
python config_manager.py import config-examples/security-compliance-focus.json
```
