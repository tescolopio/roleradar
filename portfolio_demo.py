#!/usr/bin/env python3
"""
RoleRadar Portfolio Demo Script
Showcases the key features and capabilities for portfolio presentation
"""

import json
import time
from src.roleradar.config import config


def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*72}")
    print(f"  {title.center(70)}")
    print(f"{'='*72}\n")


def demo_configuration_management():
    """Demonstrate configuration management."""
    print_header("1️⃣  CONFIGURATION MANAGEMENT")
    
    print("🎯 RoleRadar supports multiple configuration methods:\n")
    
    print("📋 Current Configuration:")
    print(f"   └─ Timezone: {config.TIMEZONE}")
    print(f"   └─ Search Roles: {len(config.SEARCH_ROLES)} configured")
    print(f"   └─ Daily Searches: {len(config.SCHEDULE_TIMES)} times")
    print(f"   └─ Total Queries: {len(config.SEARCH_QUERIES)} generated\n")
    
    print("⚙️  Configuration Methods:")
    print("   1. Environment Variables (.env file)")
    print("   2. CLI Tool (config_manager.py)")
    print("   3. JSON Files (import/export)\n")


def demo_flexible_scheduling():
    """Demonstrate scheduling flexibility."""
    print_header("2️⃣  FLEXIBLE SCHEDULING")
    
    print("🕐 Schedule searches at ANY times throughout the day:\n")
    
    schedules = {
        "3x Daily (Default)": ["08:00", "12:00", "15:00"],
        "Every 4 Hours (24/7)": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
        "Business Hours": ["08:00", "10:00", "12:00", "14:00", "16:00"],
        "Morning & Evening": ["07:00", "19:00"],
        "Single Daily Alert": ["09:00"],
    }
    
    for name, times in schedules.items():
        status = "✓" if times == config.SCHEDULE_TIMES else "○"
        print(f"  {status} {name:<30} {', '.join(times)}")
    print()


def demo_role_customization():
    """Demonstrate role customization."""
    print_header("3️⃣  SEARCH ROLE CUSTOMIZATION")
    
    print("🎯 Search for ANY job roles - completely customizable!\n")
    
    role_sets = {
        "🔐 Security & Compliance": 
            ["Security Engineer", "Compliance Officer", "CISO", "GRC Analyst"],
        "☁️ DevOps & Infrastructure":
            ["DevOps Engineer", "SRE", "Cloud Architect", "Platform Engineer"],
        "🔒 Privacy & Data Protection":
            ["Privacy Officer", "DPO", "Privacy Engineer", "Data Governance Specialist"],
        "💼 Startup Tech":
            ["Full Stack Engineer", "Backend Engineer", "Product Manager"],
    }
    
    for category, roles in role_sets.items():
        print(f"  {category}:")
        for role in roles:
            print(f"     • {role}")
        print()


def demo_timezone_support():
    """Demonstrate timezone support."""
    print_header("4️⃣  TIMEZONE SUPPORT")
    
    print(f"🌍 Current Timezone: {config.TIMEZONE}\n")
    print("Supported Timezones (and many more):\n")
    
    timezones = {
        "Americas": [
            "America/New_York (ET)",
            "America/Chicago (CT)",
            "America/Denver (MT)",
            "America/Los_Angeles (PT)",
        ],
        "Europe": [
            "Europe/London (GMT/BST)",
            "Europe/Paris (CET/CEST)",
            "Europe/Berlin (CET/CEST)",
        ],
        "Asia/Pacific": [
            "Asia/Tokyo (JST)",
            "Australia/Sydney (AEDT/AEST)",
        ],
    }
    
    for region, zones in timezones.items():
        print(f"  {region}:")
        for zone in zones:
            print(f"     • {zone}")
        print()


def demo_community_configs():
    """Demonstrate pre-built configurations."""
    print_header("5️⃣  COMMUNITY CONFIGURATION LIBRARY")
    
    print("📚 Ready-to-use configurations for common scenarios:\n")
    
    configs = {
        "🔐 Security & Compliance": {
            "file": "security-compliance-focus.json",
            "roles": 8,
            "times": 3,
            "schedule": "8 AM, 12 PM, 3 PM EST",
        },
        "☁️ DevOps & Infrastructure": {
            "file": "devops-infrastructure-focus.json",
            "roles": 6,
            "times": 4,
            "schedule": "6 AM, 10 AM, 2 PM, 6 PM EST",
        },
        "🔒 Privacy & Data Protection": {
            "file": "privacy-data-protection-focus.json",
            "roles": 5,
            "times": 2,
            "schedule": "8 AM, 2 PM (Europe/London)",
        },
        "🌍 24/7 Continuous Monitoring": {
            "file": "continuous-monitoring-24h.json",
            "roles": 4,
            "times": 6,
            "schedule": "Every 4 hours (UTC)",
        },
    }
    
    for name, details in configs.items():
        print(f"  {name}")
        print(f"     File: {details['file']}")
        print(f"     Roles: {details['roles']} • Times: {details['times']}x daily")
        print(f"     Schedule: {details['schedule']}")
        print()


def demo_cli():
    """Demonstrate CLI commands."""
    print_header("6️⃣  COMMAND-LINE INTERFACE")
    
    print("⌨️  Simple, intuitive commands:\n")
    
    commands = [
        ("View configuration", "python config_manager.py show"),
        ("Set search roles", 'python config_manager.py set-roles "role1, role2, role3"'),
        ("Add a role", 'python config_manager.py add-role "privacy officer"'),
        ("Set schedule times", 'python config_manager.py set-schedule "08:00, 12:00, 15:00"'),
        ("Export config", "python config_manager.py export my-config.json"),
        ("Import config", "python config_manager.py import my-config.json"),
    ]
    
    for description, command in commands:
        print(f"  {description}:")
        print(f"     $ {command}\n")


