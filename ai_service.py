import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

class AIRiskAssessment:
    """Uses Gemini AI to provide intelligent risk assessment for guardian applications."""
    
    @staticmethod
    def assess_application(application_data):
        """
        Assess risk level of a guardian application using Gemini AI.
        
        Args:
            application_data: Dictionary containing application details
            
        Returns:
            Dictionary with risk_score, risk_level, risk_factors, and ai_assessment
        """
        try:
            model = genai.GenerativeModel('gemini-pro')
            
            # Prepare the prompt with application data
            prompt = f"""You are an expert child welfare and safety analyst. Analyze the following guardian application and provide a comprehensive risk assessment.

APPLICATION DATA:
Name: {application_data.get('name', 'N/A')}
Age: {application_data.get('age', 'N/A')}
Occupation: {application_data.get('occupation', 'N/A')}
Annual Income: ${application_data.get('annual_income', 'N/A')}
Income Stability: {application_data.get('income_stability', 'N/A')}
Housing Type: {application_data.get('housing_type', 'N/A')}
Number of Dependents: {application_data.get('dependents', 0)}
Debt Level: {application_data.get('debt_level', 'N/A')}
Legal Issues: {application_data.get('legal_issues', 'N/A')}
Criminal Record: {application_data.get('criminal_record', 'N/A')}
Welfare History: {application_data.get('welfare_history', 'N/A')}
Health Status: {application_data.get('health_status', 'N/A')}
References Available: {len([r for r in [application_data.get('reference_1_name'), application_data.get('reference_2_name')] if r])} of 2

Please provide a structured risk assessment in JSON format with the following fields:
1. "risk_score": A float between 0-100 (0 = safest, 100 = highest risk)
2. "risk_level": Categories as "low" (0-30), "medium" (31-70), or "high" (71-100)
3. "risk_factors": A list of specific risk factors identified with severity levels
4. "protective_factors": A list of positive factors that mitigate risk
5. "detailed_assessment": A detailed paragraph explaining the assessment
6. "recommendations": Key recommendations for caseworkers
7. "confidence_score": How confident is the AI in this assessment (0-1)

Return ONLY valid JSON, no additional text."""

            response = model.generate_content(prompt)
            
            # Parse the response
            response_text = response.text.strip()
            
            # Try to extract JSON if wrapped in markdown code blocks
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            result = json.loads(response_text)
            
            return {
                'success': True,
                'risk_score': result.get('risk_score', 50),
                'risk_level': result.get('risk_level', 'medium'),
                'risk_factors': json.dumps(result.get('risk_factors', [])),
                'protective_factors': json.dumps(result.get('protective_factors', [])),
                'ai_assessment': result.get('detailed_assessment', ''),
                'recommendations': result.get('recommendations', ''),
                'confidence_score': result.get('confidence_score', 0.5),
                'raw_response': result
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'risk_score': 50,
                'risk_level': 'medium',
                'risk_factors': json.dumps([]),
                'ai_assessment': f'Error in AI assessment: {str(e)}'
            }


