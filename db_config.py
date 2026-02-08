"""
Database Configuration for Career Guidance Application
Contains database connection settings and constants
"""

import os

# Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),  # Set your MySQL password
    'database': os.getenv('DB_NAME', 'career_guidance_db'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'charset': 'utf8mb4',
    'use_unicode': True,
    'autocommit': True
}

# Connection pool settings
POOL_CONFIG = {
    'pool_name': 'career_guidance_pool',
    'pool_size': 5,
    'pool_reset_session': True
}

# Security settings
PASSWORD_MIN_LENGTH = 6
ALLOWED_EMAIL_DOMAINS = ["gmail.com", "yahoo.com", "rediffmail.com"]

# Academic level constraints
AGE_CONSTRAINTS = {
    '10th': 15,  # Minimum age for 10th grade
    '12th': 17   # Minimum age for 12th grade
}

ACADEMIC_LEVELS = ['10th', '12th']
