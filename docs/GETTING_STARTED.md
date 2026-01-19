# RoleRadar Getting Started Guide

## What's New?

RoleRadar now supports:
- **Configurable roles** - Search for any job title (not just security!)
- **Flexible scheduling** - Run searches multiple times per day at custom times
- **Easy management** - Simple CLI tool to configure everything
- **Community sharing** - Import/export configurations as JSON

## 30-Second Quick Start

```bash
# 1. Check what's currently configured
python config_manager.py show

# 2. (Optional) Try a pre-built configuration
python config_manager.py import config-examples/devops-infrastructure-focus.json

# 3. Run the scheduler (uses your configured roles & times)
python scheduler.py
```

Done! The scheduler will now search at your configured times using your configured roles.

## First Time Setup

### Step 1: View Default Configuration

```bash
python config_manager.py show
```

This shows:
- Default roles: 8 security/compliance positions
- Default schedule: 8 AM, 12 PM, 3 PM EST
- Timezone: America/New_York
- Total search queries: 16

### Step 2: Customize (Optional)

Want to search for different roles?

```bash
# Search for DevOps instead
python config_manager.py set-roles "DevOps engineer, SRE, cloud architect"
```

Want different times?

```bash
# Search every 6 hours (4 times daily)
python config_manager.py set-schedule "06:00, 12:00, 18:00, 00:00"
```

### Step 3: Run Scheduler

```bash
python scheduler.py
```

The scheduler will:
1. Display your configuration
2. Run a search immediately
3. Continue running at your scheduled times
4. Process and analyze all results

## Common Tasks

### See What's Configured

```bash
python config_manager.py show
```

### Search for Different Roles

```bash
# Replace all roles
python config_manager.py set-roles "role1, role2, role3"

# Or add/remove individual roles
python config_manager.py add-role "privacy officer"
python config_manager.py remove-role "security architect"
```

### Change Search Times

```bash
# Replace schedule
python config_manager.py set-schedule "08:00, 16:00"

# Or add/remove individual times
python config_manager.py add-time "18:00"
python config_manager.py remove-time "12:00"
```

### Use a Pre-Built Configuration

```bash
# DevOps focus (4x daily)
python config_manager.py import config-examples/devops-infrastructure-focus.json

# Privacy focus (2x daily, Europe timezone)
python config_manager.py import config-examples/privacy-data-protection-focus.json

# 24/7 monitoring (every 4 hours, UTC)
python config_manager.py import config-examples/continuous-monitoring-24h.json

# Default security focus
python config_manager.py import config-examples/security-compliance-focus.json

# Startup tech roles
python config_manager.py import config-examples/startup-hiring-signals.json
```

### Save Your Configuration

```bash
# Backup before making changes
python config_manager.py export my-config-backup.json

# Share with others
python config_manager.py export my-custom-setup.json
```

## Configuration Examples

### 3 Times Daily (Default)
```bash
python config_manager.py set-schedule "08:00, 12:00, 15:00"
```

### Every 4 Hours (24/7 Monitoring)
```bash
python config_manager.py set-schedule "00:00, 04:00, 08:00, 12:00, 16:00, 20:00"
```

### Business Hours Only
```bash
python config_manager.py set-schedule "08:00, 10:00, 12:00, 14:00, 16:00"
```

### Morning Alert
```bash
python config_manager.py set-schedule "08:00"
```

## Example: Setup for DevOps Team

```bash
# 1. Set DevOps roles
python config_manager.py set-roles "DevOps engineer, SRE, cloud architect, infrastructure engineer, platform engineer, Kubernetes engineer"

# 2. Set times (4x daily, start early)
python config_manager.py set-schedule "06:00, 10:00, 14:00, 18:00"

# 3. Verify
python config_manager.py show

# 4. Run
python scheduler.py

# 5. Save for later
python config_manager.py export devops-team-config.json
```

## Example: Setup for Privacy Team

```bash
# 1. Set privacy roles
python config_manager.py set-roles "privacy officer, DPO, privacy engineer, data governance specialist, compliance officer"

# 2. Set times (morning and afternoon)
python config_manager.py set-schedule "08:00, 14:00"

# 3. Set Europe timezone
# Edit .env and add: TIMEZONE=Europe/London

# 4. Verify and run
python config_manager.py show
python scheduler.py
```

## Environment Variables

For advanced users, you can also configure via `.env` file:

```bash
# Edit .env
TIMEZONE=America/New_York
SEARCH_ROLES=["security engineer", "CISO", "compliance officer"]
SCHEDULE_TIMES=["08:00", "12:00", "15:00"]
```

Then reload:
```bash
# Restart scheduler (Ctrl+C then run again)
python scheduler.py
```

## Help & More Info

```bash
# CLI help
python config_manager.py -h

# Detailed configuration guide
cat CONFIGURATION.md

# Quick reference
cat QUICK_REFERENCE.md

# Feature overview
cat ENHANCEMENTS.md

# Community configurations
ls config-examples/
cat config-examples/README.md
```

## Troubleshooting

### Configuration not showing?
```bash
python config_manager.py show
```

### Want to reset to defaults?
```bash
python config_manager.py import config-examples/security-compliance-focus.json
```

### Changes not taking effect?
Restart the scheduler:
- Press Ctrl+C to stop
- Run `python scheduler.py` again

### Invalid time error?
Use 24-hour format:
- ✓ Correct: `08:00`, `12:00`, `15:00`, `18:00`
- ✗ Wrong: `8:00`, `12:00 PM`, `3 PM`

## Key Directories

```
roleradar/
├── config_manager.py          ← Configuration CLI tool
├── scheduler.py               ← Run this to start searches
├── CONFIGURATION.md           ← Detailed guide
├── QUICK_REFERENCE.md         ← Command reference
├── config-examples/           ← Pre-built configurations
│   ├── security-compliance-focus.json
│   ├── devops-infrastructure-focus.json
│   ├── privacy-data-protection-focus.json
│   ├── continuous-monitoring-24h.json
│   └── startup-hiring-signals.json
└── src/roleradar/
    └── config.py              ← Where config is loaded from
```

## Next Steps

1. ✅ View current config: `python config_manager.py show`
2. ✅ Choose a configuration style (or use default)
3. ✅ Customize if needed: `python config_manager.py set-...`
4. ✅ Start scheduler: `python scheduler.py`
5. ✅ (Optional) Share your config: `python config_manager.py export my-config.json`

That's it! You're ready to go!

## Questions?

- **"How do I customize roles?"** → See CONFIGURATION.md
- **"What timezones are supported?"** → See QUICK_REFERENCE.md
- **"How do I share my config?"** → See ENHANCEMENTS.md
- **"What are the pre-built configs?"** → See config-examples/README.md

Happy searching! 🎯