class AIMatching:
    """Uses Gemini AI to provide intelligent child-to-guardian matching."""
    
    @staticmethod
    def find_best_matches(application_data, available_children):
        """
        Find the best matching children for a guardian applicant using Gemini AI.
        
        Args:
            application_data: Dictionary containing applicant details
            available_children: List of child dictionaries to match against
            
        Returns:
            Dictionary with matches sorted by compatibility score
        """
        try:
            model = genai.GenerativeModel('gemini-pro')
            
            # Prepare children data for the prompt
            children_info = ""
            for i, child in enumerate(available_children, 1):
                children_info += f"""
Child {i} - ID: {child.get('id', 'N/A')}
Name: {child.get('name', 'N/A')}
Age: {child.get('age', 'N/A')}
Gender: {child.get('gender', 'N/A')}
Health Conditions: {child.get('health_conditions', 'None')}
Behavioral Traits: {child.get('behavioral_traits', 'N/A')}
Interests: {child.get('interests', 'N/A')}
Special Needs: {child.get('special_needs', 'None')}
Requires Experienced Guardian: {child.get('requires_experienced_guardian', False)}
Requires Multilingual Support: {child.get('requires_multilingual', False)}
Requires Physical Accessibility: {child.get('requires_physical_accessibility', False)}
"""
            
            prompt = f"""You are an expert in child welfare and family matching. Analyze the following guardian applicant and the available children, then provide compatibility matches.

GUARDIAN APPLICANT:
Name: {application_data.get('name', 'N/A')}
Age: {application_data.get('age', 'N/A')}
Occupation: {application_data.get('occupation', 'N/A')}
Annual Income: ${application_data.get('annual_income', 'N/A')}
Housing Type: {application_data.get('housing_type', 'N/A')}
Number of Dependents: {application_data.get('dependents', 0)}
Health Status: {application_data.get('health_status', 'Good')}
Experience with Children: {application_data.get('experience_with_children', 'Not specified')}

AVAILABLE CHILDREN:
{children_info}

Please analyze compatibility and provide matches in the following JSON format:
{{
    "matches": [
        {{
            "child_id": "CH-XXXXX",
            "compatibility_score": 85.5,
            "match_reasoning": "Explanation of why this is a good match",
            "potential_challenges": "Any challenges or concerns",
            "recommendations": "Specific recommendations for this match"
        }}
    ],
    "overall_assessment": "Overall assessment of the applicant's readiness to take children"
}}

Include all children in the array, sorted by compatibility score (highest first). Scores should be between 0-100.
Consider: age compatibility, lifestyle match, financial stability, special needs matching, shared interests.
Return ONLY valid JSON, no additional text."""

            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Try to extract JSON if wrapped in markdown code blocks
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            result = json.loads(response_text)
            
            return {
                'success': True,
                'matches': result.get('matches', []),
                'overall_assessment': result.get('overall_assessment', ''),
                'raw_response': result
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'matches': [],
                'overall_assessment': f'Error in matching algorithm: {str(e)}'
            }
    
    @staticmethod
    def match_single_child(application_data, child_data):
        """
        Provide detailed compatibility analysis for a specific child-applicant pair.
        
        Args:
            application_data: Dictionary containing applicant details
            child_data: Dictionary containing child details
            
        Returns:
            Dictionary with detailed match analysis
        """
        try:
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""You are an expert child welfare specialist. Provide a detailed compatibility analysis for the following child-applicant pairing.

GUARDIAN APPLICANT:
Name: {application_data.get('name', 'N/A')}
Age: {application_data.get('age', 'N/A')}
Occupation: {application_data.get('occupation', 'N/A')}
Annual Income: ${application_data.get('annual_income', 'N/A')}
Housing Type: {application_data.get('housing_type', 'N/A')}
Number of Current Dependents: {application_data.get('dependents', 0)}
Health Status: {application_data.get('health_status', 'Good')}

CHILD:
Name: {child_data.get('name', 'N/A')}
Age: {child_data.get('age', 'N/A')}
Gender: {child_data.get('gender', 'N/A')}
Health Conditions: {child_data.get('health_conditions', 'None')}
Behavioral Traits: {child_data.get('behavioral_traits', 'N/A')}
Interests: {child_data.get('interests', 'N/A')}
Special Needs: {child_data.get('special_needs', 'None')}

Provide a detailed match analysis in JSON format:
{{
    "compatibility_score": 0-100,
    "match_reasoning": "Detailed explanation of compatibility",
    "strengths_of_match": ["List of positive factors"],
    "potential_challenges": ["List of challenges or concerns"],
    "support_recommendations": ["Recommendations for support services"],
    "overall_recommendation": "Strong recommendation / Good match / Consider carefully / Not recommended",
    "confidence_level": 0-1
}}

Return ONLY valid JSON, no additional text."""

            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Try to extract JSON if wrapped in markdown code blocks
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            result = json.loads(response_text)
            
            return {
                'success': True,
                'compatibility_score': result.get('compatibility_score', 50),
                'match_reasoning': result.get('match_reasoning', ''),
                'strengths_of_match': json.dumps(result.get('strengths_of_match', [])),
                'potential_challenges': json.dumps(result.get('potential_challenges', [])),
                'support_recommendations': json.dumps(result.get('support_recommendations', [])),
                'overall_recommendation': result.get('overall_recommendation', 'Consider carefully'),
                'confidence_level': result.get('confidence_level', 0.5),
                'raw_response': result
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'compatibility_score': 50,
                'match_reasoning': f'Error in matching: {str(e)}'
            }
