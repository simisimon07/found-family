# GuardianShield - AI-Powered Child Safety Platform

A comprehensive Flask-based web application that uses **Google's Gemini AI** to improve guardian applicant assessment and child-to-guardian matching.

## 🚀 What's New: Gemini AI Integration

This system now features **advanced AI-powered risk assessment** and **intelligent child matching** using Google's Gemini Pro model.

### Key Improvements

| Feature | Before | After |
|---------|--------|-------|
| **Risk Assessment** | Simple rule-based scoring | Contextual AI analysis with detailed reasoning |
| **Child Matching** | Basic demographic matching | Deep compatibility analysis |
| **Recommendations** | Generic pass/fail | Specific, actionable guidance |
| **Transparency** | Black-box decisions | Clear AI explanations |
| **Accuracy** | Fixed logic | Contextual understanding |

## 📋 Project Structure

```
found-family/
├── app.py                      # Main Flask application & API endpoints
├── models.py                   # Database models (Applications, Children, Matches)
├── ai_service.py              # Gemini AI integration for risk assessment & matching
├── requirements.txt           # Python dependencies
├── .env                       # Environment configuration (API keys)
│
├── apply.html                 # Guardian application form
├── dashboard.html             # Admin dashboard & application management
├── risk.html                  # Risk assessment analysis page
├── status.html                # Application status tracking
├── index.html                 # Landing page
├── styles.css                 # Shared styling
│
├── FLASK_API_README.md        # Complete API documentation
├── INTEGRATION_GUIDE.py       # How to integrate frontend with API
├── API_EXAMPLES.py            # Example API calls and responses
├── test_api.py               # Test suite for all endpoints
│
├── run.sh                     # Quick start script
└── quick-start.sh            # Setup and test script
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start Flask API server
python3 app.py

# 3. API will be available at:
# http://localhost:5000/api
```

### Using Start Scripts

```bash
# Make scripts executable
chmod +x run.sh quick-start.sh

# Run quick start (installs, starts server, runs tests)
./quick-start.sh

# Or run start script
./run.sh
```

## 🤖 AI Features (Gemini Integration)

### 1. **Intelligent Risk Assessment**
- **AI Model**: Google Gemini Pro
- **Analyzes**: Income stability, debt, legal background, housing, health status, references
- **Returns**: Risk score (0-100), risk level, specific risk factors, protective factors, recommendations
- **Endpoint**: `POST /api/risk-assessment/{app_id}`

### 2. **Smart Child Matching**
- **AI Model**: Google Gemini Pro
- **Considers**: Age compatibility, lifestyle alignment, financial capacity, special needs, shared interests
- **Returns**: Compatibility scores, match reasoning, potential challenges, support recommendations
- **Endpoints**: 
  - `GET /api/matching/{app_id}` - Find all potential matches
  - `GET /api/matching/{app_id}/{child_id}` - Detailed analysis for specific match

## 📡 API Endpoints

### Application Management
- `POST /api/applications` - Create new application
- `GET /api/applications` - List all applications
- `GET /api/applications/{id}` - Get application details
- `PUT /api/applications/{id}` - Update application

### AI Risk Assessment
- `POST /api/risk-assessment/{id}` - Perform AI risk analysis

### AI Child Matching
- `GET /api/matching/{id}` - Find matching children
- `GET /api/matching/{id}/{child_id}` - Detailed match analysis

### Child Management
- `POST /api/children` - Create child record
- `GET /api/children` - List all children
- `GET /api/children/{id}` - Get child details

### Decision & Status
- `POST /api/applications/{id}/decision` - Record decision
- `GET /api/stats` - Get system statistics
- `GET /api/health` - Health check

## 🔑 Configuration

### Environment Variables (.env)

```env
GEMINI_API_KEY=AIzaSyAR1BFvpUr7YbNzIQnVT7T2D-oJeO-lwLA
FLASK_ENV=development
DATABASE_URL=sqlite:///guardian_shield.db
SECRET_KEY=your-secret-key-change-in-production
```

## 💾 Database

The system uses **SQLite** by default with automatic schema creation. Models include:

- **Application**: Guardian applicant data and AI assessments
- **Child**: Children needing guardianship and requirements
- **Match**: Guardian-child compatibility records

## 📚 Documentation

- **[FLASK_API_README.md](FLASK_API_README.md)** - Complete API reference
- **[INTEGRATION_GUIDE.py](INTEGRATION_GUIDE.py)** - Frontend integration instructions
- **[API_EXAMPLES.py](API_EXAMPLES.py)** - Example API calls and responses

## 🧪 Testing

Run the test suite:

```bash
# Make sure Flask API is running
python3 app.py

# In another terminal, run tests
python3 test_api.py
```

The test suite covers:
- Creating guardian applications
- Listing applications
- AI risk assessment
- Creating child records
- AI child matching
- System statistics

## 🛠️ How It Works

### Risk Assessment Flow

1. Guardian submits application via form
2. Flask API stores application in database
3. Frontend calls `/api/risk-assessment/{id}`
4. Backend sends application data to Gemini AI
5. Gemini analyzes context and returns structured assessment
6. Results stored in database
7. Risk score, factors, and recommendations displayed

### Child Matching Flow

1. Administrator views application
2. Clicks "Find Matches" button
3. Frontend calls `/api/matching/{app_id}`
4. Backend retrieves all available children
5. Sends applicant + children data to Gemini AI
6. Gemini analyzes compatibility for all children
7. Returns ranked matches with scores and reasoning
8. Caseworker reviews matches and selects best fit

## 🔐 Security

- Environment variables for sensitive data
- SQLite database with data isolation
- CORS configuration for cross-origin requests
- Audit trails for all decisions
- No exposure of AI model internals

## 🚢 Deployment

### Development
```bash
python3 app.py
```

### Production
```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app

# Use production database (PostgreSQL recommended)
# Update DATABASE_URL in .env
# Set FLASK_ENV=production
# Use strong SECRET_KEY
# Enable HTTPS
```

## 📊 Example Usage

### Create Application
```bash
curl -X POST http://localhost:5000/api/applications \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "occupation": "Engineer",
    ...
  }'
```

### Perform AI Risk Assessment
```bash
curl -X POST http://localhost:5000/api/risk-assessment/GS-A1B2C3D4
```

### Find AI Matches
```bash
curl -X GET http://localhost:5000/api/matching/GS-A1B2C3D4
```

## 🎯 Key Benefits Over Basic System

1. **Better Decisions**: AI understands context, not just individual factors
2. **Time Saving**: Automated analysis reduces manual review burden
3. **Consistency**: Same criteria applied to all applicants
4. **Transparency**: Clear reasoning for caseworkers to review
5. **Safety**: Identifies subtle risk patterns human reviewers might miss
6. **Scalability**: Handles growing numbers of applications

## 📝 Notes for Users

- All AI assessments should be reviewed by qualified caseworkers
- Final decisions remain with human evaluators
- System provides recommendations, not decisions
- Gemini API key is configured in .env file
- Database auto-creates tables on first run

## 🤝 Support

For issues or questions:
1. Check the API documentation in FLASK_API_README.md
2. Review integration guide in INTEGRATION_GUIDE.py
3. Run test suite to verify setup: `python3 test_api.py`

---

**Built with**: Flask, SQLAlchemy, Google Gemini AI, SQLite