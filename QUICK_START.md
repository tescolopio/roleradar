# RoleRadar - Quick Start Guide

## ⚡ Fastest Way to Get Started (No CLI Required!)

### 1. Install Dependencies
```bash
cd /mnt/d/roleradar
pip install -r requirements.txt
```

### 2. Start Dashboard
```bash
python roleradar.py dashboard
```

### 3. Open Admin Panel
```
http://localhost:5000/admin
```

### 4. Configure Everything Through GUI
- **Credentials Tab:** Enter Tavily & Groq API keys
- **Configuration Tab:** Set search roles
- **Schedule Tab:** Set up automated searches
- That's it!

See [CREDENTIALS_SETUP_GUIDE.md](CREDENTIALS_SETUP_GUIDE.md) for detailed walkthrough.

---

## Prerequisites & Options

### Option A: GUI Setup (Recommended - No CLI Knowledge Needed)
1. Follow the "Fastest Way" section above
2. All configuration through web interface
3. No command line needed

### Option B: CLI Setup (For Advanced Users)

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

### Option 2: Run Search & View Results (Through Web Interface)

```bash
# Start the web dashboard
python roleradar.py dashboard
```

Then:
1. Open: **http://localhost:5000/admin**
2. Go to **Search Control** tab
3. Click **Search Now** to start a search
4. Refresh dashboard to see results

### Option 3: Automated Scheduler (Production)

```bash
# Start background scheduler (runs searches at configured times)
python scheduler.py
```

This will:
- Run searches at configured times (configured in admin panel)
- Automatically process results
- Store in database
- Dashboard updates automatically
- You can still access dashboard at **http://localhost:5000**

## Web Interface Walkthrough

### Main Dashboard (http://localhost:5000)
**What you'll see:**
- Top companies by opportunity score
- Recent hiring signals  
- Job opportunities by role
- Executive summary insights
- Admin Panel link (⚙️ button)

### Credentials Tab (First Step!)
1. Click **Admin Panel** (⚙️) button
2. Select **Credentials** tab (default)
3. Enter:
   - **Tavily API Key:** Get from https://tavily.com
   - **Groq API Key:** Get from https://console.groq.com
   - (Optional) Database URL for PostgreSQL/MySQL
4. Click **Test Credentials**
5. Click **Save**

See [CREDENTIALS_SETUP_GUIDE.md](CREDENTIALS_SETUP_GUIDE.md) for full details.

### Configuration Tab
- Add search roles (e.g., "CISO", "Security Director")
- Delete existing roles
- Settings saved automatically

### Schedule Tab
- Set automated search times
- Enable/disable automated searches
- Check current schedule status

### Prompts Tab
- Customize AI extraction prompts
- Adjust what data gets collected
- Reset to defaults if needed

### Weights Tab
- Adjust scoring algorithm weights
- Fine-tune what makes a "hot" opportunity
- View current weight values

### Search Control Tab
- Search immediately
- Enter custom queries
- Process results now
- View last search status

### System Tab
- View system status
- Check active connections
- Monitor resource usage

## Complete Workflow Example

```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Start dashboard
python roleradar.py dashboard

# Step 3: Open admin panel in your browser
# URL: http://localhost:5000/admin

# Step 4: Configure credentials (Credentials tab)
# - Enter Tavily API key
# - Enter Groq API key
# - Click Test, then Save

# Step 5: Set up search roles (Configuration tab)
# - Add roles you want to search for
# - e.g., "CISO", "Security Director", "VP of Security"

# Step 6: Configure schedule (Schedule tab, optional)
# - Set automated search times
# - Or manually search whenever

# Step 7: Run first search (Search Control tab)
# - Click "Search Now"
# - Wait for search to complete

# Step 8: View results
# - Go back to http://localhost:5000
# - Browse opportunities by role
# - Check company scores
```

## Command Line (Advanced/Optional)

**View current configuration:**
```bash
python secure_config_manager.py show
```

**Search manually:**
```bash
python roleradar.py search
```

**Process results:**
```bash
python roleradar.py process
```

**Note:** Most users won't need these - the web interface handles everything!

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
- Go to Admin Panel > Credentials tab
- Enter your PostgreSQL connection string
- Click Test, then Save

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
