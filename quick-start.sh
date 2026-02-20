#!/bin/bash
# Quick Start Guide for GuardianShield Flask API

echo "🛡️  GuardianShield - Flask API Setup & Test"
echo "=============================================="
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "🚀 Starting Flask API server..."
echo "   (Running on http://localhost:5000)"
echo ""

# Start the Flask app
python3 app.py &
FLASK_PID=$!

# Wait for server to start
sleep 3

echo ""
echo "✅ Flask API is running!"
echo ""
echo "📝 API Endpoints:"
echo "   POST   /api/applications - Create application"
echo "   GET    /api/applications - List applications"
echo "   POST   /api/risk-assessment/{id} - AI Risk Analysis"
echo "   GET    /api/matching/{id} - AI Child Matching"
echo "   GET    /api/health - Health check"
echo ""

# Run tests
echo "🧪 Running test suite..."
python3 test_api.py

# Clean up
kill $FLASK_PID 2>/dev/null

echo ""
echo "✅ Test completed!"
