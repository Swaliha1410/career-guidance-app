"""
MySQL-Based Authentication and User Management System
Handles user registration, login, and session management with MySQL database
"""

import json
import bcrypt
from typing import Optional, Dict, Tuple
from database import DatabaseManager
from input_validators import validate_signup, validate_login

from models import User, Student
import logging

logger = logging.getLogger(__name__)


class AuthManager:
    """Manages user authentication and registration with MySQL backend"""
    
    def __init__(self):
        """Initialize the authentication manager"""
        self.db = DatabaseManager
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def _verify_password(password: str, hashed: str) -> bool:
        """Verify password against bcrypt hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def register_student(self, username: str, password: str, email: str,
                        full_name: str, age: int, academic_level: str) -> Tuple[bool, str]:
        """
        Register a new student with full backend validation
        Returns: (success: bool, message: str)
        """
        try:
            # Frontend-level validation using validators module
            is_valid, error_message = validate_signup(full_name, username, email, password, age, academic_level)
            if not is_valid:
                return False, error_message
            
            # Backend business logic: check for existing username
            if self.username_exists(username):
                return False, "Username already exists. Please choose a different username."
            
            # Backend business logic: check for existing email
            if self.email_exists(email):
                return False, "Email already registered. Please use a different email or login."
            
            # Hash password using bcrypt
            password_hash = self._hash_password(password)
            
            # Insert user into database
            query = """
                INSERT INTO users (username, email, password_hash, full_name, age, academic_level, profile_completed)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (username, email, password_hash, full_name, age, academic_level, False)
            
            user_id = self.db.execute_query(query, params)
            
            if user_id:
                logger.info(f"User registered successfully: {username}")
                
                # Log activity
                self._log_activity(user_id, 'REGISTER', f'New user registered: {username}')
                
                return True, "Registration successful! Please log in to your account."
            else:
                return False, "Registration failed. Please try again."
                
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return False, f"Registration failed: {str(e)}"
    
    def login(self, username: str, password: str) -> Tuple[bool, Optional[Student], str]:
        """
        Authenticate user login with backend validation
        Returns: (success: bool, student: Student or None, message: str)
        """
        try:
            # Frontend-level validation using validators module
            is_valid, error_message = validate_login(username, password)
            if not is_valid:
                return False, None, error_message
            
            # Get user from database
            query = """
                SELECT user_id, username, email, password_hash, full_name, age, academic_level, profile_completed
                FROM users
                WHERE username = %s
            """
            user_data = self.db.execute_query(query, (username,), fetch_one=True)
            
            if not user_data:
                return False, None, "Username not found. Please register or check your username."
            
            # Verify password
            if not self._verify_password(password, user_data['password_hash']):
                # Log failed login attempt
                self._log_activity(user_data['user_id'], 'LOGIN_FAILED', f'Failed login attempt for: {username}')
                return False, None, "Incorrect password!"
            
            # Create Student object
            student = Student(
                username=user_data['username'],
                password="temp",  # We don't need actual password after verification
                email=user_data['email'],
                full_name=user_data['full_name'],
                age=user_data['age'],
                academic_level=user_data['academic_level']
            )
            
            # Load assessment results if available
            assessment_data = self._get_assessment_results(user_data['user_id'])
            if assessment_data:
                student.set_assessment_results(assessment_data)
            
            # Load recommendations if available
            recommendations = self._get_recommendations(user_data['user_id'])
            if recommendations:
                student.set_recommendations(recommendations)
            
            # Mark profile as complete if it was completed
            if user_data['profile_completed']:
                student.mark_profile_complete()
            
            # Log successful login
            self._log_activity(user_data['user_id'], 'LOGIN_SUCCESS', f'Successful login: {username}')
            
            logger.info(f"User logged in successfully: {username}")
            return True, student, "Login successful!"
            
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False, None, f"Login failed: {str(e)}"
    
    def update_student_results(self, username: str, assessment_results: Dict, recommendations: list):
        """Update student's assessment results and recommendations"""
        try:
            # Get user ID
            user_data = self._get_user_by_username(username)
            if not user_data:
                logger.error(f"User not found for update: {username}")
                return
            
            user_id = user_data['user_id']
            
            # Update or insert assessment results
            self._save_assessment_results(user_id, assessment_results)
            
            # Update or insert recommendations
            self._save_recommendations(user_id, recommendations)
            
            # Mark profile as completed
            update_query = """
                UPDATE users
                SET profile_completed = TRUE
                WHERE user_id = %s
            """
            self.db.execute_query(update_query, (user_id,))
            
            # Log activity
            self._log_activity(user_id, 'PROFILE_UPDATE', 'Assessment results and recommendations updated')
            
            logger.info(f"Updated results for user: {username}")
            
        except Exception as e:
            logger.error(f"Error updating student results: {e}")
    
    def _save_assessment_results(self, user_id: int, results: Dict):
        """Save or update assessment results"""
        results_json = json.dumps(results)
        
        # Check if results exist
        check_query = "SELECT result_id FROM assessment_results WHERE user_id = %s LIMIT 1"
        existing = self.db.execute_query(check_query, (user_id,), fetch_one=True)
        
        if existing:
            # Update existing results
            query = """
                UPDATE assessment_results
                SET results_json = %s, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = %s
            """
            self.db.execute_query(query, (results_json, user_id))
        else:
            # Insert new results
            query = """
                INSERT INTO assessment_results (user_id, assessment_type, results_json)
                VALUES (%s, %s, %s)
            """
            self.db.execute_query(query, (user_id, 'full_assessment', results_json))
    
    def _save_recommendations(self, user_id: int, recommendations: list):
        """Save or update recommendations"""
        recommendations_json = json.dumps(recommendations)
        
        # Check if recommendations exist
        check_query = "SELECT recommendation_id FROM recommendations WHERE user_id = %s LIMIT 1"
        existing = self.db.execute_query(check_query, (user_id,), fetch_one=True)
        
        if existing:
            # Update existing recommendations
            query = """
                UPDATE recommendations
                SET recommendations_json = %s, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = %s
            """
            self.db.execute_query(query, (recommendations_json, user_id))
        else:
            # Insert new recommendations
            query = """
                INSERT INTO recommendations (user_id, recommendations_json)
                VALUES (%s, %s)
            """
            self.db.execute_query(query, (user_id, recommendations_json))
    
    def _get_assessment_results(self, user_id: int) -> Optional[Dict]:
        """Get assessment results for a user"""
        query = "SELECT results_json FROM assessment_results WHERE user_id = %s LIMIT 1"
        result = self.db.execute_query(query, (user_id,), fetch_one=True)
        
        if result and result['results_json']:
            return json.loads(result['results_json'])
        return None
    
    def _get_recommendations(self, user_id: int) -> Optional[list]:
        """Get recommendations for a user"""
        query = "SELECT recommendations_json FROM recommendations WHERE user_id = %s LIMIT 1"
        result = self.db.execute_query(query, (user_id,), fetch_one=True)
        
        if result and result['recommendations_json']:
            return json.loads(result['recommendations_json'])
        return None
    
    def _get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user data by username"""
        query = """
            SELECT user_id, username, email, full_name, age, academic_level, profile_completed
            FROM users
            WHERE username = %s
        """
        return self.db.execute_query(query, (username,), fetch_one=True)
    
    def get_user_data(self, username: str) -> Optional[Dict]:
        """Get user data by username (public method)"""
        user = self._get_user_by_username(username)
        if user:
            # Add assessment results and recommendations
            user['assessment_results'] = self._get_assessment_results(user['user_id']) or {}
            user['recommendations'] = self._get_recommendations(user['user_id']) or []
        return user
    
    def username_exists(self, username: str) -> bool:
        """Check if username exists"""
        query = "SELECT COUNT(*) as count FROM users WHERE username = %s"
        result = self.db.execute_query(query, (username,), fetch_one=True)
        return result['count'] > 0 if result else False
    
    def email_exists(self, email: str) -> bool:
        """Check if email exists"""
        query = "SELECT COUNT(*) as count FROM users WHERE email = %s"
        result = self.db.execute_query(query, (email,), fetch_one=True)
        return result['count'] > 0 if result else False
    
    def _log_activity(self, user_id: int, activity_type: str, description: str, ip_address: str = None):
        """Log user activity"""
        try:
            query = """
                INSERT INTO user_activity_log (user_id, activity_type, activity_description, ip_address)
                VALUES (%s, %s, %s, %s)
            """
            self.db.execute_query(query, (user_id, activity_type, description, ip_address))
        except Exception as e:
            logger.error(f"Error logging activity: {e}")
