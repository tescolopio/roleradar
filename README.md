# 🎯 RoleRadar

An intelligent system that automates daily searches for security, compliance, and GRC opportunities using Tavily for targeted queries and Groq for extraction, scoring, and summarization. It stores results in SQL and graph databases and surfaces them in a dashboard, highlighting posted roles and companies showing signals they'll need security or compliance leadership soon.

## Features

- **🔍 Automated Daily Searches**: Uses Tavily API to search for security, compliance, and GRC job opportunities
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

3. Configure API keys:
```bash
cp .env.example .env
# Edit .env and add your API keys:
# - TAVILY_API_KEY: Get from https://tavily.com
# - GROQ_API_KEY: Get from https://console.groq.com
```

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

This will run searches daily at 9:00 AM and process results automatically.

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

## Configuration

Edit `src/roleradar/config.py` to customize:

- Search queries
- Scoring weights
- API settings
- Dashboard settings

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
├── requirements.txt           # Dependencies
└── README.md
```

### Requirements

- Python 3.8+ (3.12+ recommended for better timezone handling)
- Tavily API key
- Groq API key

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
