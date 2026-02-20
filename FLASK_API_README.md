# GuardianShield - Flask API with Gemini AI Integration

## Overview

GuardianShield is an AI-powered child safety and guardianship application platform. This Flask API backend uses **Google's Gemini AI** to provide:

- **Intelligent Risk Assessment**: AI analyzes applicant data to identify risk factors, protective factors, and provide detailed recommendations
- **Smart Child Matching**: AI matches qualified guardians with children based on compatibility factors
- **Comprehensive Application Management**: Store and track guardian applications with full audit trails

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure Environment**
The `.env` file contains:
```
GEMINI_API_KEY=AIzaSyAR1BFvpUr7YbNzIQnVT7T2D-oJeO-lwLA
FLASK_ENV=development
DATABASE_URL=sqlite:///guardian_shield.db
```

3. **Run the Server**
```bash
python app.py
```

The server will start at `http://localhost:5000`

### Quick Start Script
```bash
chmod +x run.sh
./run.sh
```

---

## 🤖 AI Features

### 1. Risk Assessment (Using Gemini AI)
The system uses Google's Gemini Pro model to analyze applications and provide:

**Endpoint**: `POST /api/risk-assessment/<app_id>`

**Features by the Gemini AI:**
- **Risk Score** (0-100): Overall risk assessment
- **Risk Level**: Categorized as Low, Medium, or High
- **Individual Risk Factors**: Specific concerns identified with severity levels
- **Protective Factors**: Positive attributes that mitigate risk
- **Detailed Assessment**: Comprehensive analysis paragraph
- **Recommendations**: Specific guidance for caseworkers
- **Confidence Score**: AI's confidence in its assessment

**Factors Analyzed:**
- Financial stability (income, debt, housing)
- Background checks (legal issues, criminal record)
- Social support (references, welfare history)
- Health and capacity to care

### 2. Intelligent Child Matching (Using Gemini AI)
The system uses Gemini Pro to match guardians with children.

**Endpoints:**
- `GET /api/matching/<app_id>` - Find all potential matches
- `GET /api/matching/<app_id>/<child_id>` - Detailed analysis for a specific match

**Features:**
- **Compatibility Score** (0-100): How well the match fits
- **Match Reasoning**: Explanation of compatibility
- **Strengths**: Positive aspects of the match
- **Potential Challenges**: Areas of concern
- **Support Recommendations**: Services needed for success
- **Overall Recommendation**: Strong/Good/Consider/Not Recommended

**Matching Factors:**
- Age compatibility
- Lifestyle alignment
- Financial capacity
- Special needs matching
- Shared interests and values
- Experience with children

---

## 📡 API Endpoints

### Application Management

**Create Application**
```
POST /api/applications
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "date_of_birth": "1985-03-15",
  "occupation": "Engineer",
  "address": "123 Main St, City",
  "annual_income": 75000,
  "income_stability": "stable",
  "debt_level": "minor",
  "housing_type": "owned",
  "dependents": 2,
  "legal_issues": "none",
  "welfare_history": "no",
  "criminal_record": "no",
  "health_status": "Good",
  "reference_1_name": "Jane Smith",
  "reference_1_contact": "jane@example.com",
  "reference_2_name": "Bob Johnson",
  "reference_2_contact": "bob@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Application created successfully",
  "application_id": "GS-A1B2C3D4",
  "data": { /* full application data */ }
}
```

**List Applications**
```
GET /api/applications?status=pending
```

**Get Application**
```
GET /api/applications/{app_id}
```

**Update Application**
```
PUT /api/applications/{app_id}
Content-Type: application/json

{ /* fields to update */ }
```

### Risk Assessment

**Perform Risk Assessment**
```
POST /api/risk-assessment/{app_id}
```

**Response:**
```json
{
  "success": true,
  "risk_score": 45,
  "risk_level": "medium",
  "risk_factors": [
    {
      "factor": "High debt level",
      "severity": "medium",
      "description": "Applicant has significant debt relative to income"
    }
  ],
  "protective_factors": [
    {
      "factor": "Stable employment",
      "strength": "strong"
    }
  ],
  "assessment": "Detailed analysis...",
  "recommendations": "Specific recommendations...",
  "confidence_score": 0.87
}
```

### Child Matching

**Find All Matches**
```
GET /api/matching/{app_id}
```

**Response:**
```json
{
  "success": true,
  "matches": [
    {
      "child_id": "CH-XXXXX",
      "compatibility_score": 85,
      "match_reasoning": "Strong match due to...",
      "potential_challenges": "...",
      "recommendations": "..."
    }
  ],
  "overall_assessment": "..."
}
```

**Detailed Match Analysis**
```
GET /api/matching/{app_id}/{child_id}
```

**Response:**
```json
{
  "success": true,
  "compatibility_score": 82,
  "match_reasoning": "...",
  "strengths_of_match": ["..."],
  "potential_challenges": ["..."],
  "support_recommendations": ["..."],
  "overall_recommendation": "Good match",
  "confidence_level": 0.89
}
```

