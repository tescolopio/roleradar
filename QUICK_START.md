# RoleRadar - Quick Start Guide

## Prerequisites

1. **Install Dependencies**
```bash
cd /mnt/d/roleradar
pip install -r requirements.txt
```

2. **Set Up Secure Configuration** (Recommended)
```bash
python secure_config_manager.py init
# You'll be prompted for:
# - Master password (minimum 8 characters)
# - Tavily API Key
# - Groq API Key
# - Database credentials (optional)
```

Or **migrate from .env** (if upgrading):
```bash
python secure_config_manager.py migrate
```

## Starting RoleRadar

### Option 1: Web Dashboard Only (Quick Start)

```bash
# Start the web dashboard
python roleradar.py dashboard
```

Then open your browser to: **http://localhost:5000**

**Features:**
- ✅ Automatically detects unavailable PostgreSQL and falls back to SQLite
- ✅ Automatically finds available port if 5000 is in use
- ✅ Full functionality with local database

### Option 2: One-Time Search + Dashboard

```bash
# Initialize database (first time only)
python roleradar.py init

# Run one search
python roleradar.py search

# Process results with AI analysis
python roleradar.py process

# Launch dashboard
python roleradar.py dashboard
```

Then open: **http://localhost:5000**

### Option 3: Automated Scheduler (Production)

```bash
# Start background scheduler (runs searches at configured times)
python scheduler.py
```

This will:
- Run searches at configured times (default: 8 AM, 12 PM, 3 PM EST)
- Automatically process results
- Store in database
- You can still access dashboard at **http://localhost:5000**

## Accessing the Application

### Web Dashboard
- **URL:** http://localhost:5000
- **Features:**
  - View top companies by score
  - Active job opportunities
  - Hiring signals and trends
  - Executive summaries

### Command Line

**View current configuration:**
```bash
python secure_config_manager.py show
```

**View database statistics:**
```bash
python roleradar.py stats
```

**Search for opportunities manually:**
```bash
python roleradar.py search
```

**Process results with AI:**
```bash
python roleradar.py process
```

## Complete Workflow Example

```bash
# Step 1: Set up secure configuration
python secure_config_manager.py init

# Step 2: Initialize database
python roleradar.py init

# Step 3: Run initial search and processing
python roleradar.py search
python roleradar.py process

# Step 4: View results in dashboard
python roleradar.py dashboard
# Open http://localhost:5000 in your browser

# Step 5: Set up automated searches (optional)
# In another terminal:
python scheduler.py
```

## Configuration Management

### View Current Settings
```bash
python secure_config_manager.py show
```

### Update Search Roles
```bash
python secure_config_manager.py set-roles "security engineer, CISO, compliance officer"
```

### Update Schedule Times
```bash
python secure_config_manager.py set-schedule "08:00, 12:00, 16:00, 20:00"
```

### Update API Keys
```bash
python secure_config_manager.py set-key TAVILY_API_KEY
python secure_config_manager.py set-key GROQ_API_KEY
```

## Port Configuration

By default, RoleRadar uses:
- **Port 5000** for the web dashboard
- Can be configured via environment variable: `FLASK_PORT=8000`

To run on a different port:
```bash
FLASK_PORT=8000 python roleradar.py dashboard
# Then access: http://localhost:8000
```

## Troubleshooting

### Database Connection Issues

**Problem:** PostgreSQL not running
```
⚠️  PostgreSQL connection failed...
📦 Falling back to SQLite for local development
```

**Solution:** ✅ Automatic! The system automatically falls back to SQLite.
- No PostgreSQL needed for local development
- Data stored in `roleradar.db`
- Full functionality preserved

To use PostgreSQL later:
```bash
# Update database URL in secure config
python secure_config_manager.py set-key DATABASE_URL "postgresql://user:pass@host:5433/roleradar"
```

### Port Already in Use

**Problem:** Port 5000 already in use
```
⚠️  Port 5000 is in use
🔄 Using available port 5001 instead
```

**Solution:** ✅ Automatic! The system finds the next available port.
- Checks ports 5000-5019
- Uses first available port found
- No manual configuration needed

To use a specific port:
```bash
FLASK_PORT=8000 python roleradar.py dashboard
```

## Advanced Usage

### Custom Timezone
```bash
python secure_config_manager.py set-key TIMEZONE "America/Chicago"
```

### Database Management
```bash
# View statistics
python roleradar.py stats

# Export data (check documentation)
python roleradar.py export
```

### Scheduler Commands
```bash
# Run scheduler with custom configuration
python scheduler.py

# The scheduler runs at configured times and:
# - Searches for opportunities
# - Processes results with AI
# - Stores in database
# - Updates dashboard
```

## Documentation Links

- **Quick Reference:** [SECURE_CONFIG_QUICK_REFERENCE.md](SECURE_CONFIG_QUICK_REFERENCE.md)
- **Security Setup:** [SECURE_CONFIGURATION.md](SECURE_CONFIGURATION.md)
- **Configuration:** [CONFIGURATION.md](CONFIGURATION.md)
- **Full Guide:** [README.md](README.md)

## Quick Commands Summary

```bash
# Setup & Config
python secure_config_manager.py init              # Initialize secure config
python secure_config_manager.py show              # View configuration
python secure_config_manager.py set-key KEY      # Update setting

# Database & Data
python roleradar.py init                          # Initialize database
python roleradar.py search                        # Run search
python roleradar.py process                       # Process with AI
python roleradar.py stats                         # View statistics

# Running the App
python roleradar.py dashboard                     # Start web dashboard
python scheduler.py                               # Start scheduler

# Configuration
python secure_config_manager.py set-roles "roles" # Change search roles
python secure_config_manager.py set-schedule "times" # Change schedule
```

## Next Steps

1. **First Time:** `python secure_config_manager.py init` then `python roleradar.py dashboard`
2. **Production:** `python scheduler.py` (runs searches automatically)
3. **Customize:** Use `secure_config_manager.py` to adjust roles, times, and credentials
4. **Monitor:** Access dashboard at `http://localhost:5000`

---

For detailed documentation, see the respective guide files in the docs/ folder.
