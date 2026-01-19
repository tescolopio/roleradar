# RoleRadar Admin Management GUI

## Overview

The RoleRadar Admin Management Dashboard provides a comprehensive web-based interface for managing search parameters, controlling manual and automated searches, and adjusting AI extraction prompts and scoring algorithms. Access it at `/admin` when the dashboard is running.

## Features

### 1. 🔍 Search Control

#### Manual Search
- **Run Search Now**: Execute a complete search across all configured roles immediately
- **Custom Query Search**: Search for a specific role, job title, or custom query
- **Process Results**: Process unprocessed search results through AI extraction and analysis

**Use Cases:**
- Test new search queries before automating them
- Manually trigger searches outside scheduled times
- Process backlog of unprocessed search results

### 2. ⚙️ Search Roles Configuration

Manage the job roles that are automatically searched for in job postings.

**Features:**
- Add new roles to search for
- Remove existing roles
- Save changes with a single click
- Reset to original configuration

**Recommended Roles:**
- CISO (Chief Information Security Officer)
- Security Director
- Security Architect
- Compliance Officer
- Compliance Director
- GRC Analyst
- Data Protection Officer (DPO)
- InfoSec Manager

**Tips:**
- Use specific, descriptive titles for better search accuracy
- Add both singular and plural variations if needed
- More specific roles yield higher quality matches

### 3. 📅 Automated Search Schedule

Configure when automated searches should run each day.

**Features:**
- Set multiple schedule times in 24-hour format (HH:MM)
- Times are sorted automatically
- Clear scheduling interface
- Save and reset options

**Recommended Schedule:**
- 08:00 (Morning)
- 12:00 (Noon)
- 15:00 (Mid-afternoon)
- 18:00 (Evening)

**Tips:**
- Space searches 3-4 hours apart for optimal coverage
- Timezone is configured in environment: `TIMEZONE` setting
- Changes take effect immediately for manual searches
- Automated scheduler respects the configured times

### 4. 💬 Data Extraction Prompts

Customize the AI prompts used to extract and analyze data from search results.

**Prompt Types:**

**Entity Extraction Prompt**
- Extracts: Company names, job titles, locations, keywords
- Used for: Initial data structuring from search results
- Default behavior: Standard entity recognition

**Hiring Signals Prompt**
- Detects: Expansion indicators, team growth, new positions
- Used for: Identifying companies likely to be hiring
- Default behavior: Pattern recognition for growth signals

**Growth Detection Prompt**
- Analyzes: Company growth patterns, market moves, funding
- Used for: Assessing company trajectory and opportunities
- Default behavior: News and activity analysis

**Tips:**
- Be specific about desired output format
- Include examples for better results
- Changes apply to newly processed results
- Test with small batches before wide deployment

### 5. ⚖️ Scoring Weights

Adjust how different factors contribute to opportunity scoring.

**Weight Components:**

| Component | Default | Purpose |
|-----------|---------|---------|
| Explicit Job Posting | 40% | Direct job opening discovery |
| Hiring Signals | 30% | Growth and expansion indicators |
| Company Growth | 20% | Long-term company trajectory |
| Recent Activity | 10% | Fresh data and recency |

**How to Adjust:**
1. Use the sliders to adjust each weight
2. Weights must sum to 100% (100.0)
3. Indicator shows green when valid, amber when invalid
4. Save changes when ready

**Example Scenarios:**

- **Conservative (Low False Positives)**: 50% Explicit, 30% Signals, 15% Growth, 5% Activity
- **Aggressive (Maximum Coverage)**: 30% Explicit, 40% Signals, 20% Growth, 10% Activity
- **Recent Focus**: 35% Explicit, 30% Signals, 15% Growth, 20% Activity

### 6. 🔧 System Status

Real-time view of system configuration and status.

**Status Indicators:**
- Database: Connection status and type
- Configuration Mode: Secure (encrypted) or Environment (.env)
- Active Roles: Number of currently configured search roles
- Scheduled Times: Number of automated search times

**Health Check:**
- Visit `/api/system/health` for system health status
- Includes version and available features

## API Endpoints

All admin operations are backed by RESTful APIs:

### Configuration APIs

```
GET  /api/config/search-roles          - Get current search roles
PUT  /api/config/search-roles          - Update search roles
GET  /api/config/schedule              - Get schedule times
PUT  /api/config/schedule              - Update schedule times
GET  /api/config/weights               - Get scoring weights
PUT  /api/config/weights               - Update weights
GET  /api/config/extraction-prompts    - Get AI prompts
PUT  /api/config/extraction-prompts    - Update AI prompts
```

