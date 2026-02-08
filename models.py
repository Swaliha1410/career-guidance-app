"""
Data Models for Career Guidance Application
Demonstrates OOP principles: Encapsulation, Inheritance, Polymorphism
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional
import json
import hashlib
from college_data_manager import CollegeDataManager


class User:
    """Base User class demonstrating Encapsulation"""
    
    def __init__(self, username: str, password: str, email: str):
        self.__username = username  # Private attribute
        self.__password = self.__hash_password(password)  # Private attribute
        self.__email = email
        self.__created_at = datetime.now()
        self.__profile_completed = False
    
    def __hash_password(self, password: str) -> str:
        """Private method for password hashing"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str) -> bool:
        """Public method to verify password"""
        return self.__hash_password(password) == self.__password
    
    # Getters (Encapsulation)
    def get_username(self) -> str:
        return self.__username
    
    def get_email(self) -> str:
        return self.__email
    
    def is_profile_completed(self) -> bool:
        return self.__profile_completed
    
    def mark_profile_complete(self):
        self.__profile_completed = True


class Student(User):
    """Student class demonstrating Inheritance from User"""
    
    def __init__(self, username: str, password: str, email: str, 
                 full_name: str, age: int, academic_level: str):
        super().__init__(username, password, email)
        self.__full_name = full_name
        self.__age = age
        self.__academic_level = academic_level  # "10th" or "12th"
        self.__assessment_results = {}
        self.__recommendations = []
    
    # Getters
    def get_full_name(self) -> str:
        return self.__full_name
    
    def get_age(self) -> int:
        return self.__age
    
    def get_academic_level(self) -> str:
        return self.__academic_level
    
    def get_assessment_results(self) -> Dict:
        return self.__assessment_results.copy()
    
    def get_recommendations(self) -> List:
        return self.__recommendations.copy()
    
    # Setters
    def set_assessment_results(self, results: Dict):
        self.__assessment_results = results
        self.mark_profile_complete()
    
    def set_recommendations(self, recommendations: List):
        self.__recommendations = recommendations


class Assessment(ABC):
    """Abstract base class demonstrating Polymorphism"""
    
    def __init__(self, student: Student):
        self.student = student
        self.questions = []
        self.scores = {}
    
    @abstractmethod
    def generate_questions(self) -> List[Dict]:
        """Abstract method to be implemented by subclasses"""
        pass
    
    @abstractmethod
    def calculate_scores(self, answers: Dict) -> Dict:
        """Abstract method to calculate assessment scores"""
        pass
    
    @abstractmethod
    def generate_recommendations(self, scores: Dict) -> List[Dict]:
        """Abstract method to generate recommendations"""
        pass


