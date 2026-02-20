#!/bin/bash

# GuardianShield Flask API Setup and Run Script

echo "🛡️  GuardianShield - Flask API Setup"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""
echo "🔗 Activating virtual environment..."
source venv/bin/activate

echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Environment Configuration (.env file)"
echo "========================================="
echo "API Key: AIzaSyAR1BFvpUr7YbNzIQnVT7T2D-oJeO-lwLA"
echo "Database: SQLite (guardian_shield.db)"
echo ""

echo "🚀 Starting Flask API Server..."
echo "Server will be available at: http://localhost:5000"
echo ""
echo "API Endpoints:"
echo "- POST   /api/applications         - Create new application"
echo "- GET    /api/applications         - List all applications"
echo "- GET    /api/applications/{id}    - Get application details"
echo "- PUT    /api/applications/{id}    - Update application"
echo "- POST   /api/risk-assessment/{id} - Perform risk assessment using Gemini AI"
echo "- GET    /api/matching/{id}        - Find matching children using Gemini AI"
echo "- GET    /api/matching/{id}/{cid}  - Get detailed match analysis"
echo "- POST   /api/children             - Create child record"
echo "- GET    /api/children             - List all children"
echo "- GET    /api/stats                - Get system statistics"
echo "- GET    /api/health               - Health check"
echo ""

python3 app.py