### Search Control APIs

```
POST /api/search/manual                - Trigger search
POST /api/search/process               - Process results
GET  /api/search/status                - Get search status
```

### System APIs

```
GET  /api/system/status                - System status
GET  /api/system/health                - Health check
```

## Workflow Examples

### Example 1: Add a New Role to Search

1. Navigate to **⚙️ Configuration**
2. Enter role name in "Enter new role" field (e.g., "Risk Manager")
3. Click "+ Add Role"
4. Click "💾 Save Roles"
5. Confirmation message appears
6. Role is now included in all future searches

### Example 2: Adjust Schedule to Business Hours

1. Navigate to **📅 Schedule**
2. Remove times outside business hours
3. Add times (e.g., 08:30, 14:00, 17:30)
4. Verify times are in HH:MM format
5. Click "💾 Save Schedule"
6. Changes take effect immediately

### Example 3: Optimize Scoring for High Quality

1. Navigate to **⚖️ Weights**
2. Increase "Explicit Job Posting" to 50%
3. Decrease "Recent Activity" to 5%
4. Verify total is 100%
5. Click "💾 Save Weights"
6. Scoring applied to new opportunities

### Example 4: Customize AI Extraction

1. Navigate to **💬 Prompts**
2. Modify "Entity Extraction Prompt" with specific requirements
3. Add examples or specific formatting requirements
4. Click "💾 Save Prompts"
5. New changes apply to future processing jobs

## Best Practices

### Search Configuration
- ✅ Use specific job titles rather than generic terms
- ✅ Include variations (e.g., "CISO", "Chief Information Security Officer")
- ✅ Review periodically and add emerging roles
- ❌ Avoid single-word terms that may have low specificity

### Scheduling
- ✅ Schedule during business hours for your target companies
- ✅ Space searches evenly throughout the day
- ✅ Monitor search quality and adjust schedule if needed
- ❌ Don't schedule too frequently (hourly searches may hit rate limits)

### Scoring Weights
- ✅ Start with defaults and adjust based on your priorities
- ✅ Test changes on smaller datasets before full deployment
- ✅ Balance between job postings and growth signals
- ❌ Don't over-weight recent activity (can miss important patterns)

### Prompts
- ✅ Keep prompts clear and specific
- ✅ Include examples of desired output
- ✅ Test on sample results before saving
- ✅ Version your prompts with comments if making major changes
- ❌ Don't use overly complex or ambiguous instructions

## Troubleshooting

### Issue: Changes Not Saving
**Solution:** Ensure database is accessible and configuration is not read-only. Check system status for database status.

### Issue: Search Returning No Results
**Solution:** 
1. Check role names are spelled correctly
2. Try "Run Search Now" manually to test
3. Check if API keys (Tavily, Groq) are configured

### Issue: Weights Always Show Invalid
**Solution:** Ensure weights sum exactly to 1.0. Use the slider tool to verify calculations.

### Issue: Custom Prompts Not Applied
**Solution:** 
1. Confirm prompts saved successfully (green status message)
2. Run "Process Results" to apply to unprocessed data
3. Note: Prompts only apply to new processing, not existing data

## Security Considerations

- Admin panel is accessible at `/admin` - consider securing with authentication if exposed
- Configuration changes are persisted in secure encrypted storage
- API keys are never displayed in admin interface
- All configuration is validated server-side before saving

## Advanced Configuration

### Via Environment Variables (Legacy)

```bash
SEARCH_ROLES='["CISO", "Security Director"]'
SCHEDULE_TIMES='["08:00", "12:00", "18:00"]'
TIMEZONE='America/New_York'
```

### Via Secure Config

```bash
python secure_config_manager.py set-key SEARCH_ROLES '["CISO", "Security Director"]'
```

## Next Steps

1. **Initialize Configuration**: Run `python secure_config_manager.py init` for encrypted storage
2. **Access Admin Panel**: Navigate to `/admin` on your running dashboard
3. **Configure Roles**: Add the security/compliance roles relevant to your search
4. **Test Search**: Use "Run Search Now" to verify configuration works
5. **Set Schedule**: Configure automated search times
6. **Monitor Results**: Check dashboard for discovered opportunities

## Support

For issues or questions:
1. Check `/api/system/health` endpoint
2. Review logs for error messages
3. Verify database connectivity
4. Ensure API keys are properly configured
