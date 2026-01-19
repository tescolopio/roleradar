# RoleRadar Installation & Setup Guide

## System Requirements

- **Python**: 3.8 or higher (3.10+ recommended)
- **OS**: Linux, macOS, or Windows (WSL)
- **Disk Space**: ~100MB for installation + database
- **Internet**: Required for API access (Tavily, Groq)

## Step 1: Get Your API Keys (5 minutes)

### Tavily Search API Key
1. Visit https://tavily.com
2. Sign up for a free account
3. Copy your API key
4. Save it somewhere safe

### Groq API Key
1. Visit https://console.groq.com
2. Sign up for a free account
3. Create an API key
4. Copy the key

**Total time**: ~5 minutes, completely free tier access available

## Step 2: Clone & Install (3 minutes)

### Option A: Git Clone (Recommended)
```bash
# Clone the repository
git clone https://github.com/tescolopio/roleradar.git
cd roleradar

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Option B: Direct Download
1. Download the project files
2. Extract to a folder
3. Open terminal in that folder
4. Run: `pip install -r requirements.txt`

## Step 3: Configure (2 minutes)

### Create .env File
```bash
# Copy the example
cp .env .env.local

# Edit .env with your editor
nano .env
# or
code .env
# or
vim .env
```

### Add Your API Keys
```bash
# Find these lines and replace with your actual keys
TAVILY_API_KEY=your_actual_key_here
GROQ_API_KEY=your_actual_key_here

# These can stay as default or customize
TIMEZONE=America/New_York
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

### Verify Configuration
```bash
python config_manager.py show
```

You should see something like:
```
╔══════════════════════════════════════════════════════════╗
║                 Current Configuration                    ║
╚══════════════════════════════════════════════════════════╝

Timezone: America/New_York

Search Roles (8):
  1. security engineer
  2. compliance officer
  ...

Scheduled Search Times (3):
  • 08:00 America/New_York
  • 12:00 America/New_York
  • 15:00 America/New_York

Total Search Queries: 16
```

## Step 4: Run It! (Choose One)

### 🎬 See Portfolio Demo (1 minute)
```bash
python portfolio_demo.py
```
Interactive showcase of all features. Great for presentations!

### 🔧 Initialize Database
```bash
python roleradar.py init
```

### 🚀 Start Scheduler (Continuous)
```bash
python scheduler.py
```
Searches run automatically at your configured times.

### 🖥️ Start Web Dashboard
```bash
python roleradar.py dashboard
```
Then visit: http://localhost:5000

### 🔍 Run One Search
```bash
python roleradar.py search
```

## ✅ Verification Checklist

After installation, verify everything works:

- [ ] Python installed: `python --version` shows 3.8+
- [ ] Dependencies installed: `pip list | grep -E "tavily|groq|schedule"`
- [ ] .env file created with API keys
- [ ] Configuration loads: `python config_manager.py show` works
- [ ] Database initializes: `python roleradar.py init` completes
- [ ] Demo runs: `python portfolio_demo.py` displays features

## Troubleshooting

### "No module named 'src.roleradar'"
**Solution**: Ensure you're in the roleradar directory and have run `pip install -r requirements.txt`

### "TAVILY_API_KEY not found"
**Solution**: 
1. Check .env file exists in current directory
2. Verify API key is set correctly (no quotes, no spaces)
3. Run: `echo $TAVILY_API_KEY` to verify it's loaded

### "Connection refused" (for web dashboard)
**Solution**: 
1. Check no other service uses port 5000
2. Try different port: Edit .env, change `FLASK_PORT=5001`

### "ModuleNotFoundError: No module named 'schedule'"
**Solution**: Run `pip install -r requirements.txt` again

### API rate limiting
**Solution**: 
1. Tavily free tier: Check remaining quota at https://tavily.com
2. Groq free tier: Usually very generous, check at https://console.groq.com
3. Reduce search frequency if needed

## Next Steps

### 1. Customize (Optional)
```bash
# Search for different roles
python config_manager.py set-roles "DevOps engineer, SRE, cloud architect"

# Search more/less frequently
python config_manager.py set-schedule "08:00, 12:00, 15:00, 18:00"

# Change timezone
# Edit .env: TIMEZONE=America/Los_Angeles
```

### 2. Learn Configuration
```bash
python config_manager.py -h          # CLI help
cat GETTING_STARTED.md               # Quick start
cat CONFIGURATION.md                 # Detailed guide
cat QUICK_REFERENCE.md               # Command reference
```

### 3. Try Pre-built Configurations
```bash
# DevOps focus
python config_manager.py import config-examples/devops-infrastructure-focus.json

# Privacy focus
python config_manager.py import config-examples/privacy-data-protection-focus.json

# 24/7 monitoring
python config_manager.py import config-examples/continuous-monitoring-24h.json
```

### 4. Start Production Use
```bash
# Run scheduler in background
python scheduler.py &

# Or use nohup
nohup python scheduler.py > roleradar.log 2>&1 &

# Or systemd service (see docs)
```

## Common Configuration Examples

### Search 6 Times Daily
```bash
python config_manager.py set-schedule "00:00, 04:00, 08:00, 12:00, 16:00, 20:00"
```

### Search Only Business Hours
```bash
python config_manager.py set-schedule "08:00, 10:00, 12:00, 14:00, 16:00"
```

### Search for Privacy Roles
```bash
python config_manager.py set-roles "privacy officer, DPO, privacy engineer, data governance specialist"
```

### Use Europe Timezone
```bash
# Edit .env
TIMEZONE=Europe/London
```

### Export Your Config
```bash
python config_manager.py export my-config.json
```

### Import a Config
```bash
python config_manager.py import my-config.json
```

## Database Options

### SQLite (Default)
Fast, lightweight, built-in. Good for development and small deployments.

### PostgreSQL
For production deployments. Edit .env:
```bash
DATABASE_URL=postgresql://user:password@host:port/roleradar
```

## Advanced Setup

### Docker (Optional)
```bash
# Build image
docker build -t roleradar .

# Run container
docker run -e TAVILY_API_KEY=your_key \
           -e GROQ_API_KEY=your_key \
           -p 5000:5000 \
           roleradar
```

### Systemd Service (Linux)
Create `/etc/systemd/system/roleradar.service`:
```ini
[Unit]
Description=RoleRadar Scheduler
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/roleradar
ExecStart=/usr/bin/python3 /path/to/roleradar/scheduler.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable roleradar
sudo systemctl start roleradar
sudo systemctl status roleradar
```

## Support & Documentation

- **Quick Start**: [GETTING_STARTED.md](GETTING_STARTED.md)
- **Full Guide**: [CONFIGURATION.md](CONFIGURATION.md)
- **Commands**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **Portfolio Info**: [PORTFOLIO.md](PORTFOLIO.md)
- **Index**: [INDEX.md](INDEX.md)

## Getting Help

1. Check documentation files
2. Run: `python config_manager.py -h`
3. Review example configurations
4. Check the code comments

## Security Notes

- **API Keys**: Never commit .env to version control
- **Credentials**: Use environment variables for sensitive data
- **Network**: Assume database may be accessed remotely
- **Updates**: Keep dependencies updated with `pip install -U -r requirements.txt`

---

**That's it! You're ready to use RoleRadar!**

Start with:
```bash
python portfolio_demo.py  # See it in action
python scheduler.py       # Start searching
```

For details, see GETTING_STARTED.md or CONFIGURATION.md
