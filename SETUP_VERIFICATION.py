#!/usr/bin/env python3
"""
SETUP VERIFICATION & TROUBLESHOOTING GUIDE
GuardianShield Flask API with Gemini AI

This script helps verify your installation is correct and troubleshoots issues.
"""

import sys
import subprocess
import json
from pathlib import Path

class SetupValidator:
    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.warnings = []
        
    def print_header(self, text):
        print(f"\n{'='*70}")
        print(f"  {text}")
        print(f"{'='*70}\n")
    
    def check(self, name, condition, error_msg=""):
        if condition:
            print(f"✅ {name}")
            self.checks_passed += 1
            return True
        else:
            print(f"❌ {name}")
            if error_msg:
                print(f"   Error: {error_msg}")
            self.checks_failed += 1
            return False
    
    def warning(self, msg):
        print(f"⚠️  {msg}")
        self.warnings.append(msg)
    
    def verify_python(self):
        self.print_header("1. Python Environment")
        
        # Check Python version
        version = sys.version_info
        version_str = f"{version.major}.{version.minor}.{version.micro}"
        has_python38_plus = version.major > 3 or (version.major == 3 and version.minor >= 8)
        self.check("Python 3.8+", has_python38_plus, 
                   f"Current: Python {version_str}")
        return has_python38_plus
    
    def verify_dependencies(self):
        self.print_header("2. Required Dependencies")
        
        dependencies = [
            ('flask', 'Flask'),
            ('flask_sqlalchemy', 'Flask-SQLAlchemy'),
            ('flask_cors', 'Flask-CORS'),
            ('dotenv', 'python-dotenv'),
            ('google.generativeai', 'google-generativeai'),
            ('requests', 'requests'),
        ]
        
        deps_ok = True
        for import_name, display_name in dependencies:
            try:
                __import__(import_name)
                self.check(f"{display_name}", True)
            except ImportError:
                self.check(f"{display_name}", False, 
                          f"Run: pip install {display_name}")
                deps_ok = False
        
        return deps_ok
    
    def verify_files(self):
        self.print_header("3. Application Files")
        
        required_files = [
            'app.py',
            'models.py',
            'ai_service.py',
            '.env',
            'requirements.txt',
            'apply.html',
            'dashboard.html',
            'risk.html',
        ]
        
        files_ok = True
        for file in required_files:
            exists = Path(file).exists()
            self.check(f"File: {file}", exists)
            if not exists:
                files_ok = False
        
        return files_ok
    
    def verify_env(self):
        self.print_header("4. Environment Configuration")
        
        env_file = Path('.env')
        if not env_file.exists():
            self.check(".env file exists", False, "Create .env file with API key")
            return False
        
        self.check(".env file exists", True)
        
        # Check contents
        env_content = env_file.read_text()
        
        has_api_key = 'GEMINI_API_KEY' in env_content
        self.check("GEMINI_API_KEY configured", has_api_key)
        
        has_flask_env = 'FLASK_ENV' in env_content
        self.check("FLASK_ENV configured", has_flask_env)
        
        has_db_url = 'DATABASE_URL' in env_content
        self.check("DATABASE_URL configured", has_db_url)
        
        if has_api_key and 'AIzaSy' not in env_content:
            self.warning("GEMINI_API_KEY is configured but might not be valid")
        
        return has_api_key and has_flask_env and has_db_url
    
    def verify_api_structure(self):
        self.print_header("5. API Structure")
        
        # Check Flask app
        try:
            with open('app.py', 'r') as f:
                app_content = f.read()
            
            endpoints = [
                ('POST /api/applications', "create_application"),
                ('GET /api/applications', "list_applications"),
                ('POST /api/risk-assessment', "assess_risk"),
                ('GET /api/matching', "find_matches"),
                ('POST /api/children', "create_child"),
            ]
            
            endpoints_ok = True
            for endpoint, function in endpoints:
                has_endpoint = function in app_content
                self.check(f"Endpoint: {endpoint}", has_endpoint)
                if not has_endpoint:
                    endpoints_ok = False
            
            return endpoints_ok
        except Exception as e:
            self.check("API structure", False, str(e))
            return False
    
    def verify_ai_service(self):
        self.print_header("6. AI Service Integration")
        
        try:
            with open('ai_service.py', 'r') as f:
                ai_content = f.read()
            
            has_risk_class = 'AIRiskAssessment' in ai_content
            self.check("AIRiskAssessment class", has_risk_class)
            
            has_matching_class = 'AIMatching' in ai_content
            self.check("AIMatching class", has_matching_class)
            
            has_gemini = 'genai.GenerativeModel' in ai_content
            self.check("Gemini API integration", has_gemini)
            
            has_prompts = 'prompt =' in ai_content
            self.check("AI prompts configured", has_prompts)
            
            return has_risk_class and has_matching_class and has_gemini
        except Exception as e:
            self.check("AI service", False, str(e))
            return False
    
    def verify_database(self):
        self.print_header("7. Database Setup")
        
        try:
            from models import db, Application, Child, Match
            self.check("Database models importable", True)
            
            # Check if database file would be created
            db_path = Path('guardian_shield.db')
            if db_path.exists():
                self.check("Database file exists", True)
            else:
                self.warning("Database file will be created on first run")
            
            return True
        except Exception as e:
            self.check("Database models", False, str(e))
            return False
    
    def generate_report(self):
        self.print_header("SETUP VERIFICATION REPORT")
        
        print(f"Checks Passed: {self.checks_passed} ✅")
        print(f"Checks Failed: {self.checks_failed} ❌")
        print(f"Warnings: {len(self.warnings)} ⚠️\n")
        
        if self.checks_failed == 0:
            print("🎉 All checks passed! Your setup is ready.")
            print("\nTo start the Flask API server:")
            print("  python3 app.py")
            print("\nTo test the API:")
            print("  python3 test_api.py")
            return True
        else:
            print("❌ Some checks failed. See errors above.")
            print("\nCommon fixes:")
            print("  1. Install dependencies: pip install -r requirements.txt")
            print("  2. Create .env file with GEMINI_API_KEY")
            print("  3. Ensure all required files are present")
            return False
    
    def run_all_checks(self):
        print(r"""
╔════════════════════════════════════════════════════════════════════╗
║         GuardianShield - Setup Verification & Troubleshooting      ║
║                    Powered by Gemini AI                            ║
╚════════════════════════════════════════════════════════════════════╝
        """)
        
        self.verify_python()
        self.verify_dependencies()
        self.verify_files()
        self.verify_env()
        self.verify_api_structure()
        self.verify_ai_service()
        self.verify_database()
        
        return self.generate_report()


