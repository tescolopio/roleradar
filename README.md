# 🎯 RoleRadar

An intelligent system that automates daily searches for security, compliance, and GRC opportunities using Tavily or Brave Search for targeted queries and Groq for extraction, scoring, and summarization. It stores results in SQL and graph databases and surfaces them in a dashboard, highlighting posted roles and companies showing signals they'll need security or compliance leadership soon.

## ⚡ Quick Start

```bash
# 1. Install
pip install -r requirements.txt

# 2. Run dashboard
python roleradar.py dashboard

# 3. Open browser → http://localhost:5000
# 4. Click ⚙️ → Configure API keys
# 5. Add search roles → Click "Search Now"
```

Done! Everything else is through the web interface.

## Features

- **🔍 Automated Daily Searches**: Uses Tavily or Brave Search APIs to search for security, compliance, and GRC job opportunities
  - **Configurable Roles**: Search for any job title or role (not just security)
  - **Flexible Scheduling**: Run searches multiple times per day at custom times
  - **Community Ready**: Share and reuse configurations with the community
- **⚙️ Admin Management GUI**: Web-based interface for:
  - Adding/removing search roles
  - Configuring automated search schedule
  - Customizing AI extraction prompts
  - Adjusting scoring algorithm weights
  - Triggering manual searches and processing
  - Viewing system status and configuration
  - **🔐 Credential Configuration**: Securely store API keys through web interface
- **🤖 AI-Powered Analysis**: Uses Groq LLM to:
  - Extract entities (companies, job titles, locations)
  - Detect hiring signals (funding, expansion, breaches, compliance news)
  - Score companies based on opportunity likelihood
  - Summarize findings
- **💾 Dual Database Storage**: 
  - SQL database (SQLite) for structured data
  - Graph database (NetworkX) for relationship tracking
- **📊 Interactive Dashboard**: Flask-based web dashboard showing:
  - Top companies by score
  - Active job opportunities
  - Hiring signals and trends
  - Executive summaries

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tescolopio/roleradar.git
cd roleradar
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. **No CLI Setup Needed!** Start the dashboard:
```bash
python roleradar.py dashboard
```

The application opens in your browser. Everything else (API keys, configuration) is done through the GUI!

### That's It!
Your browser automatically opens to http://localhost:5000. See the **Credentials** tab in the Admin Panel to configure everything through the web interface.

**Need detailed setup steps?** See [QUICK_START.md](QUICK_START.md) or [DOCKER_DEPLOYMENT_CHECKLIST.md](DOCKER_DEPLOYMENT_CHECKLIST.md)

## Usage

### Start Dashboard (All-in-One)
```bash
python roleradar.py dashboard
```

Your browser opens automatically to **http://localhost:5000**

**Everything you need is in the web interface:**
- 🔐 **Credentials Tab:** Enter API keys (Tavily or Brave, Groq)
- ⚙️ **Configuration Tab:** Add/remove search roles
- 📅 **Schedule Tab:** Set up automated searches
- 🤖 **Prompts Tab:** Customize AI analysis
- ⚖️ **Weights Tab:** Adjust scoring algorithm
- 🔎 **Search Control Tab:** Run searches immediately
- 📊 **System Tab:** Monitor status

### Advanced Usage (Optional - For Power Users)

Run a one-time search:
```bash
python roleradar.py search
```

Process results with AI:
```bash
python roleradar.py process
```

View statistics:
```bash
python roleradar.py stats
```

**Note:** Most users won't need the CLI - everything is available in the web dashboard!

### Scheduled Searches (Production)

For 24/7 automated searches, run the scheduler in background:
```bash
python scheduler.py
```

This runs searches at times configured in the Admin Panel's Schedule tab.

---

**👉 First Time User?** Start with [QUICK_START.md](QUICK_START.md) or [DOCKER_DEPLOYMENT_CHECKLIST.md](DOCKER_DEPLOYMENT_CHECKLIST.md) Then open your browser to `http://localhost:5000`

**Dashboard Features:**
- View top companies and opportunities
- Click **⚙️ Admin Panel** for configuration

