#!/usr/bin/env python3
"""
Sample data and examples for GuardianShield Flask API
Shows how to use all endpoints with real data examples
"""

# EXAMPLE 1: Creating a Guardian Application
CREATE_APP_EXAMPLE = {
    "name": "Sarah Johnson",
    "email": "sarah.johnson@example.com",
    "phone": "+1 (555) 123-4567",
    "date_of_birth": "1985-06-15",
    "occupation": "Clinical Social Worker",
    "address": "742 Elm Street, Portland, OR 97214",
    "annual_income": 65000,
    "income_stability": "stable",
    "debt_level": "minor",
    "housing_type": "owned",
    "dependents": 1,
    "legal_issues": "none",
    "welfare_history": "no",
    "criminal_record": "no",
    "health_status": "Excellent health, very active",
    "reference_1_name": "Dr. Michael Patterson",
    "reference_1_contact": "m.patterson@clinic.org",
    "reference_2_name": "Teresa Martinez",
    "reference_2_contact": "t.martinez@community.org"
}

# EXAMPLE 2: Creating a Child Record
CREATE_CHILD_EXAMPLE = {
    "name": "James Okonkwo",
    "date_of_birth": "2012-04-08",
    "gender": "Male",
    "health_conditions": "No known health conditions, up to date on vaccinations",
    "behavioral_traits": "Sociable, likes teamwork, good at problem-solving",
    "interests": "Soccer, robotics, video games, science experiments",
    "special_needs": "None",
    "requires_experienced_guardian": False,
    "requires_multilingual": False,
    "requires_physical_accessibility": False
}

# EXAMPLE 3: Risk Assessment Output (AI Generated)
RISK_ASSESSMENT_EXAMPLE = {
    "success": True,
    "risk_score": 32,
    "risk_level": "low",
    "risk_factors": [
        {
            "factor": "Single parent household",
            "severity": "low",
            "description": "Applicant is single. Should ensure adequate support network."
        },
        {
            "factor": "Minor debt",
            "severity": "low",
            "description": "Some debt but well-managed relative to income"
        }
    ],
    "protective_factors": [
        {
            "factor": "Stable employment",
            "strength": "strong",
            "description": "12+ years in same profession"
        },
        {
            "factor": "Professional background",
            "strength": "strong",
            "description": "Social work training provides child development knowledge"
        },
        {
            "factor": "Strong references",
            "strength": "strong",
            "description": "Two professional references available"
        },
        {
            "factor": "Stable housing",
            "strength": "strong",
            "description": "Owned home in established neighborhood"
        }
    ],
    "assessment": "Applicant presents a low-risk profile with strong protective factors. Professional background in social work suggests good understanding of trauma-informed care and child development. Stable employment and housing provide a strong foundation. The single-parent status is not a concern given the applicant's professional qualifications and strong support network.",
    "recommendations": "Approve for next stage of screening. Conduct home visit to assess physical environment and neighborhood. Verify references thoroughly. Discuss post-placement support services.",
    "confidence_score": 0.91
}

# EXAMPLE 4: Child Matching Output (AI Generated)
CHILD_MATCHING_EXAMPLE = {
    "success": True,
    "matches": [
        {
            "child_id": "CH-7F3B2A",
            "compatibility_score": 88,
            "match_reasoning": "Excellent match. Applicant's professional background in social work aligns well with child's need for emotionally supportive guardian. Both interested in sports and science activities. Applicant has space in household and resources for child's needs.",
            "potential_challenges": "Applicant currently works full-time. May need to arrange after-school care for child. Verify that applicant can manage professional and caregiving responsibilities.",
            "recommendations": "Discuss work schedule and childcare arrangements. Consider summer programs and mentoring opportunities related to soccer and robotics."
        },
        {
            "child_id": "CH-5D8C4E",
            "compatibility_score": 75,
            "match_reasoning": "Good match. Child with behavioral challenges would benefit from applicant's social work expertise and structured approach. Adequate resources and stable environment.",
            "potential_challenges": "Child may require significant emotional support during transition. Applicant will need training on specific behavioral management for this child's background.",
            "recommendations": "Recommend pre-placement counseling for both. Provide training on trauma-informed parenting. Establish post-placement follow-up schedule."
        }
    ],
    "overall_assessment": "Applicant is well-suited to provide stable, nurturing care. Professional qualifications in social work provide added confidence in child welfare. Strong consideration for placement with children needing emotional support and structure."
}

