# RoleRadar Configuration Examples

This directory contains pre-configured setup files for various use cases and industries. You can use these as starting points for your own RoleRadar configuration.

## Available Configurations

### 1. Security & Compliance Focus (Default)
**File:** `security-compliance-focus.json`

Optimized for security and compliance professionals. Searches for:
- Security Engineers
- Compliance Officers
- GRC Analysts
- CISOs
- Data Protection Officers
- Security Architects
- InfoSec Directors

**Schedule:** 3 times daily (8 AM, 12 PM, 3 PM EST)

**Best for:** Security practitioners, GRC professionals, compliance officers

### 2. DevOps & Infrastructure Focus
**File:** `devops-infrastructure-focus.json`

Focused on infrastructure, DevOps, and cloud roles:
- DevOps Engineers
- Cloud Architects
- SREs
- Infrastructure Engineers
- Platform Engineers
- Kubernetes Engineers

**Schedule:** 4 times daily (6 AM, 10 AM, 2 PM, 6 PM EST)

**Best for:** DevOps engineers, infrastructure teams, platform teams

### 3. Privacy & Data Protection Focus
**File:** `privacy-data-protection-focus.json`

Specialized for privacy and data governance:
- Privacy Officers
- Data Protection Officers (DPOs)
- Privacy Engineers
- Data Governance Specialists
- Compliance Officers

**Schedule:** 2 times daily (8 AM, 2 PM GMT)
**Timezone:** Europe/London (good for EU-based roles)

**Best for:** Privacy professionals, GDPR specialists, data governance teams

### 4. 24/7 Continuous Monitoring
**File:** `continuous-monitoring-24h.json`

For organizations needing round-the-clock monitoring:
- Searches every 4 hours (6 searches daily)
- Covers all time zones
- UTC timezone (easily convertible)

**Schedule:** Every 4 hours (00:00, 04:00, 08:00, 12:00, 16:00, 20:00 UTC)

**Best for:** Global organizations, research teams, automated tracking

### 5. Startup Hiring Signals
**File:** `startup-hiring-signals.json`

Focused on identifying startup growth and hiring patterns:
- Full Stack Engineers
- Backend Engineers
- DevOps Engineers
- Security Engineers
- Product Managers
- Engineering Managers

**Schedule:** 2 times daily (8 AM, 5 PM PST)
**Timezone:** America/Los_Angeles

**Best for:** Investor relations, startup researchers, venture capital teams

## How to Use

### Import a Configuration

```bash
# Use the Security & Compliance configuration
python config_manager.py import config-examples/security-compliance-focus.json

# Use the DevOps configuration
python config_manager.py import config-examples/devops-infrastructure-focus.json

# Use the Privacy-focused configuration
python config_manager.py import config-examples/privacy-data-protection-focus.json

# Use 24/7 monitoring
python config_manager.py import config-examples/continuous-monitoring-24h.json

# Use startup hiring signals
python config_manager.py import config-examples/startup-hiring-signals.json
```

### Customize a Configuration

1. Import one of these configurations:
   ```bash
   python config_manager.py import config-examples/security-compliance-focus.json
   ```

2. Make adjustments:
   ```bash
   # Add a role
   python config_manager.py add-role "privacy engineer"
   
   # Add a schedule time
   python config_manager.py add-time "21:00"
   
   # View current config
   python config_manager.py show
   ```

3. Export your custom configuration:
   ```bash
   python config_manager.py export config-examples/my-custom-focus.json
   ```

## Creating Your Own Configuration

Create a new JSON file in this directory following this template:

```json
{
  "name": "My Custom Focus",
  "description": "Description of what this configuration is for",
  "timezone": "America/New_York",
  "search_roles": [
    "role 1",
    "role 2",
    "role 3"
  ],
  "schedule_times": [
    "08:00",
    "12:00",
    "15:00"
  ]
}
```

### Notes for Custom Configurations

- **Timezone:** Use IANA timezone format (see [Timezone Reference](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones))
- **Schedule Times:** Use 24-hour format (HH:MM)
- **Search Roles:** Be specific with job titles - more specific = better results
- **Optional Fields:** `name` and `description` are optional but recommended for sharing

## Community Sharing

Have a great configuration? Share it with the community!

1. Create your configuration file
2. Submit a pull request to add it to this directory
3. Include a clear description of what it's for

## Tips for Effective Configurations

### Role Selection
- **Be specific:** "Security Engineer" is better than "Security"
- **Include variations:** "DevOps Engineer", "DevOps", "DevOps Manager"
- **Consider level:** Mix junior, mid-level, and senior roles if desired
- **Industry-specific:** "InfoSec Director", "CISO" vs "Security Manager"

### Schedule Selection
- **Business hours focus:** 08:00, 10:00, 12:00, 14:00, 16:00
- **Multiple time zones:** Use UTC and run 4 times daily (00:00, 06:00, 12:00, 18:00)
- **Morning alerts only:** 06:00, 09:00, 12:00
- **Minimal overhead:** Single 09:00 run (good for testing)

### Timezone Selection
- For most US users: `America/New_York` (ET)
- For EU users: `Europe/London` (GMT/BST) or `Europe/Paris` (CET/CEST)
- For global users: `UTC`
- For specific timezones: See full [timezone list](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

## Troubleshooting

### Configuration not loading?
- Ensure the JSON is valid (no trailing commas, quotes match)
- Check that `schedule_times` are in 24-hour format
- Verify timezone is valid (use IANA format)

### Searches running at wrong time?
- Verify your `TIMEZONE` environment variable
- Check system time is correct
- Run `python config_manager.py show` to verify loaded config

### Getting too many results?
- Reduce number of roles or be more specific with titles
- Reduce schedule frequency (fewer times per day)
- Filter by more specific keywords

### Getting too few results?
- Add more roles
- Use broader role titles
- Increase schedule frequency
- Check API rate limits with Tavily