### Admin Management Panel

Configure RoleRadar without code:

```bash
# Navigate to Admin Panel
http://localhost:5000/admin
```

**In the Admin Panel, you can:**
- ✅ Add/remove search roles
- ✅ Set automated search schedule
- ✅ Customize AI extraction prompts
- ✅ Adjust scoring weights
- ✅ Trigger manual searches
- ✅ Monitor system status

See [ADMIN_GUI_QUICK_START.md](docs/ADMIN_GUI_QUICK_START.md) for detailed guide.

### Automated Daily Searches

Run the scheduler for automated daily searches:

```bash
python scheduler.py
```

This will run searches at your configured times (default: 8 AM, 12 PM, 3 PM EST) and process results automatically.

### Configuration

RoleRadar supports **secure encrypted configuration** for protecting your credentials:

#### Web-Based Configuration (Recommended)

1. Start dashboard: `python roleradar.py dashboard`
2. Open admin panel: `http://localhost:5000/admin`
3. Configure using intuitive web interface:
   - Add search roles
   - Set schedule times
   - Customize prompts
   - Adjust weights

See [ADMIN_GUI_GUIDE.md](docs/ADMIN_GUI_GUIDE.md) for comprehensive documentation.

#### Secure Configuration (Command Line)

```bash
# Initialize and set up credentials securely
python secure_config_manager.py init

# View configuration
python secure_config_manager.py show

# Update API keys
python secure_config_manager.py set-key TAVILY_API_KEY
python secure_config_manager.py set-key BRAVE_API_KEY
python secure_config_manager.py set-key GROQ_API_KEY

# Customize search roles and schedule
python secure_config_manager.py set-roles "DevOps engineer, cloud architect, SRE"
python secure_config_manager.py set-schedule "06:00, 10:00, 14:00, 18:00"

# Migrate from .env to secure storage
python secure_config_manager.py migrate
```

See [SECURE_CONFIGURATION.md](docs/SECURE_CONFIGURATION.md) for complete security documentation.

#### Customizable Settings

- **Search Roles**: Change what job titles to search for (not limited to security)
- **Schedule Times**: Search multiple times per day at custom times
- **Timezone**: Set your local timezone

See [CONFIGURATION.md](CONFIGURATION.md) for detailed instructions.

**Quick Examples:**

```bash
# View current configuration
python config_manager.py show

# Search for different roles
python config_manager.py set-roles "DevOps engineer, cloud architect, SRE"

# Change schedule to 6 AM, 10 AM, 2 PM, 6 PM
python config_manager.py set-schedule "06:00, 10:00, 14:00, 18:00"

# Add a role to existing searches
python config_manager.py add-role "Privacy Officer"

# Remove a time slot
python config_manager.py remove-time "12:00"
```

## Architecture

### Components

1. **Search Service** (`services/tavily_service.py`, `services/brave_service.py`)
   - Performs targeted searches using Tavily or Brave Search APIs
   - Stores raw search results
   - Tracks processed vs unprocessed results

2. **Analysis Service** (`services/groq_service.py`)
   - Extracts entities from text
   - Detects hiring signals
   - Scores companies
   - Generates summaries

3. **Processing Service** (`services/processing_service.py`)
   - Orchestrates search and analysis
   - Updates SQL and graph databases
   - Calculates company scores

4. **Database Layer** (`database/`, `models/`)
   - SQL models for companies, opportunities, signals
   - Graph database for relationship tracking
   - Session management

5. **Dashboard** (`dashboard/`)
   - Flask web application
   - REST API endpoints
   - Interactive UI with real-time data

### Data Flow

```
Tavily/Brave Search → Raw Results → Groq Analysis → Entity Extraction
                                    ↓
                            Hiring Signals
                                    ↓
                     SQL + Graph Database Storage
                                    ↓
                            Company Scoring
                                    ↓
                              Dashboard
```

## Database Schema

### SQL Tables

- **companies**: Company information and scores
- **opportunities**: Job postings and roles
- **hiring_signals**: Detected signals (funding, expansion, etc.)
- **search_results**: Raw search results

