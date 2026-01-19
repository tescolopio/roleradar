# 🎯 RoleRadar - Intelligent Opportunity Discovery Platform

[![Portfolio Project](https://img.shields.io/badge/Portfolio-Project-blue)](https://github.com/tescolopio/roleradar)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

> An intelligent, fully-configurable opportunity discovery platform that automates targeted searches for job roles using advanced AI analysis. Production-ready, enterprise-grade, and built for community collaboration.

## 🌟 Highlights

### For Employers/Reviewers
- **Full-Stack Python** - API integration, CLI tools, web dashboards, databases
- **Production-Ready** - Error handling, validation, comprehensive logging
- **Extensible Design** - Easy to add features, community-friendly architecture
- **Professional Documentation** - 1000+ lines covering every aspect
- **Advanced Features** - Multi-database strategy, AI integration, real-time scheduling

### For End Users
- **5-Minute Setup** - Get running immediately with simple commands
- **Flexible Configuration** - CLI tool, JSON, or environment variables
- **Community-Ready** - Import/export configurations, pre-built examples
- **No Lock-in** - Customize everything, switch configurations anytime
- **Beautiful Interface** - Intuitive CLI, interactive web dashboard

## 🚀 Quick Start

### 1. Install & Configure (2 minutes)
```bash
# Install dependencies
pip install -r requirements.txt

# Edit .env with your API keys
TAVILY_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
```

### 2. View Configuration (30 seconds)
```bash
python config_manager.py show
```

### 3. Start Searching (1 minute)
```bash
python scheduler.py
```

**That's it!** Searches now run automatically at your configured times.

## ✨ Core Features

### 🎯 Fully Configurable
- **Search Roles**: Define any job titles to search for
- **Schedule Times**: 1-6+ times daily at custom hours
- **Timezone Support**: Full IANA timezone database (100+ timezones)
- **Easy Management**: CLI tool with 9+ commands

### 📚 Community Configuration Library
Pre-built configurations for common use cases:
- **Security & Compliance**: 8 roles, 3x daily (8 AM, 12 PM, 3 PM EST)
- **DevOps & Infrastructure**: 6 roles, 4x daily
- **Privacy & Data Protection**: 5 roles, 2x daily (Europe/London)
- **24/7 Monitoring**: Every 4 hours (6 searches daily, UTC)
- **Startup Signals**: Tech roles, 2x daily (Los Angeles)

### 🤖 Intelligent Analysis
- **Tavily Search API**: Targeted web searches for opportunities
- **Groq LLM**: Entity extraction, hiring signal detection, company scoring
- **AI-Powered**: Automatic analysis without manual intervention

### 💾 Persistent Data
- **SQL Database**: Structured data (companies, opportunities, signals)
- **Graph Database**: Relationship tracking and network analysis
- **Scalable**: Ready for growth from startups to enterprises

### 📊 Interactive Dashboard
- Web-based UI showing opportunities
- Top companies by score
- Active job postings
- Hiring signals and trends
- REST API endpoints

## 🛠️ Configuration Examples

### 3 Times Daily (Default)
```bash
python config_manager.py set-schedule "08:00, 12:00, 15:00"
```

### Every 4 Hours (24/7)
```bash
python config_manager.py set-schedule "00:00, 04:00, 08:00, 12:00, 16:00, 20:00"
```

### DevOps Roles
```bash
python config_manager.py set-roles "DevOps engineer, SRE, cloud architect, infrastructure engineer"
```

### Use Pre-built Config
```bash
python config_manager.py import config-examples/devops-infrastructure-focus.json
```

### Share Your Config
```bash
python config_manager.py export my-custom-config.json
```

## 📖 Documentation

| Guide | Purpose |
|-------|---------|
| **[GETTING_STARTED.md](GETTING_STARTED.md)** | 30-second quick start + common tasks |
| **[CONFIGURATION.md](CONFIGURATION.md)** | Complete configuration guide |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | CLI commands at a glance |
| **[INDEX.md](INDEX.md)** | Documentation navigator |
| **[config-examples/README.md](config-examples/README.md)** | Pre-built configurations guide |

## 🎬 See It In Action

### Portfolio Demo
```bash
python portfolio_demo.py
```
Showcases all features and capabilities in an interactive presentation.

### Interactive Setup
```bash
bash setup.sh
```
Walks you through configuration with helpful prompts.

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│      Schedule Manager                   │
│  (Multiple times per day, all timezones)│
└──────────┬──────────────────────────────┘
           │
           ↓
┌─────────────────────────────────────────┐
│      Tavily Search API                  │
│  (Targeted web searches)                │
└──────────┬──────────────────────────────┘
           │
           ↓
┌─────────────────────────────────────────┐
│      Groq LLM Analysis                  │
│  (Entity extraction, scoring)           │
└──────────┬──────────────────────────────┘
           │
           ↓
┌──────────┴──────────────────────────────┐
│                                         │
├─ SQL Database        ─ Graph Database ─┤
│ (Structured data)    (Relationships)   │
│                                         │
└──────────┬──────────────────────────────┘
           │
           ↓
┌─────────────────────────────────────────┐
│      Web Dashboard & API                │
│  (Interactive UI, REST endpoints)       │
└─────────────────────────────────────────┘
```

## 🎯 Command Reference

### Configuration Management
```bash
python config_manager.py show              # View current config
python config_manager.py set-roles "..."   # Replace all roles
python config_manager.py add-role "..."    # Add single role
python config_manager.py remove-role "..." # Remove role
python config_manager.py set-schedule "..." # Replace schedule
python config_manager.py add-time "..."    # Add time slot
python config_manager.py remove-time "..." # Remove time slot
python config_manager.py export <file>     # Save config
python config_manager.py import <file>     # Load config
```

### Core Application
```bash
python roleradar.py init                   # Initialize database
python roleradar.py search                 # Run one search
python roleradar.py process                # Process results
python roleradar.py dashboard              # Start web UI
python scheduler.py                        # Start auto scheduler
```

## 🌟 Why This Project Stands Out

### Technical Excellence
- ✅ **Clean Code** - Modular design, separation of concerns
- ✅ **Error Handling** - Comprehensive exception management
- ✅ **Validation** - Input validation at all layers
- ✅ **Logging** - Detailed operational logging
- ✅ **Testing** - Configurable test suite

### Product Quality
- ✅ **Easy Setup** - 5-minute installation
- ✅ **Great UX** - Intuitive CLI, beautiful dashboard
- ✅ **Comprehensive Docs** - 1000+ lines of documentation
- ✅ **Community Ready** - Pre-built configs, easy sharing
- ✅ **Production Ready** - No crashes, handles edge cases

### Extensibility
- ✅ **Plugin Architecture** - Easy to add new search APIs
- ✅ **Modular Services** - Independent, reusable components
- ✅ **Database Agnostic** - SQL + Graph options
- ✅ **API Integration** - RESTful endpoints
- ✅ **Configuration First** - Everything is configurable

## 📚 Project Statistics

- **Code**: 350+ lines (config_manager.py)
- **Documentation**: 1000+ lines across 8+ files
- **Configurations**: 5 pre-built examples
- **Commands**: 9+ CLI commands with full help
- **Timezones**: 100+ supported timezones
- **Backward Compatible**: No breaking changes

## 🚀 Implementation Highlights

### User-Facing Features
- Multi-method configuration (ENV, CLI, JSON)
- Runtime configuration updates
- Configuration import/export
- Pre-built configuration templates
- Multiple search schedules
- Full timezone support

### Technical Implementation
- Enhanced config system with dynamic updates
- Multi-time job scheduler
- JSON-based configuration persistence
- Comprehensive validation
- Error handling & user feedback
- Beautiful CLI output

### Documentation
- Getting started guide
- Complete configuration guide
- Quick reference cards
- Implementation details
- Validation report
- Community guides

## 💼 Portfolio Talking Points

1. **Full-Stack Development**: Python CLI, backend services, database layer, web UI
2. **API Integration**: Successfully integrated Tavily Search and Groq LLM APIs
3. **System Design**: Modular architecture supporting multiple databases (SQL + Graph)
4. **User Experience**: Intuitive CLI tool, configuration management, pre-built examples
5. **Documentation**: Professional documentation for users, developers, and community
6. **Scalability**: Designed to scale from individual use to enterprise deployment
7. **Community Focus**: Configuration sharing, pre-built examples, extensible design
8. **Production Readiness**: Error handling, validation, logging, testing

## 🔧 Tech Stack

- **Python** 3.8+ - Core language
- **Tavily API** - Web search integration
- **Groq LLM** - AI analysis and extraction
- **SQLAlchemy** - SQL database ORM
- **NetworkX** - Graph database
- **Flask** - Web dashboard
- **Schedule** - Job scheduling
- **Click/Argparse** - CLI framework

## 📝 License

MIT License - See [LICENSE](LICENSE) for details

## 🤝 Community

This project welcomes community contributions:
- Create specialized configurations for your use case
- Share your configurations via PR
- Contribute improvements to documentation
- Report bugs and suggest features

## ✨ Get Started

1. **Read**: [GETTING_STARTED.md](GETTING_STARTED.md) (5 minutes)
2. **Setup**: `pip install -r requirements.txt` (1 minute)
3. **Configure**: Edit `.env` with your API keys (2 minutes)
4. **Run**: `python portfolio_demo.py` to see features (1 minute)
5. **Launch**: `python scheduler.py` to start searching (ongoing)

---

**Built with ❤️ for portfolio presentation**

For detailed information, explore the documentation files or run `portfolio_demo.py` for an interactive showcase.
