from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.String(50), primary_key=True, default=lambda: 'GS-' + str(uuid.uuid4())[:8].upper())
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    occupation = db.Column(db.String(100))
    address = db.Column(db.Text)
    
    # Financial Info
    annual_income = db.Column(db.Integer)
    income_stability = db.Column(db.String(50))  # stable, unstable, variable
    debt_level = db.Column(db.String(50))  # none, minor, significant, severe
    housing_type = db.Column(db.String(50))  # owned, rented, other
    
    # Background
    dependents = db.Column(db.Integer, default=0)
    legal_issues = db.Column(db.String(50))  # none, minor, serious, felony
    welfare_history = db.Column(db.String(50))  # no, yes
    criminal_record = db.Column(db.String(50))  # no, minor, serious, felony
    health_status = db.Column(db.Text)
    
    # References
    reference_1_name = db.Column(db.String(150))
    reference_1_contact = db.Column(db.String(120))
    reference_2_name = db.Column(db.String(150))
    reference_2_contact = db.Column(db.String(120))
    
    # Risk Assessment (AI Generated)
    risk_score = db.Column(db.Float, default=0)
    risk_level = db.Column(db.String(20))  # low, medium, high
    risk_factors = db.Column(db.Text)  # JSON string of factors
    ai_assessment = db.Column(db.Text)  # Detailed AI assessment
    
    # Matching & Status
    status = db.Column(db.String(50), default='pending')  # pending, approved, rejected, info_needed
    match_score = db.Column(db.Float, default=0)
    match_recommendations = db.Column(db.Text)  # JSON string
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    reviewed_by = db.Column(db.String(100))
    notes = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'occupation': self.occupation,
            'address': self.address,
            'annual_income': self.annual_income,
            'income_stability': self.income_stability,
            'debt_level': self.debt_level,
            'housing_type': self.housing_type,
            'dependents': self.dependents,
            'legal_issues': self.legal_issues,
            'welfare_history': self.welfare_history,
            'criminal_record': self.criminal_record,
            'health_status': self.health_status,
            'reference_1_name': self.reference_1_name,
            'reference_1_contact': self.reference_1_contact,
            'reference_2_name': self.reference_2_name,
            'reference_2_contact': self.reference_2_contact,
            'risk_score': self.risk_score,
            'risk_level': self.risk_level,
            'risk_factors': self.risk_factors,
            'ai_assessment': self.ai_assessment,
            'status': self.status,
            'match_score': self.match_score,
            'match_recommendations': self.match_recommendations,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'reviewed_by': self.reviewed_by,
            'notes': self.notes
        }