def demo_quick_start():
    """Demonstrate quick start."""
    print_header("7️⃣  QUICK START")
    
    print("🚀 Get running in minutes:\n")
    
    steps = [
        ("1", "Install dependencies", "pip install -r requirements.txt"),
        ("2", "Configure API keys", "Edit .env - add TAVILY_API_KEY & GROQ_API_KEY"),
        ("3", "View current config", "python config_manager.py show"),
        ("4", "Customize (optional)", 'python config_manager.py set-roles "your roles"'),
        ("5", "Start searching", "python scheduler.py"),
    ]
    
    for num, description, command in steps:
        print(f"  {num}️⃣  {description}")
        print(f"      $ {command}\n")


def demo_features():
    """Demonstrate key features."""
    print_header("8️⃣  KEY FEATURES")
    
    features = [
        ("Configurable Roles", "Search for any job title, not just security"),
        ("Flexible Scheduling", "1-6+ searches daily at custom times"),
        ("Timezone Support", "Full IANA timezone database"),
        ("AI Analysis", "Groq LLM for entity extraction & scoring"),
        ("Persistent Storage", "SQL + Graph databases"),
        ("Web Dashboard", "Interactive Flask UI"),
        ("Import/Export", "Share configs via JSON"),
        ("Pre-built Configs", "5 ready-to-use examples"),
        ("Easy CLI", "Intuitive command-line tool"),
        ("Backward Compatible", "No breaking changes"),
    ]
    
    for i, (feature, description) in enumerate(features, 1):
        print(f"  ✓ {feature:<25} {description}")
    print()


def demo_architecture():
    """Demonstrate architecture."""
    print_header("9️⃣  ARCHITECTURE")
    
    print("🏗️  Clean, modular design:\n")
    
    print("  Search API (Tavily)")
    print("      ↓")
    print("  AI Analysis (Groq LLM)")
    print("      ↓")
    print("  Entity Extraction & Scoring")
    print("      ↓")
    print("  Dual Databases (SQL + Graph)")
    print("      ↓")
    print("  Web Dashboard & REST API")
    print()
    
    print("📁 Project Structure:\n")
    print("  roleradar/")
    print("  ├── config_manager.py         Configuration CLI tool")
    print("  ├── scheduler.py              Automated job scheduler")
    print("  ├── src/roleradar/")
    print("  │   ├── config.py            Configuration system")
    print("  │   ├── services/             Business logic (search, analysis)")
    print("  │   ├── models/               Data models (SQL + Graph)")
    print("  │   ├── database/             Database layer")
    print("  │   └── dashboard/            Flask web UI")
    print("  └── config-examples/          Community configurations")
    print()


def demo_portfolio_value():
    """Highlight portfolio value."""
    print_header("🌟 PORTFOLIO VALUE")
    
    print("This project demonstrates:\n")
    
    value_props = [
        ("Full-Stack Python Development", "CLI, API, Web UI, Database"),
        ("System Design", "Modular architecture, separation of concerns"),
        ("Configuration Management", "Multiple strategies, user-friendly"),
        ("API Integration", "Tavily Search, Groq LLM APIs"),
        ("Database Design", "SQL + Graph database implementation"),
        ("Documentation", "1000+ lines of professional documentation"),
        ("Community Focus", "Pre-built configs, import/export, extensible"),
        ("Production Ready", "Error handling, validation, logging"),
        ("User Experience", "CLI tool, dashboard, clear instructions"),
        ("Open Source Practices", "Backward compatible, contribution-friendly"),
    ]
    
    for feature, description in value_props:
        print(f"  ✓ {feature}")
        print(f"    → {description}\n")


def main():
    """Run the portfolio demo."""
    print("\n" + "="*72)
    print("  🎯 ROLERADAR - PORTFOLIO SHOWCASE".center(72))
    print("  Advanced Opportunity Discovery & Analysis".center(72))
    print("="*72)
    
    demos = [
        ("Configuration", demo_configuration_management),
        ("Scheduling", demo_flexible_scheduling),
        ("Customization", demo_role_customization),
        ("Timezone", demo_timezone_support),
        ("Community", demo_community_configs),
        ("CLI", demo_cli),
        ("Quick Start", demo_quick_start),
        ("Features", demo_features),
        ("Architecture", demo_architecture),
        ("Portfolio Value", demo_portfolio_value),
    ]
    
    for name, demo_func in demos:
        demo_func()
        time.sleep(0.3)  # Small delay for readability
    
    # Final section
    print_header("🎬 GET STARTED")
    print("📖 Documentation:")
    print("   • GETTING_STARTED.md     - 30-second quick start")
    print("   • CONFIGURATION.md       - Complete configuration guide")
    print("   • QUICK_REFERENCE.md     - Command reference")
    print("   • INDEX.md               - Documentation index")
    print()
    print("🚀 Next Steps:")
    print("   1. Edit .env with your API keys")
    print("   2. Run: python config_manager.py show")
    print("   3. Run: python scheduler.py")
    print()
    print("="*72)
    print("  ✨ Thank you for exploring RoleRadar!")
    print("="*72 + "\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo stopped")