class TenthGradeAssessment(Assessment):
    """10th Grade Assessment - Polymorphic implementation"""
    
    def __init__(self, student: Student):
        super().__init__(student)
        self.stream_categories = {
            'science': 0,
            'commerce': 0,
            'arts': 0
        }
        # Initialize college data manager
        self.college_manager = CollegeDataManager()
    
    def generate_questions(self) -> List[Dict]:
        """Generate interest-based questions for 10th graders"""
        self.questions = [
            {
                'id': 1,
                'question': 'Which subjects do you enjoy the most?',
                'options': {
                    'Mathematics and Physics': {'science': 3, 'commerce': 1},
                    'Economics and Business Studies': {'commerce': 3, 'arts': 1},
                    'History and Literature': {'arts': 3, 'science': 0},
                    'Biology and Chemistry': {'science': 3, 'commerce': 0}
                }
            },
            {
                'id': 2,
                'question': 'What type of career interests you?',
                'options': {
                    'Engineering or Medicine': {'science': 3},
                    'Business or Finance': {'commerce': 3},
                    'Creative Arts or Social Work': {'arts': 3},
                    'Law or Civil Services': {'arts': 2, 'commerce': 1}
                }
            },
            {
                'id': 3,
                'question': 'How do you prefer to solve problems?',
                'options': {
                    'Using logical and analytical thinking': {'science': 2, 'commerce': 2},
                    'Through creative and innovative approaches': {'arts': 3},
                    'By analyzing data and numbers': {'commerce': 2, 'science': 1},
                    'By understanding people and situations': {'arts': 2}
                }
            },
            {
                'id': 4,
                'question': 'Which activity would you enjoy most?',
                'options': {
                    'Conducting science experiments': {'science': 3},
                    'Managing a small business project': {'commerce': 3},
                    'Writing stories or creating art': {'arts': 3},
                    'Debating on current affairs': {'arts': 2, 'commerce': 1}
                }
            },
            {
                'id': 5,
                'question': 'What are your strengths?',
                'options': {
                    'Problem-solving and critical thinking': {'science': 2, 'commerce': 1},
                    'Communication and presentation': {'arts': 2, 'commerce': 2},
                    'Creativity and imagination': {'arts': 3},
                    'Numerical ability and calculations': {'science': 2, 'commerce': 3}
                }
            },
            {
                'id': 6,
                'question': 'Which field excites you for future study?',
                'options': {
                    'Technology and Innovation': {'science': 3},
                    'Economics and Markets': {'commerce': 3},
                    'Psychology and Sociology': {'arts': 3},
                    'Environmental Science': {'science': 2, 'arts': 1}
                }
            },
            {
                'id': 7,
                'question': 'How do you spend your free time?',
                'options': {
                    'Reading tech blogs or science articles': {'science': 2},
                    'Following business news or stock market': {'commerce': 2},
                    'Reading novels or watching movies': {'arts': 2},
                    'Playing sports or games': {'science': 1, 'arts': 1}
                }
            },
            {
                'id': 8,
                'question': 'What motivates you the most?',
                'options': {
                    'Discovering how things work': {'science': 3},
                    'Building wealth and success': {'commerce': 3},
                    'Making a difference in society': {'arts': 3},
                    'Innovation and invention': {'science': 2, 'arts': 1}
                }
            }
        ]
        return self.questions
    
    def calculate_scores(self, answers: Dict) -> Dict:
        """Calculate stream preference scores"""
        scores = {'science': 0, 'commerce': 0, 'arts': 0}
        
        for question_id, answer in answers.items():
            question = next((q for q in self.questions if q['id'] == question_id), None)
            if question and answer in question['options']:
                option_scores = question['options'][answer]
                for stream, points in option_scores.items():
                    scores[stream] += points
        
        return scores
    
    def generate_recommendations(self, scores: Dict) -> List[Dict]:
        """Generate stream and college recommendations"""
        # Determine top streams
        sorted_streams = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        primary_stream = sorted_streams[0][0]
        
        recommendations = []
        
        # Science Stream Recommendations
        if primary_stream == 'science':
            # Get real colleges from dataset
            science_colleges = self.college_manager.get_colleges_by_stream('Science', max_results=8)
            
            recommendations.append({
                'stream': 'Science',
                'confidence': self._calculate_confidence(scores['science'], scores),
                'subjects': ['Physics', 'Chemistry', 'Mathematics', 'Biology (optional)', 'English'],
                'career_paths': [
                    'Engineering (Computer Science, Mechanical, Electrical, Civil)',
                    'Medical (MBBS, BDS, Nursing, Pharmacy)',
                    'Research & Development',
                    'Architecture',
                    'Aviation'
                ],
                'colleges': science_colleges if science_colleges else [
                    {'name': 'Delhi Public School', 'location': 'Multiple Cities', 'type': 'CBSE'}
                ],
                'entrance_exams': ['JEE Main', 'JEE Advanced', 'NEET', 'BITSAT', 'State Engineering Exams'],
                'skills_needed': ['Analytical thinking', 'Problem-solving', 'Mathematical aptitude', 'Scientific curiosity']
            })
        
        # Commerce Stream Recommendations
        elif primary_stream == 'commerce':
            # Get real colleges from dataset
            commerce_colleges = self.college_manager.get_colleges_by_stream('Commerce', max_results=8)
            
            recommendations.append({
                'stream': 'Commerce',
                'confidence': self._calculate_confidence(scores['commerce'], scores),
                'subjects': ['Accountancy', 'Business Studies', 'Economics', 'Mathematics/IP', 'English'],
                'career_paths': [
                    'Chartered Accountancy (CA)',
                    'Company Secretary (CS)',
                    'Business Management (BBA, MBA)',
                    'Banking and Finance',
                    'Digital Marketing',
                    'Entrepreneurship'
                ],
                'colleges': commerce_colleges if commerce_colleges else [
                    {'name': 'Sri Ram College of Commerce', 'location': 'Delhi', 'type': 'CBSE'}
                ],
                'entrance_exams': ['CA Foundation', 'CS Foundation', 'BBA Entrance Tests', 'CUET'],
                'skills_needed': ['Numerical ability', 'Business acumen', 'Communication', 'Financial literacy']
            })
        
        # Arts/Humanities Stream Recommendations
        else:
            # Get real colleges from dataset
            arts_colleges = self.college_manager.get_colleges_by_stream('Arts', max_results=8)
            
            recommendations.append({
                'stream': 'Arts/Humanities',
                'confidence': self._calculate_confidence(scores['arts'], scores),
                'subjects': ['History', 'Political Science', 'Psychology', 'Sociology', 'English'],
                'career_paths': [
                    'Civil Services (IAS, IPS, IFS)',
                    'Law (LLB, Corporate Law)',
                    'Journalism and Mass Communication',
                    'Psychology and Counseling',
                    'Social Work',
                    'Design and Creative Arts',
                    'Teaching and Education'
                ],
                'colleges': arts_colleges if arts_colleges else [
                    {'name': 'The Shri Ram School', 'location': 'Delhi', 'type': 'CBSE'}
                ],
                'entrance_exams': ['CLAT (Law)', 'UPSC (Civil Services)', 'NIFT/NID (Design)', 'CUET'],
                'skills_needed': ['Critical thinking', 'Communication', 'Creativity', 'Empathy']
            })
        
        # Add alternative stream if score is close
        if sorted_streams[1][1] >= sorted_streams[0][1] * 0.7:
            alternative_stream = sorted_streams[1][0]
            if alternative_stream == 'science':
                recommendations.append(self._get_science_alternative())
            elif alternative_stream == 'commerce':
                recommendations.append(self._get_commerce_alternative())
            else:
                recommendations.append(self._get_arts_alternative())
        
        return recommendations
    
    def _calculate_confidence(self, stream_score: int, all_scores: Dict) -> str:
        """Calculate confidence level for recommendation"""
        total_score = sum(all_scores.values())
        if total_score == 0:
            return "Low"
        
        percentage = (stream_score / total_score) * 100
        
        if percentage >= 60:
            return "High"
        elif percentage >= 40:
            return "Moderate"
        else:
            return "Low"
    
    def _get_science_alternative(self) -> Dict:
        return {
            'stream': 'Science (Alternative)',
            'confidence': 'Moderate',
            'subjects': ['Physics', 'Chemistry', 'Mathematics', 'Biology (optional)', 'English'],
            'career_paths': ['Engineering', 'Medical', 'Research'],
            'colleges': [{'name': 'Various CBSE Schools', 'location': 'Pan India', 'type': 'CBSE'}],
            'entrance_exams': ['JEE', 'NEET'],
            'skills_needed': ['Analytical thinking', 'Problem-solving']
        }
    
    def _get_commerce_alternative(self) -> Dict:
        return {
            'stream': 'Commerce (Alternative)',
            'confidence': 'Moderate',
            'subjects': ['Accountancy', 'Business Studies', 'Economics', 'English'],
            'career_paths': ['CA', 'CS', 'Business Management'],
            'colleges': [{'name': 'Various CBSE Schools', 'location': 'Pan India', 'type': 'CBSE'}],
            'entrance_exams': ['CA Foundation', 'BBA Entrance'],
            'skills_needed': ['Numerical ability', 'Business acumen']
        }
    
    def _get_arts_alternative(self) -> Dict:
        return {
            'stream': 'Arts/Humanities (Alternative)',
            'confidence': 'Moderate',
            'subjects': ['History', 'Political Science', 'Psychology', 'English'],
            'career_paths': ['Civil Services', 'Law', 'Journalism'],
            'colleges': [{'name': 'Various CBSE Schools', 'location': 'Pan India', 'type': 'CBSE'}],
            'entrance_exams': ['CLAT', 'UPSC'],
            'skills_needed': ['Critical thinking', 'Communication']
        }


