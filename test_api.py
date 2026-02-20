#!/usr/bin/env python3
"""
Test script for GuardianShield Flask API
Demonstrates each endpoint and the AI features
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000/api"

# Colors for terminal output
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
END = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}{END}")
    print(f"{BLUE}{text:^60}{END}")
    print(f"{BLUE}{'='*60}{END}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{END}")

def print_error(text):
    print(f"{RED}✗ {text}{END}")

def print_info(text):
    print(f"{YELLOW}ℹ {text}{END}")

def test_create_applications():
    """Test creating guardian applications"""
    print_header("Testing: Create Guardian Applications")
    
    test_apps = [
        {
            "name": "Rajesh Kumar",
            "email": "rajesh@example.com",
            "phone": "+91 98765 43210",
            "date_of_birth": "1980-05-15",
            "occupation": "Sales Executive",
            "address": "123 Main Street, Mumbai, India 400001",
            "annual_income": 45000,
            "income_stability": "stable",
            "debt_level": "significant",
            "housing_type": "rented",
            "dependents": 2,
            "legal_issues": "minor",
            "welfare_history": "yes",
            "criminal_record": "no",
            "health_status": "Good health, occasional migraine",
            "reference_1_name": "Priya Sharma",
            "reference_1_contact": "priya@example.com",
            "reference_2_name": "Amit Patel",
            "reference_2_contact": "amit@example.com"
        },
        {
            "name": "Sarah Williams",
            "email": "sarah@example.com",
            "phone": "+1 555 123 4567",
            "date_of_birth": "1990-08-22",
            "occupation": "Software Engineer",
            "address": "456 Oak Avenue, San Francisco, CA 94102",
            "annual_income": 120000,
            "income_stability": "stable",
            "debt_level": "minor",
            "housing_type": "owned",
            "dependents": 0,
            "legal_issues": "none",
            "welfare_history": "no",
            "criminal_record": "no",
            "health_status": "Excellent health",
            "reference_1_name": "Michael Chen",
            "reference_1_contact": "michael@example.com",
            "reference_2_name": "Lisa Anderson",
            "reference_2_contact": "lisa@example.com"
        }
    ]
    
    app_ids = []
    for app_data in test_apps:
        try:
            response = requests.post(f"{BASE_URL}/applications", json=app_data)
            if response.status_code == 201:
                result = response.json()
                app_id = result['application_id']
                app_ids.append(app_id)
                print_success(f"Created application for {app_data['name']}")
                print(f"   Application ID: {app_id}\n")
            else:
                print_error(f"Failed to create application: {response.text}")
        except Exception as e:
            print_error(f"Error: {str(e)}")
    
    return app_ids

def test_list_applications():
    """Test listing applications"""
    print_header("Testing: List All Applications")
    
    try:
        response = requests.get(f"{BASE_URL}/applications")
        if response.status_code == 200:
            result = response.json()
            print_success(f"Retrieved {result['count']} applications")
            for app in result['data'][:2]:  # Show first 2
                print(f"  - {app['name']} ({app['id']}): Status = {app['status']}")
        else:
            print_error(f"Failed to retrieve applications: {response.text}")
    except Exception as e:
        print_error(f"Error: {str(e)}")

def test_risk_assessment(app_ids):
    """Test AI risk assessment"""
    print_header("Testing: AI Risk Assessment with Gemini")
    
    for app_id in app_ids[:1]:  # Test first app
        try:
            print_info(f"Analyzing risk for application {app_id}...")
            response = requests.post(f"{BASE_URL}/risk-assessment/{app_id}")
            
            if response.status_code == 200:
                result = response.json()
                print_success("Risk assessment completed!")
                print(f"  Risk Score: {result['risk_score']}/100")
                print(f"  Risk Level: {result['risk_level']}")
                print(f"  Confidence: {result['confidence_score']:.1%}")
                print(f"\n  Risk Factors:")
                for factor in result['risk_factors'][:3]:
                    print(f"    • {factor.get('factor', 'Unknown')}")
                print(f"\n  Assessment Summary:")
                print(f"    {result['assessment'][:200]}...")
            else:
                print_error(f"Risk assessment failed: {response.text}")
        except Exception as e:
            print_error(f"Error: {str(e)}")

def test_create_children():
    """Test creating child records"""
    print_header("Testing: Create Child Records")
    
    test_children = [
        {
            "name": "Arjun Sharma",
            "date_of_birth": "2015-03-10",
            "gender": "Male",
            "health_conditions": "No chronic conditions",
            "behavioral_traits": "Outgoing, likes sports and music",
            "interests": "Cricket, computers, drawing",
            "special_needs": "None",
            "requires_experienced_guardian": False,
            "requires_multilingual": False,
            "requires_physical_accessibility": False
        },
        {
            "name": "Zara Ahmed",
            "date_of_birth": "2008-07-22",
            "gender": "Female",
            "health_conditions": "Asthma, well-controlled",
            "behavioral_traits": "Quiet, thoughtful, loves reading",
            "interests": "Books, science, art",
            "special_needs": "Requires supportive environment",
            "requires_experienced_guardian": True,
            "requires_multilingual": False,
            "requires_physical_accessibility": False
        }
    ]
    
    child_ids = []
    for child_data in test_children:
        try:
            response = requests.post(f"{BASE_URL}/children", json=child_data)
            if response.status_code == 201:
                result = response.json()
                child_id = result['child_id']
                child_ids.append(child_id)
                print_success(f"Created child record for {child_data['name']}")
                print(f"   Child ID: {child_id}\n")
            else:
                print_error(f"Failed to create child: {response.text}")
        except Exception as e:
            print_error(f"Error: {str(e)}")
    
    return child_ids

def test_matching(app_ids, child_ids):
    """Test AI-powered child matching"""
    print_header("Testing: AI Child Matching with Gemini")
    
    if not app_ids or not child_ids:
        print_info("Skipping matching test - need both applications and children")
        return
    
    try:
        print_info(f"Finding matches for application {app_ids[0]}...")
        response = requests.get(f"{BASE_URL}/matching/{app_ids[0]}")
        
        if response.status_code == 200:
            result = response.json()
            matches = result.get('matches', [])
            print_success("Matching analysis completed!")
            print(f"\n  Found {len(matches)} potential matches:")
            
            if matches:
                top_match = matches[0]
                print(f"\n  Top Match:")
                print(f"    Child ID: {top_match['child_id']}")
                print(f"    Compatibility: {top_match['compatibility_score']}/100")
                print(f"    Reasoning: {top_match['match_reasoning'][:100]}...")
                
                # Test detailed match for top match
                print_info(f"Getting detailed analysis for top match...")
                detailed_response = requests.get(
                    f"{BASE_URL}/matching/{app_ids[0]}/{top_match['child_id']}"
                )
                if detailed_response.status_code == 200:
                    detailed = detailed_response.json()
                    print_success("Detailed match analysis retrieved!")
                    print(f"    Overall Recommendation: {detailed['overall_recommendation']}")
                    print(f"    Confidence Level: {detailed['confidence_level']:.1%}")
        else:
            print_error(f"Matching failed: {response.text}")
    except Exception as e:
        print_error(f"Error: {str(e)}")

def test_get_stats():
    """Test system statistics"""
    print_header("Testing: Get System Statistics")
    
    try:
        response = requests.get(f"{BASE_URL}/stats")
        if response.status_code == 200:
            result = response.json()
            stats = result['stats']
            print_success("Statistics retrieved!")
            print(f"  Total Applications: {stats['total_applications']}")
            print(f"    ├─ Approved: {stats['approved']}")
            print(f"    ├─ Rejected: {stats['rejected']}")
            print(f"    ├─ Pending: {stats['pending']}")
            print(f"    └─ Info Needed: {stats['info_needed']}")
            print(f"  Total Children: {stats['total_children']}")
        else:
            print_error(f"Failed to get stats: {response.text}")
    except Exception as e:
        print_error(f"Error: {str(e)}")

def test_health_check():
    """Test API health"""
    print_header("Testing: API Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print_success("API is healthy and running!")
        else:
            print_error(f"API returned status {response.status_code}")
    except Exception as e:
        print_error(f"Cannot reach API: {str(e)}")
        return False
    return True

def main():
    """Run all tests"""
    print(f"{BLUE}")
    print(r"""
    ╔═══════════════════════════════════════════════╗
    ║     GuardianShield - Flask API Test Suite     ║
    ║           Powered by Gemini AI                ║
    ╚═══════════════════════════════════════════════╝
    """)
    print(f"{END}")
    
    # Check API is running
    if not test_health_check():
        print("\n" + RED + "START THE FLASK API FIRST: python app.py" + END)
        return
    
    # Run tests
    app_ids = test_create_applications()
    test_list_applications()
    test_risk_assessment(app_ids)
    
    child_ids = test_create_children()
    test_matching(app_ids, child_ids)
    
    test_get_stats()
    
    # Final summary
    print_header("Test Summary")
    print(GREEN + "All tests completed! Check the API responses above." + END)
    print("\n" + YELLOW + "Key Features Tested:" + END)
    print(f"  ✓ Application creation")
    print(f"  ✓ Application listing")
    print(f"  ✓ Gemini AI Risk Assessment")
    print(f"  ✓ Child record creation")
    print(f"  ✓ Gemini AI Child Matching")
    print(f"  ✓ System statistics")
    print("\n" + BLUE + "Next Steps:" + END)
    print(f"  1. Integrate API with frontend (HTML/JS)")
    print(f"  2. Update dashboard to call /api/applications")
    print(f"  3. Update risk.html to call /api/risk-assessment/{id}")
    print(f"  4. Update matching to call /api/matching/{id}")
    print()

if __name__ == "__main__":
    main()