def main():
    validator = SetupValidator()
    success = validator.run_all_checks()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

"""
TROUBLESHOOTING GUIDE

Problem: "ModuleNotFoundError: No module named 'flask'"
Solution: pip install -r requirements.txt

Problem: "GEMINI_API_KEY is not configured"
Solution: 
  1. Create .env file in project root
  2. Add: GEMINI_API_KEY=AIzaSyAR1BFvpUr7YbNzIQnVT7T2D-oJeO-lwLA
  3. Save and restart Flask

Problem: "Port 5000 already in use"
Solution: 
  1. Kill existing process: lsof -i :5000
  2. Or change port in app.py: app.run(port=5001)

Problem: "Database locked" error
Solution:
  1. Stop all Flask instances
  2. Delete guardian_shield.db
  3. Restart Flask to recreate database

Problem: "API returns 404 on endpoints"
Solution:
  1. Check endpoint paths are correct
  2. Verify Content-Type: application/json header
  3. Check FLASK_ENV=development in .env

Problem: "Gemini AI returns errors"
Solution:
  1. Verify API key is correct
  2. Check internet connection
  3. Ensure google-generativeai is installed
  4. Check Gemini API is available in your region

Problem: "CORS errors when calling from frontend"
Solution:
  1. Verify Flask-CORS is installed
  2. Check API_BASE_URL in frontend matches server
  3. Ensure CORS(app) is called in app.py

For more help, check:
- README.md - Project overview
- FLASK_API_README.md - Complete API documentation
- INTEGRATION_GUIDE.py - Frontend integration instructions
"""
