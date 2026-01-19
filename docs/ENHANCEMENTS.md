# RoleRadar Enhancements Summary

## What's New

RoleRadar has been enhanced to support **configurable roles** and **flexible scheduling**, making it suitable for community-wide use and customizable searches.

## Key Enhancements

### 1. **Configurable Search Roles** 🎯
Search for ANY job title, not just security roles. The application now supports:
- Custom role configuration
- Runtime updates without restarts
- Automatic query generation from roles
- Community-shared configurations

### 2. **Flexible Scheduling** ⏰
Multiple search times per day with full timezone support:
- Default: 8 AM, 12 PM, 3 PM EST
- Customizable to any number of times
- Full timezone support (IANA format)
- Examples: every 4 hours, business hours only, continuous 24/7

### 3. **Configuration Management** ⚙️
Three ways to manage configuration:

#### Option A: Environment Variables (.env)
```bash
TIMEZONE=America/New_York
SEARCH_ROLES=["security engineer", "compliance officer", "CISO"]
SCHEDULE_TIMES=["08:00", "12:00", "15:00"]
```

#### Option B: CLI Configuration Manager
```bash
python config_manager.py show
python config_manager.py set-roles "DevOps engineer, cloud architect"
python config_manager.py set-schedule "06:00, 14:00, 22:00"
python config_manager.py add-role "SRE"
python config_manager.py remove-time "12:00"
```

#### Option C: JSON Files (Import/Export)
```bash
python config_manager.py export my-config.json
python config_manager.py import my-config.json
```

### 4. **Community Configuration Library** 📚
Pre-built configurations for common use cases:
- Security & Compliance Focus
- DevOps & Infrastructure Focus
- Privacy & Data Protection Focus
- 24/7 Continuous Monitoring
- Startup Hiring Signals

Located in: `config-examples/`

## Files Modified/Created

### Modified Files
1. **src/roleradar/config.py**
   - Added support for role configuration
   - Added support for schedule time configuration
   - Added timezone support
   - Added methods to update configuration at runtime

2. **scheduler.py**
   - Enhanced to support multiple scheduled times
   - Better logging and status displays
   - Displays next scheduled runs

3. **.env**
   - Added configuration examples
   - Documented all new options

4. **README.md**
   - Updated with configuration references
   - Added quick examples
   - Added community sharing information

### New Files
1. **config_manager.py** (CLI tool)
   - View current configuration
   - Add/remove/update roles
   - Add/remove/update schedule times
   - Import/export JSON configurations

2. **CONFIGURATION.md** (Documentation)
   - Comprehensive configuration guide
   - Quick start examples
   - Advanced configuration patterns
   - Timezone reference
   - Troubleshooting guide

3. **config-examples/** (Community library)
   - 5 pre-built configurations
   - README with usage instructions
   - Template for creating custom configs

## Usage Examples

### Basic Setup
```bash
# View current configuration
python config_manager.py show

# Search for different roles
python config_manager.py set-roles "DevOps engineer, SRE, cloud architect"

# Search 5 times per day
python config_manager.py set-schedule "07:00, 10:00, 13:00, 16:00, 19:00"
```

### Import Community Config
```bash
# Use pre-built security config
python config_manager.py import config-examples/security-compliance-focus.json

# Use DevOps config
python config_manager.py import config-examples/devops-infrastructure-focus.json
```

### Run Scheduler
```bash
# Scheduler now uses configured roles and schedule times
python scheduler.py
```

Output:
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

Next scheduled runs:
  → 2026-01-19 08:00:00
  → 2026-01-19 12:00:00
  → 2026-01-19 15:00:00
```

## Technical Details

### Configuration Inheritance
1. **Default config** → Built-in defaults
2. **Environment variables** → Override defaults
3. **Runtime updates** → Override environment variables
4. **JSON import** → Replace entire configuration

### Timezone Handling
- Uses IANA timezone database format
- Automatically converts times to scheduler's local time
- Supports all standard timezones (UTC, EST, PST, GMT, CET, etc.)

### Search Query Generation
Queries are automatically generated from roles:
- Input: `["security engineer", "CISO"]`
- Generated queries:
  - "security engineer job openings"
  - "security engineer hiring"
  - "CISO job openings"
  - "CISO hiring"

## Backward Compatibility

All enhancements are **fully backward compatible**:
- Existing .env files continue to work
- Default behavior unchanged if not customized
- Old scripts and integrations still work

## Next Steps

### For Users
1. Review current configuration: `python config_manager.py show`
2. Try a pre-built configuration: `python config_manager.py import config-examples/[name].json`
3. Customize as needed using CLI or .env
4. Run scheduler with new configuration

### For Community
1. Create specialized configurations for your use case
2. Export and share: `python config_manager.py export my-config.json`
3. Contribute back to `config-examples/`
4. Help others by documenting your configuration

### For Development
1. Configuration is modular and easy to extend
2. New configuration options can be added to `config.py`
3. See [CONFIGURATION.md](CONFIGURATION.md) for API usage examples

## Documentation

- **Quick Start:** See README.md "Configuration" section
- **Detailed Guide:** See [CONFIGURATION.md](CONFIGURATION.md)
- **Examples:** See [config-examples/README.md](config-examples/README.md)
- **CLI Help:** `python config_manager.py -h`

## Questions?

Refer to:
1. CONFIGURATION.md - Detailed documentation
2. config-examples/README.md - Pre-built configs and tips
3. config_manager.py -h - CLI help
4. Run: `python config_manager.py show` - Check current state