### Child Management

**Create Child**
```
POST /api/children
Content-Type: application/json

{
  "name": "Emma Johnson",
  "date_of_birth": "2010-06-20",
  "gender": "Female",
  "health_conditions": "No chronic conditions",
  "behavioral_traits": "Energetic, social",
  "interests": "Sports, reading, music",
  "special_needs": "None",
  "requires_experienced_guardian": false,
  "requires_multilingual": false,
  "requires_physical_accessibility": false
}
```

**List Children**
```
GET /api/children
```

**Get Child**
```
GET /api/children/{child_id}
```

### Decisions & Status

**Record Decision**
```
POST /api/applications/{app_id}/decision
Content-Type: application/json

{
  "decision": "approved",
  "reviewed_by": "Caseworker Name",
  "notes": "Passed all checks. Good fit for programs."
}
```

### Statistics

**Get Stats**
```
GET /api/stats
```

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_applications": 42,
    "approved": 15,
    "rejected": 8,
    "pending": 12,
    "info_needed": 7,
    "total_children": 28
  }
}
```

---

## 🗄️ Database Models

### Application
Stores guardian applicant information and assessment results:
- Personal info (name, email, phone, DOB, occupation)
- Financial details (income, debt, housing)
- Background information (dependents, legal issues, welfare history)
- References (2 available)
- AI Risk Assessment (score, level, factors, assessment)
- Decision status and notes

### Child
Represents children needing guardianship:
- Basic info (name, DOB, age, gender)
- Health and behavioral information
- Special needs and requirements
- Compatibility requirements

### Match
Tracks guardian-child matches:
- Compatibility score
- Match reasoning
- Potential challenges
- Support recommendations
- Match status

---

## 🔑 How Gemini AI Improves the System

### Previous Logic Limitations
The original system (before AI) likely used simple rule-based scoring, such as:
- Fixed point values for each factor
- No contextual understanding
- No nuanced risk consideration
- Generic matching algorithm

### Gemini AI Improvements

**1. Contextual Understanding**
- AI understands relationships between factors
- Recognizes that high income + low debt = better financial picture
- Understands occupation type matters (some jobs have more background check scrutiny)

**2. Nuanced Risk Assessment**
- Identifies compound risk factors
- Considers protective factors that mitigate risk
- Provides detailed reasoning, not just a score
- Recognizes context (e.g., young age isn't automatically disqualifying)

**3. Intelligent Child Matching**
- Analyzes compatibility beyond surface demographics
- Understands behavioral compatibility
- Identifies support needs proactively
- Provides specific, actionable recommendations

**4. Natural Language Explanations**
- Caseworkers understand the "why" behind decisions
- Reduces need for manual analysis
- Enables better decision-making by case workers
- Supports transparency and accountability

---

## 🔐 Security & Privacy

- SQLite database with application data isolation
- Environment variables for sensitive data (API keys)
- No direct exposure of assessment algorithms
- Audit trails for all decisions

## 📊 Example Workflow

1. **Guardian Application Submission**
   ```bash
   curl -X POST http://localhost:5000/api/applications \
     -H "Content-Type: application/json" \
     -d @application.json
   ```

2. **AI Risk Assessment**
   ```bash
   curl -X POST http://localhost:5000/api/risk-assessment/GS-A1B2C3D4
   ```

3. **Find Child Matches**
   ```bash
   curl -X GET http://localhost:5000/api/matching/GS-A1B2C3D4
   ```

4. **Detailed Match Analysis**
   ```bash
   curl -X GET http://localhost:5000/api/matching/GS-A1B2C3D4/CH-XXXXX
   ```

5. **Record Decision**
   ```bash
   curl -X POST http://localhost:5000/api/applications/GS-A1B2C3D4/decision \
     -H "Content-Type: application/json" \
     -d '{"decision": "approved", "reviewed_by": "John Smith"}'
   ```

---

## 🧠 Environment Variables

```
GEMINI_API_KEY          - Google Gemini API key for AI features
FLASK_ENV              - Flask environment (development/production)
DATABASE_URL           - SQLite database location
SECRET_KEY             - Flask session secret key
```

---

## 📝 Notes

- The Gemini API key is configured in `.env`
- SQLite database is auto-created on first run
- All API responses include a `success` boolean and error messages
- Timestamps in ISO 8601 format (UTC)

## 🛠️ Development

To modify risk assessment logic:
1. Edit `ai_service.py` - `AIRiskAssessment` class
2. Modify the prompt in `assess_application()` method

To modify matching logic:
1. Edit `ai_service.py` - `AIMatching` class
2. Modify prompts in `find_best_matches()` or `match_single_child()` methods

---

## 📄 License & Support

This system is designed for child welfare organizations to assist in fair, transparent, and safe guardian selection.

All AI assessments should be reviewed and validated by qualified caseworkers.
