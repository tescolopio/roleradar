# RoleRadar Admin GUI - Quick Start

## Accessing the Admin Dashboard

Once RoleRadar is running, access the admin panel here:

```
http://localhost:5000/admin
```

Or from your main dashboard: Click the **⚙️ Admin Panel** button in the top right.

## What You Can Do

### 🔍 Search Control
- **Run Search Now**: Execute immediate search across all configured roles
- **Custom Search**: Search for specific job titles or queries
- **Process Results**: Process unprocessed results through AI analysis

### ⚙️ Configuration
- Add or remove job roles to search for
- See how many roles are currently configured
- Save changes with one click

### 📅 Schedule
- Set up to 4+ automated search times per day
- Use 24-hour format (e.g., 08:00, 14:30)
- Automatically enforced by the scheduler

### 💬 Prompts
- Customize the AI prompts used for data extraction
- Control how entities, signals, and growth are detected
- Changes apply to new processing jobs

### ⚖️ Weights
- Adjust how different factors score opportunities
- Control balance between job postings, growth signals, and activity
- Real-time validation (must sum to 100%)

### 🔧 System
- View current database type
- Check if secure configuration is enabled
- See number of active roles and schedules

## Quick Setup Example

1. Start dashboard: `python roleradar.py dashboard`
2. Open browser: `http://localhost:5000`
3. Click **⚙️ Admin Panel**
4. Go to **⚙️ Configuration** tab
5. Add roles like:
   - CISO
   - Security Director
   - Compliance Officer
   - GRC Analyst
6. Click **💾 Save Roles**
7. Go to **📅 Schedule** tab
8. Add times: 08:00, 14:00, 18:00
9. Click **💾 Save Schedule**
10. Try **🔍 Search Control** → **Run Search Now** to test

## Key Features

✅ **No Code Required** - Pure web interface
✅ **Real-time Validation** - Immediate feedback on configuration
✅ **Safe Changes** - All changes validated server-side
✅ **Status Indicators** - See system health and configuration status
✅ **Responsive Design** - Works on desktop and tablet
✅ **Persistent Storage** - All changes saved to encrypted config

## Common Tasks

### Add a New Role to Search

1. Go to **⚙️ Configuration**
2. Type role name in the input field
3. Click **+ Add Role**
4. Click **💾 Save Roles**

### Change Search Schedule

1. Go to **📅 Schedule**
2. Remove times: Click ✕ on any time
3. Add times: Select time and click **+ Add Time**
4. Click **💾 Save Schedule**

### Increase Job Posting Weight

1. Go to **⚖️ Weights**
2. Drag "Explicit Job Posting" slider right
3. Adjust others to keep total at 100%
4. Click **💾 Save Weights**

### Customize AI Prompts

1. Go to **💬 Prompts**
2. Edit the text in any prompt textarea
3. Click **💾 Save Prompts**
4. Prompts apply to new processing jobs

### Run a Manual Search

1. Go to **🔍 Search Control**
2. For custom search:
   - Type role name in search field
   - Click **🔎 Search**
3. For full search:
   - Click **▶️ Start Search Now**
4. Results shown immediately

## API Endpoints (Advanced)

All admin functions are backed by REST APIs:

```bash
# Get configuration
curl http://localhost:5000/api/config/search-roles
curl http://localhost:5000/api/config/schedule
curl http://localhost:5000/api/config/weights

# Update configuration
curl -X PUT http://localhost:5000/api/config/search-roles \
  -H "Content-Type: application/json" \
  -d '{"roles": ["CISO", "Security Director"]}'

# Trigger search
curl -X POST http://localhost:5000/api/search/manual
curl -X POST http://localhost:5000/api/search/process

# System status
curl http://localhost:5000/api/system/status
curl http://localhost:5000/api/system/health
```

## Troubleshooting

**Changes not saving?**
- Check that database is accessible
- Verify network connection
- Check browser console for errors (F12)

**Search returns no results?**
- Verify API keys are configured (Tavily, Groq)
- Check role names are spelled correctly
- Try manual search first to test

**Prompts not applying?**
- Saved prompts apply to NEW processing jobs
- Existing data isn't re-processed
- Run "Process Results" to apply to new data

**Port already in use?**
- Dashboard auto-detects and uses alternate port
- Check console output for actual port (usually 5000-5019)

## Next Steps

After initial setup:

1. **Monitor Results**: Check dashboard for discovered opportunities
2. **Refine Roles**: Add/remove roles based on your specific focus
3. **Adjust Schedule**: Find optimal timing for your workflow
4. **Customize Prompts**: Fine-tune AI extraction based on results
5. **Tune Weights**: Adjust scoring to match your priorities

## More Information

- Full guide: See `ADMIN_GUI_GUIDE.md`
- Configuration help: See `CONFIGURATION.md`
- System resilience: See `RESILIENCE_IMPROVEMENTS.md`
- Dashboard usage: See `QUICK_START.md`

---

**Ready?** Start the dashboard and click **⚙️ Admin Panel** to begin! 🚀