# EXAMPLE 5: Detailed Match Analysis (AI Generated)
DETAILED_MATCH_EXAMPLE = {
    "success": True,
    "compatibility_score": 88,
    "match_reasoning": "This is a strong match based on multiple compatibility factors. The applicant's background in social work and child development aligns well with the child's needs. Both share interests in sports and educational activities. The applicant has demonstrated ability to create a stable, supportive home environment.",
    "strengths_of_match": [
        "Applicant's social work background provides child development expertise",
        "Stable employment and housing create secure environment",
        "Shared interests in sports and science activities",
        "Adequate financial resources for child's needs",
        "Strong professional and community references",
        "Applicant demonstrates commitment to ongoing learning"
    ],
    "potential_challenges": [
        "Single parent managing full-time work - need for quality childcare",
        "Limited extended family support - need to build local networks",
        "Child adjusted to previous guardian - manage transition carefully"
    ],
    "support_recommendations": [
        "Weekly post-placement check-ins for first 3 months",
        "Connect with local parent support groups",
        "Arrange counseling for child to process transition",
        "Enroll in evidence-based parenting program",
        "Connect with mentoring organization for additional support",
        "Annual competency assessments"
    ],
    "overall_recommendation": "Strong recommendation - Proceed with placement",
    "confidence_level": 0.91
}

# EXAMPLE 6: API Call Examples

API_EXAMPLES = """
# 1. CREATE A NEW APPLICATION
curl -X POST http://localhost:5000/api/applications \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Sarah Johnson",
    "email": "sarah@example.com",
    "phone": "+1 555 123-4567",
    "date_of_birth": "1985-06-15",
    "occupation": "Social Worker",
    "address": "742 Elm Street, Portland, OR",
    "annual_income": 65000,
    "income_stability": "stable",
    "debt_level": "minor",
    "housing_type": "owned",
    "dependents": 1,
    "legal_issues": "none",
    "welfare_history": "no",
    "criminal_record": "no",
    "health_status": "Excellent",
    "reference_1_name": "Dr. Patterson",
    "reference_1_contact": "dr@example.com",
    "reference_2_name": "Teresa Martinez",
    "reference_2_contact": "teresa@example.com"
  }'

Response:
{
  "success": true,
  "message": "Application created successfully",
  "application_id": "GS-A1B2C3D4",
  "data": { ... full application data ... }
}


# 2. LIST ALL APPLICATIONS
curl -X GET "http://localhost:5000/api/applications?status=pending"

Response:
{
  "success": true,
  "count": 5,
  "data": [
    { "id": "GS-A1B2C3D4", "name": "Sarah Johnson", "status": "pending", ... },
    ...
  ]
}


# 3. PERFORM AI RISK ASSESSMENT
curl -X POST http://localhost:5000/api/risk-assessment/GS-A1B2C3D4

Response:
{
  "success": true,
  "risk_score": 32,
  "risk_level": "low",
  "risk_factors": [ ... ],
  "protective_factors": [ ... ],
  "assessment": "Detailed analysis from Gemini AI...",
  "recommendations": "Recommendations from AI...",
  "confidence_score": 0.91
}


# 4. CREATE A CHILD RECORD
curl -X POST http://localhost:5000/api/children \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "James Okonkwo",
    "date_of_birth": "2012-04-08",
    "gender": "Male",
    "health_conditions": "None",
    "behavioral_traits": "Sociable, good at problem-solving",
    "interests": "Soccer, robotics, science",
    "special_needs": "None",
    "requires_experienced_guardian": false
  }'

Response:
{
  "success": true,
  "message": "Child record created successfully",
  "child_id": "CH-XXXXX",
  "data": { ... child data ... }
}


# 5. FIND MATCHING CHILDREN (AI POWERED)
curl -X GET http://localhost:5000/api/matching/GS-A1B2C3D4

Response:
{
  "success": true,
  "matches": [
    {
      "child_id": "CH-7F3B2A",
      "compatibility_score": 88,
      "match_reasoning": "Excellent match because...",
      "potential_challenges": "...",
      "recommendations": "..."
    },
    ...
  ],
  "overall_assessment": "Assessment from Gemini AI..."
}


# 6. GET DETAILED MATCH ANALYSIS
curl -X GET http://localhost:5000/api/matching/GS-A1B2C3D4/CH-7F3B2A

Response:
{
  "success": true,
  "compatibility_score": 88,
  "match_reasoning": "Detailed reasoning...",
  "strengths_of_match": ["...", "..."],
  "potential_challenges": ["...", "..."],
  "support_recommendations": ["...", "..."],
  "overall_recommendation": "Strong recommendation",
  "confidence_level": 0.91
}


# 7. RECORD A DECISION
curl -X POST http://localhost:5000/api/applications/GS-A1B2C3D4/decision \\
  -H "Content-Type: application/json" \\
  -d '{
    "decision": "approved",
    "reviewed_by": "Jane Smith, Case Manager",
    "notes": "Applicant passed all checks. Good match for available children."
  }'

Response:
{
  "success": true,
  "message": "Decision recorded: approved",
  "data": { ... updated application ... }
}


# 8. GET SYSTEM STATISTICS
curl -X GET http://localhost:5000/api/stats

Response:
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


# 9. HEALTH CHECK
curl -X GET http://localhost:5000/api/health

Response:
{
  "success": true,
  "status": "API is running",
  "timestamp": "2024-02-20T10:30:45.123456"
}
"""

print(__doc__)
print(API_EXAMPLES)
