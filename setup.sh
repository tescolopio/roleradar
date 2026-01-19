#!/bin/bash
# RoleRadar Quick Setup Script
# Gets you up and running in minutes!

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                  🎯 RoleRadar Quick Setup                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "✓ Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Found Python $python_version"
echo ""

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found!"
    exit 1
fi

# Install dependencies
echo "✓ Installing dependencies..."
pip install -q -r requirements.txt
echo "  Dependencies installed successfully"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating template..."
    cat > .env << 'EOF'
# RoleRadar Configuration

# API Keys (Get yours from https://tavily.com and https://console.groq.com)
TAVILY_API_KEY=your_key_here
GROQ_API_KEY=your_key_here

# Database
DATABASE_URL=sqlite:///roleradar.db

# Application
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# Scheduling
TIMEZONE=America/New_York
SEARCH_ROLES=["security engineer", "compliance officer", "CISO"]
SCHEDULE_TIMES=["08:00", "12:00", "15:00"]
EOF
    echo "  Created .env template"
    echo "  ⚠️  IMPORTANT: Edit .env and add your API keys!"
    echo ""
else
    echo "✓ Found existing .env configuration"
    echo ""
fi

# Show configuration
echo "✓ Current Configuration:"
python3 config_manager.py show 2>/dev/null || echo "  (Run config_manager.py to see details)"
echo ""

# Final instructions
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    🚀 Setup Complete!                         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your API keys"
echo "  2. Run portfolio demo:     python demo.py"
echo "  3. View configuration:     python config_manager.py show"
echo "  4. Customize if needed:    python config_manager.py set-roles \"...\""
echo "  5. Start scheduler:        python scheduler.py"
echo ""
echo "📚 Documentation:"
echo "  • GETTING_STARTED.md - 30-second quick start"
echo "  • CONFIGURATION.md - Detailed configuration guide"
echo "  • QUICK_REFERENCE.md - Command reference"
echo ""
echo "Happy searching! 🎯"
echo ""
