# 🎯 RoleRadar

An intelligent system that automates daily searches for security, compliance, and GRC opportunities using Tavily for targeted queries and Groq for extraction, scoring, and summarization. It stores results in SQL and graph databases and surfaces them in a dashboard, highlighting posted roles and companies showing signals they'll need security or compliance leadership soon.

## Features

- **🔍 Automated Daily Searches**: Uses Tavily API to search for security, compliance, and GRC job opportunities
  - **Configurable Roles**: Search for any job title or role (not just security)
  - **Flexible Scheduling**: Run searches multiple times per day at custom times
  - **Community Ready**: Share and reuse configurations with the community
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
- **🔐 Secure Configuration**: 
  - AES-256 encrypted credential storage
  - Master password protection
  - No plaintext API keys in files
  - PBKDF2 key derivation (390k iterations)

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

3. **Secure Configuration (Recommended):**
```bash
# Initialize encrypted credential storage
python secure_config_manager.py init
# You'll be prompted to create a master password and enter API keys

# Get API keys from:
# - Tavily: https://tavily.com
# - Groq: https://console.groq.com
```

**Alternative (Legacy .env method):**
```bash
cp .env.example .env
# Edit .env and add your API keys
# Note: This method stores credentials in plaintext
```

See [SECURE_CONFIGURATION.md](SECURE_CONFIGURATION.md) for detailed security setup.

## Usage

### Initialize Database

```bash
python roleradar.py init
```

### Run a Search

Run a one-time search for opportunities:

```bash
python roleradar.py search
```

### Process Results

Process unprocessed search results with AI analysis:

```bash
python roleradar.py process
```

### View Statistics

```bash
python roleradar.py stats
```

### Launch Dashboard

Start the web dashboard:

```bash
python roleradar.py dashboard
```

Then open your browser to `http://localhost:5000`

### Automated Daily Searches

Run the scheduler for automated daily searches:

```bash
python scheduler.py
```

This will run searches at your configured times (default: 8 AM, 12 PM, 3 PM EST) and process results automatically.

### Configuration

RoleRadar supports **secure encrypted configuration** for protecting your credentials:

#### Secure Configuration (Recommended)

```bash
# Initialize and set up credentials securely
python secure_config_manager.py init

# View configuration
python secure_config_manager.py show

# Update API keys
python secure_config_manager.py set-key TAVILY_API_KEY
python secure_config_manager.py set-key GROQ_API_KEY

# Customize search roles and schedule
python secure_config_manager.py set-roles "DevOps engineer, cloud architect, SRE"
python secure_config_manager.py set-schedule "06:00, 10:00, 14:00, 18:00"

# Migrate from .env to secure storage
python secure_config_manager.py migrate
```

See [SECURE_CONFIGURATION.md](SECURE_CONFIGURATION.md) for complete security documentation.

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

1. **Search Service** (`services/tavily_service.py`)
   - Performs targeted searches using Tavily API
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
Tavily Search → Raw Results → Groq Analysis → Entity Extraction
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
# Search Roles (JSON array)
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
│   │   ├── tavily_service.py  # Search service
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
- Tavily API key
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
