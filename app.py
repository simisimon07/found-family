from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from datetime import datetime, date
import json
import os
from dotenv import load_dotenv

from models import db, Application, Child, Match
from ai_service import AIRiskAssessment, AIMatching

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///guardian_shield.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

# Initialize database
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()


# Serve frontend static files (SPA fallback)
from flask import send_from_directory


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    static_dir = os.path.join(app.root_path, 'static')
    # If the requested file exists in static, serve it directly
    full_path = os.path.join(static_dir, path)
    if path and os.path.exists(full_path):
        return send_from_directory(static_dir, path)
    # Otherwise serve index.html (SPA fallback)
    return send_from_directory(static_dir, 'index.html')


# ============= UTILITY FUNCTIONS =============

def calculate_age(birth_date):
    """Calculate age from date of birth."""
    if isinstance(birth_date, str):
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


# ============= APPLICATION ENDPOINTS =============

@app.route('/api/applications', methods=['POST'])
def create_application():
    """Create a new guardian application."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('email'):
            return jsonify({'success': False, 'error': 'Name and email are required'}), 400
        
        # Convert date strings to date objects
        dob = None
        if data.get('date_of_birth'):
            if isinstance(data['date_of_birth'], str):
                dob = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
            else:
                dob = data['date_of_birth']
        
        # Create application
        application = Application(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            date_of_birth=dob,
            occupation=data.get('occupation'),
            address=data.get('address'),
            annual_income=data.get('annual_income'),
            income_stability=data.get('income_stability'),
            debt_level=data.get('debt_level'),
            housing_type=data.get('housing_type'),
            dependents=data.get('dependents', 0),
            legal_issues=data.get('legal_issues'),
            welfare_history=data.get('welfare_history'),
            criminal_record=data.get('criminal_record'),
            health_status=data.get('health_status'),
            reference_1_name=data.get('reference_1_name'),
            reference_1_contact=data.get('reference_1_contact'),
            reference_2_name=data.get('reference_2_name'),
            reference_2_contact=data.get('reference_2_contact'),
        )
        
        db.session.add(application)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Application created successfully',
            'application_id': application.id,
            'data': application.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/applications/<app_id>', methods=['GET'])
def get_application(app_id):
    """Retrieve a specific application by ID."""
    try:
        application = Application.query.get(app_id)
        
        if not application:
            return jsonify({'success': False, 'error': 'Application not found'}), 404
        
        return jsonify({
            'success': True,
            'data': application.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/applications', methods=['GET'])
def list_applications():
    """List all applications with optional filtering."""
    try:
        status = request.args.get('status')
        
        query = Application.query
        if status:
            query = query.filter_by(status=status)
        
        applications = query.all()
        
        return jsonify({
            'success': True,
            'count': len(applications),
            'data': [app.to_dict() for app in applications]
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/applications/<app_id>', methods=['PUT'])
def update_application(app_id):
    """Update an existing application."""
    try:
        application = Application.query.get(app_id)
        
        if not application:
            return jsonify({'success': False, 'error': 'Application not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        updatable_fields = [
            'name', 'email', 'phone', 'occupation', 'address',
            'annual_income', 'income_stability', 'debt_level', 'housing_type',
            'dependents', 'legal_issues', 'welfare_history', 'criminal_record',
            'health_status', 'reference_1_name', 'reference_1_contact',
            'reference_2_name', 'reference_2_contact', 'notes'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(application, field, data[field])
        
        application.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Application updated successfully',
            'data': application.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ============= RISK ASSESSMENT ENDPOINTS =============

@app.route('/api/risk-assessment/<app_id>', methods=['POST'])
def assess_risk(app_id):
    """Perform AI-based risk assessment for an application."""
    try:
        application = Application.query.get(app_id)
        
        if not application:
            return jsonify({'success': False, 'error': 'Application not found'}), 404
        
        # Prepare application data
        app_data = {
            'name': application.name,
            'age': calculate_age(application.date_of_birth) if application.date_of_birth else None,
            'occupation': application.occupation,
            'annual_income': application.annual_income,
            'income_stability': application.income_stability,
            'housing_type': application.housing_type,
            'dependents': application.dependents,
            'debt_level': application.debt_level,
            'legal_issues': application.legal_issues,
            'criminal_record': application.criminal_record,
            'welfare_history': application.welfare_history,
            'health_status': application.health_status,
            'reference_1_name': application.reference_1_name,
            'reference_2_name': application.reference_2_name,
        }
        
        # Get AI assessment
        assessment = AIRiskAssessment.assess_application(app_data)
        
        if assessment.get('success'):
            # Update application with assessment results
            application.risk_score = assessment.get('risk_score', 50)
            application.risk_level = assessment.get('risk_level', 'medium')
            application.risk_factors = assessment.get('risk_factors')
            application.ai_assessment = assessment.get('ai_assessment')
            application.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Risk assessment completed',
                'risk_score': assessment.get('risk_score'),
                'risk_level': assessment.get('risk_level'),
                'risk_factors': json.loads(assessment.get('risk_factors', '[]')),
                'protective_factors': json.loads(assessment.get('protective_factors', '[]')),
                'assessment': assessment.get('ai_assessment'),
                'recommendations': assessment.get('recommendations'),
                'confidence_score': assessment.get('confidence_score')
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': assessment.get('error', 'Assessment failed')
            }), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============= MATCHING ENDPOINTS =============

@app.route('/api/matching/<app_id>', methods=['GET'])
def find_matches(app_id):
    """Find the best matching children for an applicant."""
    try:
        application = Application.query.get(app_id)
        
        if not application:
            return jsonify({'success': False, 'error': 'Application not found'}), 404
        
        # Get all available children
        children = Child.query.all()
        
        if not children:
            return jsonify({
                'success': True,
                'message': 'No children available for matching',
                'matches': []
            }), 200
        
        # Prepare application data
        app_data = {
            'name': application.name,
            'age': calculate_age(application.date_of_birth) if application.date_of_birth else None,
            'occupation': application.occupation,
            'annual_income': application.annual_income,
            'housing_type': application.housing_type,
            'dependents': application.dependents,
            'health_status': application.health_status,
            'experience_with_children': 'Not specified',
        }
        
        # Prepare children data
        children_data = [child.to_dict() for child in children]
        
        # Get AI matching
        matching_result = AIMatching.find_best_matches(app_data, children_data)
        
        if matching_result.get('success'):
            return jsonify({
                'success': True,
                'matches': matching_result.get('matches', []),
                'overall_assessment': matching_result.get('overall_assessment', '')
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': matching_result.get('error', 'Matching failed')
            }), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/matching/<app_id>/<child_id>', methods=['GET'])
def match_child(app_id, child_id):
    """Get detailed match analysis for a specific child-applicant pair."""
    try:
        application = Application.query.get(app_id)
        child = Child.query.get(child_id)
        
        if not application:
            return jsonify({'success': False, 'error': 'Application not found'}), 404
        
        if not child:
            return jsonify({'success': False, 'error': 'Child not found'}), 404
        
        # Prepare application and child data
        app_data = {
            'name': application.name,
            'age': calculate_age(application.date_of_birth) if application.date_of_birth else None,
            'occupation': application.occupation,
            'annual_income': application.annual_income,
            'housing_type': application.housing_type,
            'dependents': application.dependents,
            'health_status': application.health_status,
        }
        
        child_data = child.to_dict()
        
        # Get detailed match analysis
        match_analysis = AIMatching.match_single_child(app_data, child_data)
        
        if match_analysis.get('success'):
            # Save match to database
            existing_match = Match.query.filter_by(
                application_id=app_id,
                child_id=child_id
            ).first()
            
            if existing_match:
                existing_match.compatibility_score = match_analysis.get('compatibility_score')
                existing_match.match_reasoning = match_analysis.get('match_reasoning')
                existing_match.potential_challenges = match_analysis.get('potential_challenges')
                existing_match.recommendations = match_analysis.get('support_recommendations')
                existing_match.updated_at = datetime.utcnow()
            else:
                new_match = Match(
                    application_id=app_id,
                    child_id=child_id,
                    compatibility_score=match_analysis.get('compatibility_score'),
                    match_reasoning=match_analysis.get('match_reasoning'),
                    potential_challenges=match_analysis.get('potential_challenges'),
                    recommendations=match_analysis.get('support_recommendations')
                )
                db.session.add(new_match)
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'compatibility_score': match_analysis.get('compatibility_score'),
                'match_reasoning': match_analysis.get('match_reasoning'),
                'strengths_of_match': json.loads(match_analysis.get('strengths_of_match', '[]')),
                'potential_challenges': json.loads(match_analysis.get('potential_challenges', '[]')),
                'support_recommendations': json.loads(match_analysis.get('support_recommendations', '[]')),
                'overall_recommendation': match_analysis.get('overall_recommendation'),
                'confidence_level': match_analysis.get('confidence_level')
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': match_analysis.get('error', 'Match analysis failed')
            }), 500
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ============= CHILDREN ENDPOINTS =============

@app.route('/api/children', methods=['POST'])
def create_child():
    """Create a new child record in the system."""
    try:
        data = request.get_json()
        
        if not data.get('name') or not data.get('date_of_birth'):
            return jsonify({'success': False, 'error': 'Name and date of birth are required'}), 400
        
        dob = None
        if isinstance(data['date_of_birth'], str):
            dob = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        else:
            dob = data['date_of_birth']
        
        child = Child(
            name=data.get('name'),
            date_of_birth=dob,
            age=calculate_age(dob),
            gender=data.get('gender'),
            health_conditions=data.get('health_conditions'),
            behavioral_traits=data.get('behavioral_traits'),
            interests=data.get('interests'),
            special_needs=data.get('special_needs'),
            requires_experienced_guardian=data.get('requires_experienced_guardian', False),
            requires_multilingual=data.get('requires_multilingual', False),
            requires_physical_accessibility=data.get('requires_physical_accessibility', False),
        )
        
        db.session.add(child)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Child record created successfully',
            'child_id': child.id,
            'data': child.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/children', methods=['GET'])
def list_children():
    """List all children in the system."""
    try:
        children = Child.query.all()
        
        return jsonify({
            'success': True,
            'count': len(children),
            'data': [child.to_dict() for child in children]
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/children/<child_id>', methods=['GET'])
def get_child(child_id):
    """Get a specific child by ID."""
    try:
        child = Child.query.get(child_id)
        
        if not child:
            return jsonify({'success': False, 'error': 'Child not found'}), 404
        
        return jsonify({
            'success': True,
            'data': child.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============= DECISION ENDPOINTS =============

@app.route('/api/applications/<app_id>/decision', methods=['POST'])
def make_decision(app_id):
    """Record a decision on an application."""
    try:
        application = Application.query.get(app_id)
        
        if not application:
            return jsonify({'success': False, 'error': 'Application not found'}), 404
        
        data = request.get_json()
        decision = data.get('decision')  # approved, rejected, info_needed
        reviewed_by = data.get('reviewed_by')
        notes = data.get('notes')
        
        if decision not in ['approved', 'rejected', 'info_needed']:
            return jsonify({'success': False, 'error': 'Invalid decision'}), 400
        
        application.status = decision
        application.reviewed_by = reviewed_by
        application.notes = notes
        application.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Decision recorded: {decision}',
            'data': application.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ============= STATS ENDPOINTS =============

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics."""
    try:
        total_apps = Application.query.count()
        approved = Application.query.filter_by(status='approved').count()
        rejected = Application.query.filter_by(status='rejected').count()
        pending = Application.query.filter_by(status='pending').count()
        info_needed = Application.query.filter_by(status='info_needed').count()
        
        total_children = Child.query.count()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_applications': total_apps,
                'approved': approved,
                'rejected': rejected,
                'pending': pending,
                'info_needed': info_needed,
                'total_children': total_children
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============= HEALTH CHECK =============

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'success': True,
        'status': 'API is running',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


# ============= ERROR HANDLERS =============

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
