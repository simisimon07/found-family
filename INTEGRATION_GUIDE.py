#!/usr/bin/env python3
"""
INTEGRATION GUIDE: Connecting GuardianShield Frontend to Flask API Backend

This guide shows how to update the existing HTML files to use the new Flask API
with AI-powered risk assessment and child matching.
"""

INTEGRATION_STEPS = """
═══════════════════════════════════════════════════════════════════════════════
                      GUARMIANSHIELD API INTEGRATION GUIDE
                         Frontend-to-Backend Connection
═══════════════════════════════════════════════════════════════════════════════

📋 TABLE OF CONTENTS:
1. API Configuration
2. Updating Apply Form (apply.html)
3. Updating Dashboard (dashboard.html)
4. Updating Risk Analysis (risk.html)
5. Matching System Integration
6. Database Integration
7. Testing & Deployment

═══════════════════════════════════════════════════════════════════════════════
1. API CONFIGURATION
═══════════════════════════════════════════════════════════════════════════════

Add this to your HTML files' <head> section:

<script>
  // API Configuration
  const API_BASE_URL = 'http://localhost:5000/api';
  
  // API Helper Functions
  async function callAPI(endpoint, method = 'GET', data = null) {
    const options = {
      method: method,
      headers: {
        'Content-Type': 'application/json'
      }
    };
    
    if (data) {
      options.body = JSON.stringify(data);
    }
    
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error('API call failed:', error);
      throw error;
    }
  }
</script>

═══════════════════════════════════════════════════════════════════════════════
2. UPDATING APPLY FORM (apply.html)
═══════════════════════════════════════════════════════════════════════════════

REPLACE the form submission logic:

OLD CODE:
app.status = 'pending';
localStorage.setItem('gs_applications', JSON.stringify([app]));

NEW CODE:
async function submitApplication(app) {
  try {
    const response = await callAPI('/applications', 'POST', {
      name: app.name,
      email: app.email,
      phone: app.phone,
      date_of_birth: app.dateOfBirth,
      occupation: app.occupation,
      address: app.address,
      annual_income: parseInt(app.annualIncome),
      income_stability: app.incomeStability,
      debt_level: app.debtLevel,
      housing_type: app.housingType,
      dependents: parseInt(app.dependents),
      legal_issues: app.legalIssues,
      welfare_history: app.welfareHistory,
      criminal_record: app.criminalRecord,
      health_status: app.healthStatus,
      reference_1_name: app.reference1Name,
      reference_1_contact: app.reference1Contact,
      reference_2_name: app.reference2Name,
      reference_2_contact: app.reference2Contact
    });
    
    if (response.success) {
      const appId = response.application_id;
      showToast('✅ Application submitted successfully!');
      
      // Perform AI risk assessment
      evaluateRisk(appId);
      
      // Redirect to dashboard
      setTimeout(() => {
        window.location.href = 'dashboard.html?app=' + appId;
      }, 1500);
    } else {
      showToast('❌ Error: ' + response.error);
    }
  } catch (error) {
    showToast('❌ Submission failed: ' + error.message);
  }
}

// Call this function on form submit:
document.getElementById('applicationForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const app = {
    name: document.getElementById('fullName').value,
    email: document.getElementById('email').value,
    phone: document.getElementById('phone').value,
    dateOfBirth: document.getElementById('dob').value,
    occupation: document.getElementById('occupation').value,
    address: document.getElementById('address').value,
    annualIncome: document.getElementById('annualIncome').value,
    incomeStability: document.querySelector('input[name="incomeStability"]:checked').value,
    debtLevel: document.querySelector('input[name="debtLevel"]:checked').value,
    housingType: document.querySelector('input[name="housing"]:checked').value,
    dependents: document.getElementById('dependents').value,
    legalIssues: document.querySelector('input[name="legalIssues"]:checked').value,
    welfareHistory: document.querySelector('input[name="welfare"]:checked').value,
    criminalRecord: document.querySelector('input[name="criminalBackground"]:checked').value,
    healthStatus: document.getElementById('healthStatus').value,
    reference1Name: document.getElementById('ref1Name').value,
    reference1Contact: document.getElementById('ref1Contact').value,
    reference2Name: document.getElementById('ref2Name').value,
    reference2Contact: document.getElementById('ref2Contact').value
  };
  
  await submitApplication(app);
});


═══════════════════════════════════════════════════════════════════════════════
3. UPDATING DASHBOARD (dashboard.html)
═══════════════════════════════════════════════════════════════════════════════

REPLACE the application listing logic:

OLD CODE:
let apps = JSON.parse(localStorage.getItem('gs_applications') || '[]');

NEW CODE:
async function loadApplications() {
  try {
    const response = await callAPI('/applications');
    if (response.success) {
      const applications = response.data;
      renderApplicationsTable(applications);
    } else {
      showToast('Error loading applications');
    }
  } catch (error) {
    console.error('Failed to load applications:', error);
  }
}

function renderApplicationsTable(applications) {
  const tbody = document.querySelector('#applicationsTable tbody');
  tbody.innerHTML = '';
  
  applications.forEach(app => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${app.name}</td>
      <td>${app.occupation}</td>
      <td><span class="pill pill-${app.status}">${app.status}</span></td>
      <td>${app.risk_score ? app.risk_score + '/100' : 'Not assessed'}</td>
      <td>
        <button onclick="viewApplication('${app.id}')" class="btn-small">View</button>
        <button onclick="performRiskAssessment('${app.id}')" class="btn-small">Assess Risk</button>
        <button onclick="findMatches('${app.id}')" class="btn-small">Find Matches</button>
      </td>
    `;
    tbody.appendChild(row);
  });
}

// Load applications when page loads
loadApplications();

// Refresh applications periodically
setInterval(loadApplications, 30000); // Every 30 seconds


═══════════════════════════════════════════════════════════════════════════════
4. UPDATING RISK ANALYSIS (risk.html)
═══════════════════════════════════════════════════════════════════════════════

REPLACE the risk scoring logic:

OLD CODE:
// Local calculation
let riskScore = 0;
if(app.debt === 'significant') riskScore += 20;
...

NEW CODE:
async function performRiskAssessment(appId) {
  try {
    showToast('🔄 Performing AI risk assessment...');
    
    const response = await callAPI(`/risk-assessment/${appId}`, 'POST');
    
    if (response.success) {
      displayRiskAssessment(response);
      updateApplicationStatus(appId, 'risk_assessed');
      showToast('✅ Risk assessment completed!');
    } else {
      showToast('❌ Risk assessment failed: ' + response.error);
    }
  } catch (error) {
    showToast('❌ Error: ' + error.message);
  }
}

function displayRiskAssessment(assessment) {
  // Update risk score circle
  document.getElementById('scoreNum').textContent = Math.round(assessment.risk_score);
  
  const colorClass = assessment.risk_level === 'high' ? 'circle-high' :
                    assessment.risk_level === 'medium' ? 'circle-medium' : 'circle-low';
  
  const circle = document.getElementById('circleFill');
  circle.className.baseVal = 'circle-fill ' + colorClass;
  
  // Update factor list
  const factorList = document.getElementById('factorList');
  factorList.innerHTML = '';
  
  assessment.risk_factors.forEach(factor => {
    const factorDiv = document.createElement('div');
    factorDiv.className = 'factor-row';
    factorDiv.innerHTML = `
      <div class="factor-icon ${factor.severity}">
        ${factor.severity === 'high' ? '⚠️' : factor.severity === 'medium' ? '⚡' : '✓'}
      </div>
      <div class="factor-name">
        <strong>${factor.factor}</strong>
        <span>${factor.description}</span>
      </div>
      <div class="factor-pill pill-${factor.severity}">
        ${factor.severity}
      </div>
    `;
    factorList.appendChild(factorDiv);
  });
  
  // Update assessment text
  document.getElementById('assessmentText').innerHTML = assessment.assessment;
  
  // Show confidence
  const confidencePercent = (assessment.confidence_score * 100).toFixed(0);
  document.getElementById('confidenceScore').textContent = confidencePercent + '%';
}


═══════════════════════════════════════════════════════════════════════════════
5. MATCHING SYSTEM INTEGRATION
═══════════════════════════════════════════════════════════════════════════════

Add a new "Matching" section to dashboard.html:

<div class="card">
  <div class="card-title">👨‍👧 Child Matching (AI Powered)</div>
  <div id="matchingResults"></div>
</div>

Then add this JavaScript:

async function findMatches(appId) {
  try {
    showToast('🔄 Finding AI matches...');
    
    const response = await callAPI(`/matching/${appId}`);
    
    if (response.success) {
      displayMatches(response.matches, appId);
      showToast('✅ Matching completed!');
    } else {
      showToast('❌ Matching failed: ' + response.error);
    }
  } catch (error) {
    showToast('❌ Error: ' + error.message);
  }
}

function displayMatches(matches, appId) {
  const container = document.getElementById('matchingResults');
  container.innerHTML = '';
  
  if (matches.length === 0) {
    container.innerHTML = '<p>No matches found</p>';
    return;
  }
  
  const matchGrid = document.createElement('div');
  matchGrid.className = 'grid-2';
  
  matches.slice(0, 5).forEach(match => {
    const matchCard = document.createElement('div');
    matchCard.className = 'card match-card';
    matchCard.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: start;">
        <div>
          <strong style="display: block; margin-bottom: 0.5rem;">Child ID: ${match.child_id}</strong>
          <div class="score-display" style="font-size: 2rem; color: var(--accent);">
            ${match.compatibility_score}%
          </div>
          <p style="font-size: 0.8rem; color: var(--muted); margin-top: 0.5rem;">
            Compatibility Score
          </p>
        </div>
        <button onclick="getDetailedMatch('${appId}', '${match.child_id}')" class="btn-small">
          View Details
        </button>
      </div>
      <p style="margin-top: 1rem; font-size: 0.9rem;">
        ${match.match_reasoning}
      </p>
    `;
    matchGrid.appendChild(matchCard);
  });
  
  container.appendChild(matchGrid);
}

async function getDetailedMatch(appId, childId) {
  try {
    const response = await callAPI(`/matching/${appId}/${childId}`);
    
    if (response.success) {
      displayDetailedMatchModal(response);
    } else {
      showToast('Error loading match details: ' + response.error);
    }
  } catch (error) {
    showToast('Error: ' + error.message);
  }
}


═══════════════════════════════════════════════════════════════════════════════
6. DATABASE INTEGRATION
═══════════════════════════════════════════════════════════════════════════════

The Flask API automatically manages the SQLite database. No frontend changes needed.
Data is persisted on the backend, not in localStorage.

Advantages:
✓ Data survives browser refresh
✓ Multiple users can access same data
✓ Full audit trail in database
✓ Scalable to production database


═══════════════════════════════════════════════════════════════════════════════
7. TESTING & DEPLOYMENT
═══════════════════════════════════════════════════════════════════════════════

Testing:
1. Start Flask API:
   python3 app.py

2. Open test page in browser:
   python3 test_api.py
   
3. Or use curl to test endpoints:
   curl http://localhost:5000/api/health

Deployment:
1. Set FLASK_ENV=production in .env
2. Use production database (PostgreSQL recommended)
3. Enable CORS properly for your domain
4. Use HTTPS in production
5. Set strong SECRET_KEY
6. Use gunicorn or similar WSGI server

Example deployment command:
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app


═══════════════════════════════════════════════════════════════════════════════
KEY IMPROVEMENTS WITH GEMINI AI
═══════════════════════════════════════════════════════════════════════════════

1. RISK ASSESSMENT
   Before: Simple rule-based scoring (add/subtract points)
   After: Contextual AI analysis considering all factors together
   
2. CHILD MATCHING
   Before: Simple demographic matching
   After: Deep compatibility analysis with reasoning

3. RECOMMENDATIONS
   Before: Generic approval/rejection
   After: Specific, actionable guidance for caseworkers

4. TRANSPARENCY
   Before: Black-box scoring
   After: Clear explanation of AI reasoning
"""

print(INTEGRATION_STEPS)