### Graph Relationships

- Company → has_opening → Opportunity
- Company → shows_signal → HiringSignal

## Configuration Reference

For detailed configuration documentation, see [CONFIGURATION.md](CONFIGURATION.md).

Key environment variables (in `.env`):

```bash
# Search/API Keys (Use Tavily OR Brave)
# TAVILY_API_KEY=your_key
# BRAVE_API_KEY=your_key
# GROQ_API_KEY=your_key
SEARCH_ROLES=["security engineer", "compliance officer", "CISO"]

# Scheduled Times (JSON array, 24-hour format)
SCHEDULE_TIMES=["08:00", "12:00", "15:00"]

# Timezone (IANA timezone format)
TIMEZONE=America/New_York
```

## API Endpoints

- `GET /api/summary` - Dashboard summary with stats
- `GET /api/companies?limit=20` - Top companies by score
- `GET /api/opportunities?limit=50` - Active opportunities

## Development

### Project Structure

```
roleradar/
├── src/roleradar/
│   ├── config.py              # Configuration
│   ├── models/                # Database models
│   │   ├── database.py        # SQL models
│   │   └── graph.py           # Graph database
│   ├── services/              # Business logic
│   │   ├── tavily_service.py  # Tavily search service
│   │   ├── brave_service.py   # Brave search service
│   │   ├── search_factory.py  # Search service factory
│   │   ├── groq_service.py    # AI analysis
│   │   └── processing_service.py
│   ├── database/              # Database layer
│   │   └── service.py
│   └── dashboard/             # Web dashboard
│       ├── app.py
│       ├── templates/
│       └── static/
├── roleradar.py               # CLI application
├── scheduler.py               # Automated scheduler
├── config_manager.py          # Configuration manager
├── requirements.txt           # Dependencies
├── CONFIGURATION.md           # Configuration guide
└── README.md
```

### Requirements

- Python 3.8+ (3.12+ recommended for better timezone handling)
- Tavily API key or Brave Search API key
- Groq API key

## Community

RoleRadar supports community configuration sharing! Share your role searches and schedules:

```bash
# Export your configuration
python config_manager.py export my-security-focus.json

# Others can use your configuration
python config_manager.py import my-security-focus.json
```

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Docker Deployment

Run RoleRadar with Docker for consistent deployments.

### Quick Start (docker-compose)

```bash
# 1) Build the image
docker compose build

# 2) Set env vars (create .env in repo root, optional)
cat > .env << 'EOF'
TAVILY_API_KEY=
BRAVE_API_KEY=
GROQ_API_KEY=
# Persist DB to a named volume at /data inside the container
DATABASE_URL=sqlite:////data/roleradar.db
TIMEZONE=America/New_York
# Processing + LLM safety (optional overrides)
PROCESS_BATCH_SIZE=20
GROQ_MAX_INPUT_CHARS=4000
SQLITE_FALLBACK_URL=sqlite:////data/roleradar.db
EOF

# 3) Start web + scheduler
docker compose up -d

# 4) Open the dashboard
xdg-open http://localhost:9000 || echo "Open http://localhost:9000"
```

### Notes

- Web service listens on port 8000 (mapped to host 9000 by default).
- Scheduler runs as a separate service and shares the same DB volume.
- To use Postgres/MySQL, set `DATABASE_URL` accordingly (e.g., `postgresql://user:pass@host:5432/dbname`).
- Health endpoint: `GET /api/system/health`.
- Batching and context safety:
   - `PROCESS_BATCH_SIZE` controls how many search results are processed per batch (default 20).
   - `GROQ_MAX_INPUT_CHARS` limits text length sent to Groq (default 4000), truncating longer inputs safely.
   - `SQLITE_FALLBACK_URL` ensures both services fall back to the same SQLite file if Postgres is unavailable.

### Common Commands

```bash
# View logs
docker compose logs -f web
docker compose logs -f scheduler

# Stop services
docker compose down

# Rebuild after changes
docker compose build --no-cache && docker compose up -d
```
