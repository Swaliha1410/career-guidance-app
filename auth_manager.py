"""
Authentication and User Management System
Handles user registration, login, and session management
"""

import json
import os
from typing import Optional, Dict
from models import User, Student
from validators import validate_signup, validate_login


class AuthManager:
    """Manages user authentication and registration"""
    
    def __init__(self, data_file: str = "users.json"):
        self.data_file = data_file
        self.users = self._load_users()
    
    def _load_users(self) -> Dict:
        """Load users from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def _save_users(self):
        """Save users to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.users, f, indent=4)
    
    def register_student(self, username: str, password: str, email: str,
                        full_name: str, age: int, academic_level: str) -> tuple[bool, str]:
        """
        Register a new student with full backend validation
        Returns: (success: bool, message: str)
        """
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
        
        # Create student object
        student = Student(username, password, email, full_name, age, academic_level)
        
        # Store user data
        self.users[username] = {
            'email': email,
            'full_name': full_name,
            'age': age,
            'academic_level': academic_level,
            'password_hash': student._User__password,  # Access private attribute for storage
            'profile_completed': False,
            'assessment_results': {},
            'recommendations': []
        }
        
        self._save_users()
        return True, "Registration successful! Please log in to your account."
    
    def login(self, username: str, password: str) -> tuple[bool, Optional[Student], str]:
        """
        Authenticate user login with backend validation
        Returns: (success: bool, student: Student or None, message: str)
        """
        # Frontend-level validation using validators module
        is_valid, error_message = validate_login(username, password)
        if not is_valid:
            return False, None, error_message
        
        # Backend business logic: check if user exists
        if username not in self.users:
            return False, None, "Username not found. Please register or check your username."
        
        user_data = self.users[username]
        
        # Create student object to verify password
        temp_student = Student(
            username=username,
            password="temp",  # Temporary password
            email=user_data['email'],
            full_name=user_data['full_name'],
            age=user_data['age'],
            academic_level=user_data['academic_level']
        )
        
        # Replace with actual password hash
        temp_student._User__password = user_data['password_hash']
        
        # Verify password
        if not temp_student.verify_password(password):
            return False, None, "Incorrect password!"
        
        # Restore student's assessment data
        if user_data['assessment_results']:
            temp_student.set_assessment_results(user_data['assessment_results'])
        
        if user_data['recommendations']:
            temp_student.set_recommendations(user_data['recommendations'])
        
        return True, temp_student, "Login successful!"
    
    def update_student_results(self, username: str, assessment_results: Dict, recommendations: list):
        """Update student's assessment results and recommendations"""
        if username in self.users:
            self.users[username]['assessment_results'] = assessment_results
            self.users[username]['recommendations'] = recommendations
            self.users[username]['profile_completed'] = True
            self._save_users()
    
    def get_user_data(self, username: str) -> Optional[Dict]:
        """Get user data by username"""
        return self.users.get(username)
    
    def username_exists(self, username: str) -> bool:
        """Check if username exists"""
        return username in self.users
    
    def email_exists(self, email: str) -> bool:
        """Check if email exists"""
        return any(user['email'] == email for user in self.users.values())
