#!/bin/bash

# FWD Client Manager - Startup Script

echo "🚀 Starting FWD Client Management System..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt -q

# Initialize database
echo "🗄️  Initializing database..."
python3 -c "from app import init_db; init_db()"

# Start the application
echo ""
echo "✅ Starting server at http://localhost:5000"
echo "🛑 Press Ctrl+C to stop"
echo ""

python3 app.py