class TwelfthGradeAssessment(Assessment):
    """12th Grade Assessment - Polymorphic implementation"""
    
    def __init__(self, student: Student):
        super().__init__(student)
        self.field_categories = {
            'engineering': 0,
            'medical': 0,
            'business': 0,
            'law': 0,
            'design': 0,
            'social_sciences': 0
        }
        # Initialize college data manager
        self.college_manager = CollegeDataManager()
    
    def generate_questions(self) -> List[Dict]:
        """Generate career-focused questions for 12th graders"""
        self.questions = [
            {
                'id': 1,
                'question': 'Which field aligns with your interests?',
                'options': {
                    'Technology and Innovation': {'engineering': 3},
                    'Healthcare and Medicine': {'medical': 3},
                    'Business and Entrepreneurship': {'business': 3},
                    'Legal and Judicial System': {'law': 3},
                    'Creative Design and Arts': {'design': 3},
                    'Social Work and Research': {'social_sciences': 3}
                }
            },
            {
                'id': 2,
                'question': 'What is your preferred work environment?',
                'options': {
                    'Tech companies and startups': {'engineering': 2, 'business': 1},
                    'Hospitals and clinics': {'medical': 3},
                    'Corporate offices': {'business': 2, 'law': 1},
                    'Studios and creative spaces': {'design': 3},
                    'Research institutions': {'engineering': 1, 'social_sciences': 2}
                }
            },
            {
                'id': 3,
                'question': 'Which skill set describes you best?',
                'options': {
                    'Coding and technical problem-solving': {'engineering': 3},
                    'Empathy and patient care': {'medical': 3},
                    'Leadership and management': {'business': 3},
                    'Analytical and argumentative': {'law': 3},
                    'Creative and artistic': {'design': 3},
                    'Research and analysis': {'social_sciences': 3}
                }
            },
            {
                'id': 4,
                'question': 'What subjects did you excel in?',
                'options': {
                    'Mathematics and Computer Science': {'engineering': 3},
                    'Biology and Chemistry': {'medical': 3},
                    'Economics and Accountancy': {'business': 3},
                    'Political Science and History': {'law': 2, 'social_sciences': 2},
                    'Fine Arts and Design': {'design': 3}
                }
            },
            {
                'id': 5,
                'question': 'What are your career priorities?',
                'options': {
                    'High salary and job security': {'engineering': 2, 'business': 2},
                    'Helping people and making impact': {'medical': 2, 'social_sciences': 2},
                    'Creativity and self-expression': {'design': 3},
                    'Power and influence': {'law': 2, 'business': 1},
                    'Innovation and research': {'engineering': 2, 'medical': 1}
                }
            },
            {
                'id': 6,
                'question': 'How long are you willing to study?',
                'options': {
                    '3-4 years (Bachelor\'s degree)': {'engineering': 1, 'business': 2, 'design': 2},
                    '5-6 years (Professional course)': {'medical': 2, 'law': 2},
                    'Flexible, depends on the field': {'engineering': 1, 'business': 1, 'social_sciences': 1}
                }
            },
            {
                'id': 7,
                'question': 'What type of challenges excite you?',
                'options': {
                    'Building and creating new things': {'engineering': 3, 'design': 2},
                    'Solving medical mysteries': {'medical': 3},
                    'Market strategies and growth': {'business': 3},
                    'Fighting for justice': {'law': 3},
                    'Understanding human behavior': {'social_sciences': 3}
                }
            },
            {
                'id': 8,
                'question': 'Which industry trends interest you?',
                'options': {
                    'AI and Machine Learning': {'engineering': 3},
                    'Biotechnology and Genomics': {'medical': 3},
                    'Fintech and Startups': {'business': 3},
                    'Digital Media and UX Design': {'design': 3},
                    'Public Policy and Sustainability': {'social_sciences': 3}
                }
            }
        ]
        return self.questions
    
    def calculate_scores(self, answers: Dict) -> Dict:
        """Calculate career field preference scores"""
        scores = {
            'engineering': 0,
            'medical': 0,
            'business': 0,
            'law': 0,
            'design': 0,
            'social_sciences': 0
        }
        
        for question_id, answer in answers.items():
            question = next((q for q in self.questions if q['id'] == question_id), None)
            if question and answer in question['options']:
                option_scores = question['options'][answer]
                for field, points in option_scores.items():
                    scores[field] += points
        
        return scores
    
    def generate_recommendations(self, scores: Dict) -> List[Dict]:
        """Generate graduation course and college recommendations"""
        sorted_fields = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        primary_field = sorted_fields[0][0]
        
        recommendations = []
        
        # Engineering Recommendations
        if primary_field == 'engineering':
            # Get real colleges from dataset
            engineering_colleges = self.college_manager.get_colleges_by_field('Computer Science', 'B.Tech', max_results=10)
            
            # Format colleges for display
            formatted_colleges = []
            for college in engineering_colleges:
                formatted_colleges.append({
                    'name': college['name'],
                    'location': college['location'],
                    'ranking': college['ranking'],
                    'cutoff': f"{college['cutoff']} | {college['entrance_exam']}",
                    'fees': college['fees'],
                    'placement': college['placement'],
                    'tier': college['tier'],
                    'naac_grade': college['naac_grade'],
                    'rating': college['rating']
                })
            
            recommendations.append({
                'field': 'Engineering & Technology',
                'confidence': self._calculate_confidence(scores['engineering'], scores),
                'courses': [
                    {
                        'name': 'B.Tech Computer Science & Engineering',
                        'duration': '4 years',
                        'trending_specializations': ['AI/ML', 'Data Science', 'Cyber Security', 'Cloud Computing'],
                        'average_salary': '₹6-15 LPA (Fresher)',
                        'top_salary': '₹40+ LPA (Top Companies)'
                    },
                    {
                        'name': 'B.Tech Electronics & Communication',
                        'duration': '4 years',
                        'trending_specializations': ['IoT', 'VLSI Design', '5G Technology'],
                        'average_salary': '₹5-10 LPA',
                        'top_salary': '₹25+ LPA'
                    },
                    {
                        'name': 'B.Tech Mechanical Engineering',
                        'duration': '4 years',
                        'trending_specializations': ['Robotics', 'Automotive', 'Renewable Energy'],
                        'average_salary': '₹4-8 LPA',
                        'top_salary': '₹20+ LPA'
                    }
                ],
                'top_colleges': formatted_colleges if formatted_colleges else [
                    {'name': 'IIT Bombay', 'location': 'Mumbai', 'ranking': 1, 'cutoff': 'JEE Advanced Rank < 500'}
                ],
                'entrance_exams': ['JEE Main', 'JEE Advanced', 'BITSAT', 'VITEEE', 'State Engineering Exams'],
                'career_opportunities': [
                    'Software Engineer at Google, Microsoft, Amazon',
                    'Data Scientist/ML Engineer',
                    'Product Manager',
                    'Startup Founder',
                    'Research & Development'
                ],
                'growth_prospects': 'Excellent - Tech industry growing at 15% annually'
            })
        
        # Medical Recommendations
        elif primary_field == 'medical':
            # Get real colleges from dataset
            medical_colleges = self.college_manager.get_colleges_by_field('Medicine', 'MBBS', max_results=10)
            
            # Format colleges for display
            formatted_colleges = []
            for college in medical_colleges:
                formatted_colleges.append({
                    'name': college['name'],
                    'location': college['location'],
                    'ranking': college['ranking'],
                    'cutoff': f"{college['cutoff']} | {college['entrance_exam']}",
                    'fees': college['fees'],
                    'placement': college['placement'],
                    'tier': college['tier'],
                    'naac_grade': college['naac_grade'],
                    'rating': college['rating']
                })
            
            recommendations.append({
                'field': 'Medical & Healthcare',
                'confidence': self._calculate_confidence(scores['medical'], scores),
                'courses': [
                    {
                        'name': 'MBBS',
                        'duration': '5.5 years (including internship)',
                        'trending_specializations': ['Cardiology', 'Neurology', 'Oncology', 'Pediatrics'],
                        'average_salary': '₹6-12 LPA (Starting)',
                        'top_salary': '₹50+ LPA (Senior Specialists)'
                    },
                    {
                        'name': 'BDS (Dental Surgery)',
                        'duration': '5 years',
                        'trending_specializations': ['Orthodontics', 'Oral Surgery'],
                        'average_salary': '₹4-8 LPA',
                        'top_salary': '₹20+ LPA'
                    },
                    {
                        'name': 'B.Pharm (Pharmacy)',
                        'duration': '4 years',
                        'trending_specializations': ['Clinical Pharmacy', 'Pharmaceutical Research'],
                        'average_salary': '₹3-6 LPA',
                        'top_salary': '₹15+ LPA'
                    }
                ],
                'top_colleges': formatted_colleges if formatted_colleges else [
                    {'name': 'AIIMS Delhi', 'location': 'Delhi', 'ranking': 1, 'cutoff': 'NEET Rank < 100'}
                ],
                'entrance_exams': ['NEET UG', 'AIIMS MBBS (merged with NEET)', 'State Medical Exams'],
                'career_opportunities': [
                    'Medical Practitioner',
                    'Hospital Administrator',
                    'Medical Researcher',
                    'Public Health Officer',
                    'Medical Consultant'
                ],
                'growth_prospects': 'Very Good - Healthcare sector growing rapidly'
            })
        
        # Business Recommendations
        elif primary_field == 'business':
            # Get real colleges from dataset
            business_colleges = self.college_manager.get_colleges_by_field('Business Administration', 'MBA', max_results=10)
            
            # Format colleges for display
            formatted_colleges = []
            for college in business_colleges:
                formatted_colleges.append({
                    'name': college['name'],
                    'location': college['location'],
                    'ranking': college['ranking'],
                    'cutoff': f"{college['cutoff']} | {college['entrance_exam']}",
                    'fees': college['fees'],
                    'placement': college['placement'],
                    'tier': college['tier'],
                    'naac_grade': college['naac_grade'],
                    'rating': college['rating']
                })
            
            recommendations.append({
                'field': 'Business & Management',
                'confidence': self._calculate_confidence(scores['business'], scores),
                'courses': [
                    {
                        'name': 'BBA (Bachelor of Business Administration)',
                        'duration': '3 years',
                        'trending_specializations': ['Digital Marketing', 'Fintech', 'International Business'],
                        'average_salary': '₹3-7 LPA',
                        'top_salary': '₹15+ LPA (After MBA)'
                    },
                    {
                        'name': 'B.Com (Hons)',
                        'duration': '3 years',
                        'trending_specializations': ['Accounting', 'Finance', 'Taxation'],
                        'average_salary': '₹3-6 LPA',
                        'top_salary': '₹12+ LPA'
                    },
                    {
                        'name': 'CA (Chartered Accountancy)',
                        'duration': '4-5 years',
                        'trending_specializations': ['Audit', 'Tax Consulting', 'Corporate Finance'],
                        'average_salary': '₹6-10 LPA',
                        'top_salary': '₹30+ LPA'
                    }
                ],
                'top_colleges': formatted_colleges if formatted_colleges else [
                    {'name': 'SRCC Delhi', 'location': 'Delhi', 'ranking': 1, 'cutoff': 'CUET Score > 700'}
                ],
                'entrance_exams': ['CUET', 'DU JAT', 'NPAT', 'SET', 'IPM Aptitude Test'],
                'career_opportunities': [
                    'Investment Banker',
                    'Management Consultant',
                    'Digital Marketing Manager',
                    'Financial Analyst',
                    'Entrepreneur'
                ],
                'growth_prospects': 'Excellent - Startup ecosystem booming'
            })
        
        # Law Recommendations
        elif primary_field == 'law':
            # Get real colleges from dataset
            law_colleges = self.college_manager.get_colleges_by_field('Law', 'LLB', max_results=10)
            
            # Format colleges for display
            formatted_colleges = []
            for college in law_colleges:
                formatted_colleges.append({
                    'name': college['name'],
                    'location': college['location'],
                    'ranking': college['ranking'],
                    'cutoff': f"{college['cutoff']} | {college['entrance_exam']}",
                    'fees': college['fees'],
                    'placement': college['placement'],
                    'tier': college['tier'],
                    'naac_grade': college['naac_grade'],
                    'rating': college['rating']
                })
            
            recommendations.append({
                'field': 'Law & Legal Studies',
                'confidence': self._calculate_confidence(scores['law'], scores),
                'courses': [
                    {
                        'name': 'BA LLB (5 Year Integrated)',
                        'duration': '5 years',
                        'trending_specializations': ['Corporate Law', 'IPR', 'Criminal Law', 'Cyber Law'],
                        'average_salary': '₹4-8 LPA',
                        'top_salary': '₹25+ LPA (Corporate Firms)'
                    },
                    {
                        'name': 'BBA LLB',
                        'duration': '5 years',
                        'trending_specializations': ['Business Law', 'Tax Law'],
                        'average_salary': '₹5-10 LPA',
                        'top_salary': '₹30+ LPA'
                    }
                ],
                'top_colleges': formatted_colleges if formatted_colleges else [
                    {'name': 'NLSIU Bangalore', 'location': 'Bangalore', 'ranking': 1, 'cutoff': 'CLAT Rank < 50'}
                ],
                'entrance_exams': ['CLAT', 'LSAT India', 'AILET', 'SET Law'],
                'career_opportunities': [
                    'Corporate Lawyer',
                    'Litigation Lawyer',
                    'Legal Advisor',
                    'Judge/Magistrate',
                    'Legal Consultant'
                ],
                'growth_prospects': 'Very Good - Growing demand for legal professionals'
            })
        
        # Design Recommendations
        elif primary_field == 'design':
            recommendations.append({
                'field': 'Design & Creative Arts',
                'confidence': self._calculate_confidence(scores['design'], scores),
                'courses': [
                    {
                        'name': 'B.Des (Bachelor of Design)',
                        'duration': '4 years',
                        'trending_specializations': ['UX/UI Design', 'Product Design', 'Fashion Design'],
                        'average_salary': '₹4-8 LPA',
                        'top_salary': '₹20+ LPA'
                    },
                    {
                        'name': 'B.Arch (Architecture)',
                        'duration': '5 years',
                        'trending_specializations': ['Sustainable Architecture', 'Urban Planning'],
                        'average_salary': '₹3-6 LPA',
                        'top_salary': '₹15+ LPA'
                    },
                    {
                        'name': 'BFA (Fine Arts)',
                        'duration': '4 years',
                        'trending_specializations': ['Animation', 'Graphic Design', 'Digital Art'],
                        'average_salary': '₹3-6 LPA',
                        'top_salary': '₹12+ LPA'
                    }
                ],
                'top_colleges': [
                    {'name': 'NID Ahmedabad', 'location': 'Ahmedabad', 'ranking': 1, 'cutoff': 'NID DAT Exam'},
                    {'name': 'NIFT Delhi', 'location': 'Delhi', 'ranking': 2, 'cutoff': 'NIFT Entrance'},
                    {'name': 'IIT Bombay IDC', 'location': 'Mumbai', 'ranking': 'Top 3', 'cutoff': 'UCEED Exam'},
                    {'name': 'Srishti Institute', 'location': 'Bangalore', 'ranking': 'Top 10', 'cutoff': 'Portfolio Review'},
                    {'name': 'Pearl Academy', 'location': 'Delhi/Mumbai', 'ranking': 'Top 15', 'cutoff': 'Entrance Test'}
                ],
                'entrance_exams': ['NID DAT', 'NIFT', 'UCEED', 'CEED', 'NATA'],
                'career_opportunities': [
                    'UX/UI Designer',
                    'Product Designer',
                    'Creative Director',
                    'Architect',
                    'Brand Consultant'
                ],
                'growth_prospects': 'Excellent - Digital design industry growing rapidly'
            })
        
        # Social Sciences Recommendations
        else:
            recommendations.append({
                'field': 'Social Sciences & Humanities',
                'confidence': self._calculate_confidence(scores['social_sciences'], scores),
                'courses': [
                    {
                        'name': 'BA Psychology',
                        'duration': '3 years',
                        'trending_specializations': ['Clinical Psychology', 'Organizational Psychology'],
                        'average_salary': '₹3-6 LPA',
                        'top_salary': '₹12+ LPA (After M.A./M.Phil)'
                    },
                    {
                        'name': 'BA Political Science',
                        'duration': '3 years',
                        'trending_specializations': ['Public Policy', 'International Relations'],
                        'average_salary': '₹3-5 LPA',
                        'top_salary': '₹15+ LPA (Civil Services)'
                    },
                    {
                        'name': 'BA Mass Communication',
                        'duration': '3 years',
                        'trending_specializations': ['Digital Journalism', 'PR & Advertising'],
                        'average_salary': '₹3-6 LPA',
                        'top_salary': '₹15+ LPA'
                    }
                ],
                'top_colleges': [
                    {'name': 'St. Stephen\'s College', 'location': 'Delhi', 'ranking': 1, 'cutoff': 'CUET Score > 700'},
                    {'name': 'Lady Shri Ram College', 'location': 'Delhi', 'ranking': 2, 'cutoff': 'CUET Score > 680'},
                    {'name': 'Presidency University', 'location': 'Kolkata', 'ranking': 'Top 5', 'cutoff': 'CUET Based'},
                    {'name': 'Fergusson College', 'location': 'Pune', 'ranking': 'Top 10', 'cutoff': '85%+ in 12th'},
                    {'name': 'Xavier\'s Mumbai', 'location': 'Mumbai', 'ranking': 'Top 15', 'cutoff': 'Entrance Test'}
                ],
                'entrance_exams': ['CUET', 'DU Entrance', 'BHU UET', 'JMI Entrance'],
                'career_opportunities': [
                    'Psychologist/Counselor',
                    'Civil Services Officer',
                    'Journalist/Content Writer',
                    'Social Worker',
                    'Research Analyst'
                ],
                'growth_prospects': 'Good - Growing awareness of mental health and social issues'
            })
        
        # Add alternative field if score is close
        if sorted_fields[1][1] >= sorted_fields[0][1] * 0.6:
            alternative_field = sorted_fields[1][0]
            alt_recommendation = self._get_alternative_recommendation(alternative_field, scores)
            if alt_recommendation:
                recommendations.append(alt_recommendation)
        
        return recommendations
    
    def _calculate_confidence(self, field_score: int, all_scores: Dict) -> str:
        """Calculate confidence level for recommendation"""
        total_score = sum(all_scores.values())
        if total_score == 0:
            return "Low"
        
        percentage = (field_score / total_score) * 100
        
        if percentage >= 50:
            return "High"
        elif percentage >= 30:
            return "Moderate"
        else:
            return "Low"
    
    def _get_alternative_recommendation(self, field: str, scores: Dict) -> Optional[Dict]:
        """Generate alternative recommendations"""
        field_map = {
            'engineering': ('Engineering & Technology (Alternative)', 'B.Tech/BE'),
            'medical': ('Medical & Healthcare (Alternative)', 'MBBS/BDS'),
            'business': ('Business & Management (Alternative)', 'BBA/B.Com'),
            'law': ('Law & Legal Studies (Alternative)', 'BA LLB'),
            'design': ('Design & Creative Arts (Alternative)', 'B.Des'),
            'social_sciences': ('Social Sciences (Alternative)', 'BA Programs')
        }
        
        if field in field_map:
            field_name, primary_course = field_map[field]
            return {
                'field': field_name,
                'confidence': self._calculate_confidence(scores[field], scores),
                'courses': [{'name': primary_course, 'note': 'Consider this as an alternative career path'}],
                'top_colleges': [{'name': 'Various Top Institutions', 'location': 'Pan India'}],
                'entrance_exams': ['Relevant entrance exams'],
                'career_opportunities': ['Multiple career paths available']
            }
        return None