class Child(db.Model):
    __tablename__ = 'children'
    
    id = db.Column(db.String(50), primary_key=True, default=lambda: 'CH-' + str(uuid.uuid4())[:8].upper())
    name = db.Column(db.String(150), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    health_conditions = db.Column(db.Text)
    behavioral_traits = db.Column(db.Text)
    interests = db.Column(db.Text)
    special_needs = db.Column(db.Text)
    
    # Matching attributes
    requires_experienced_guardian = db.Column(db.Boolean, default=False)
    requires_multilingual = db.Column(db.Boolean, default=False)
    requires_physical_accessibility = db.Column(db.Boolean, default=False)
    compatibility_profile = db.Column(db.Text)  # JSON string
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date_of_birth': self.date_of_birth.isoformat(),
            'age': self.age,
            'gender': self.gender,
            'health_conditions': self.health_conditions,
            'behavioral_traits': self.behavioral_traits,
            'interests': self.interests,
            'special_needs': self.special_needs,
            'requires_experienced_guardian': self.requires_experienced_guardian,
            'requires_multilingual': self.requires_multilingual,
            'requires_physical_accessibility': self.requires_physical_accessibility,
            'compatibility_profile': self.compatibility_profile,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Match(db.Model):
    __tablename__ = 'matches'
    
    id = db.Column(db.String(50), primary_key=True, default=lambda: 'M-' + str(uuid.uuid4())[:8].upper())
    application_id = db.Column(db.String(50), db.ForeignKey('applications.id'), nullable=False)
    child_id = db.Column(db.String(50), db.ForeignKey('children.id'), nullable=False)
    compatibility_score = db.Column(db.Float, default=0)
    match_reasoning = db.Column(db.Text)
    potential_challenges = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    status = db.Column(db.String(50), default='pending')  # pending, accepted, rejected
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'application_id': self.application_id,
            'child_id': self.child_id,
            'compatibility_score': self.compatibility_score,
            'match_reasoning': self.match_reasoning,
            'potential_challenges': self.potential_challenges,
            'recommendations': self.recommendations,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class PsychologicalAssessment(db.Model):
    __tablename__ = 'psychological_assessments'
    
    id = db.Column(db.String(50), primary_key=True, default=lambda: 'PA-' + str(uuid.uuid4())[:8].upper())
    application_id = db.Column(db.String(50), db.ForeignKey('applications.id'), nullable=False, unique=True)
    
    # Assessment Responses (15 questions max)
    q1_emotional_control = db.Column(db.String(10))  # 1-5 scale
    q2_stress_management = db.Column(db.String(10))
    q3_anger_issues = db.Column(db.String(10))
    q4_substance_use = db.Column(db.String(10))
    q5_alcohol_dependency = db.Column(db.String(10))
    q6_prescription_misuse = db.Column(db.String(10))
    q7_violence_tendency = db.Column(db.String(10))
    q8_physical_abuse = db.Column(db.String(10))
    q9_emotional_abuse = db.Column(db.String(10))
    q10_verbal_abuse = db.Column(db.String(10))
    q11_psychological_history = db.Column(db.String(10))
    q12_mental_health_treatment = db.Column(db.String(10))
    q13_emotional_stability = db.Column(db.String(10))
    q14_impulse_control = db.Column(db.String(10))
    q15_patience_with_children = db.Column(db.String(10))
    
    # Overall Assessment Results
    total_score = db.Column(db.Float, default=0)
    risk_level = db.Column(db.String(20))  # low, medium, high (based on scores)
    toxicity_score = db.Column(db.Float, default=0)
    substance_abuse_score = db.Column(db.Float, default=0)
    violence_score = db.Column(db.Float, default=0)
    mental_health_score = db.Column(db.Float, default=0)
    
    # Detailed Analysis Report
    analysis_report = db.Column(db.Text)  # JSON or formatted text
    recommendations = db.Column(db.Text)
    red_flags = db.Column(db.Text)  # JSON array
    protective_factors = db.Column(db.Text)  # JSON array
    
    # Meta
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'application_id': self.application_id,
            'q1_emotional_control': self.q1_emotional_control,
            'q2_stress_management': self.q2_stress_management,
            'q3_anger_issues': self.q3_anger_issues,
            'q4_substance_use': self.q4_substance_use,
            'q5_alcohol_dependency': self.q5_alcohol_dependency,
            'q6_prescription_misuse': self.q6_prescription_misuse,
            'q7_violence_tendency': self.q7_violence_tendency,
            'q8_physical_abuse': self.q8_physical_abuse,
            'q9_emotional_abuse': self.q9_emotional_abuse,
            'q10_verbal_abuse': self.q10_verbal_abuse,
            'q11_psychological_history': self.q11_psychological_history,
            'q12_mental_health_treatment': self.q12_mental_health_treatment,
            'q13_emotional_stability': self.q13_emotional_stability,
            'q14_impulse_control': self.q14_impulse_control,
            'q15_patience_with_children': self.q15_patience_with_children,
            'total_score': self.total_score,
            'risk_level': self.risk_level,
            'toxicity_score': self.toxicity_score,
            'substance_abuse_score': self.substance_abuse_score,
            'violence_score': self.violence_score,
            'mental_health_score': self.mental_health_score,
            'analysis_report': self.analysis_report,
            'recommendations': self.recommendations,
            'red_flags': self.red_flags,
            'protective_factors': self.protective_factors,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
