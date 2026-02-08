# 🎓 Career Guidance Application

A professional, full-featured career guidance system built with Python and Streamlit, demonstrating advanced Object-Oriented Programming principles.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technical Architecture](#technical-architecture)
- [OOP Principles Demonstrated](#oop-principles-demonstrated)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)

## 🎯 Overview

The Career Guidance Application is a comprehensive system designed to help students in grades 10 and 12 make informed decisions about their academic and career paths. The application provides personalized recommendations based on interest assessments, aptitude analysis, and career preferences.

### Key Capabilities

- **For 10th Grade Students**: Stream selection (Science/Commerce/Arts), junior college recommendations, and career pathway guidance
- **For 12th Grade Students**: Graduation course suggestions, trending branches, salary insights, and top university recommendations

## ✨ Features

### User Management
- Secure user registration and authentication
- Password hashing for security
- Session management
- Profile completion tracking

### Assessment System
- **10th Grade Assessment**: 8 comprehensive questions analyzing subject preferences, career interests, problem-solving approaches, and skills
- **12th Grade Assessment**: 8 career-focused questions evaluating field interests, work environment preferences, and career priorities

### Personalized Recommendations
- Stream/field recommendations with confidence levels
- Alternative path suggestions
- Course details with trending specializations
- Salary package information (average and top packages)
- Top colleges and universities with rankings and cutoffs
- Entrance exam guidance
- Skills development roadmap

### Data Visualization
- Interactive bar charts and pie charts (10th grade)
- Radar charts for career field analysis (12th grade)
- Score breakdowns and comparisons
- Progress tracking

### Professional UI/UX
- Modern, responsive design
- Intuitive navigation
- Custom CSS styling
- Progress indicators
- Visual feedback (success/error messages, balloons)

## 🏗️ Technical Architecture

### Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python 3.8+
- **Data Visualization**: Plotly
- **Data Storage**: JSON-based file system
- **Security**: SHA-256 password hashing

### Design Patterns

1. **Model-View-Controller (MVC)**
   - Models: User, Student, Assessment classes
   - View: Streamlit UI components
   - Controller: CareerGuidanceApp orchestrator

2. **Factory Pattern**
   - Assessment creation based on academic level

3. **Strategy Pattern**
   - Different assessment strategies for 10th and 12th grades

## 🎓 OOP Principles Demonstrated

### 1. Encapsulation

**Private Attributes and Methods**
```python
class User:
    def __init__(self, username, password, email):
        self.__username = username          # Private
        self.__password = self.__hash_password(password)  # Private
        self.__email = email               # Private
    
    def __hash_password(self, password):   # Private method
        return hashlib.sha256(password.encode()).hexdigest()
    
    # Public getters
    def get_username(self):
        return self.__username
```

**Benefits**:
- Data hiding and protection
- Controlled access through getters
- Password security through private hashing

### 2. Inheritance

**Class Hierarchy**
```python
class User:
    # Base class with common user functionality
    pass

class Student(User):
    # Inherits from User, adds student-specific features
    def __init__(self, username, password, email, full_name, age, academic_level):
        super().__init__(username, password, email)  # Call parent constructor
        self.__full_name = full_name
        self.__academic_level = academic_level
```

**Benefits**:
- Code reusability
- Logical class hierarchy
- Extension of base functionality

### 3. Polymorphism

**Abstract Base Class and Method Overriding**
```python
class Assessment(ABC):
    @abstractmethod
    def generate_questions(self) -> List[Dict]:
        pass
    
    @abstractmethod
    def calculate_scores(self, answers: Dict) -> Dict:
        pass

class TenthGradeAssessment(Assessment):
    def generate_questions(self) -> List[Dict]:
        # 10th grade specific implementation
        pass
    
    def calculate_scores(self, answers: Dict) -> Dict:
        # 10th grade specific scoring
        pass

class TwelfthGradeAssessment(Assessment):
    def generate_questions(self) -> List[Dict]:
        # 12th grade specific implementation
        pass
```

**Benefits**:
- Different implementations for different student levels
- Consistent interface across assessment types
- Easy to add new assessment types

### 4. Abstraction

**Abstract Methods Hide Implementation Details**
```python
# Users of the class don't need to know HOW assessments work
assessment = TenthGradeAssessment(student)
questions = assessment.generate_questions()  # Abstract interface
scores = assessment.calculate_scores(answers)
recommendations = assessment.generate_recommendations(scores)
```

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step-by-Step Installation

1. **Clone or download the project**
```bash
cd career_guidance_app
```

2. **Install required packages**
```bash
pip install -r requirements.txt
```

3. **Verify installation**
```bash
python -c "import streamlit; import plotly; print('All dependencies installed!')"
```

## 🚀 Usage

### Running the Application

1. **Start the Streamlit server**
```bash
streamlit run app.py
```

2. **Access the application**
   - The application will automatically open in your default browser
   - If not, navigate to: `http://localhost:8501`

### User Workflow

#### For New Users

1. **Sign Up**
   - Click on the "Sign Up" tab
   - Fill in your details:
     - Full Name
     - Username (unique)
     - Email
     - Age (14-25)
     - Academic Level (10th or 12th)
     - Password (minimum 6 characters)
   - Agree to terms and conditions
   - Click "Sign Up"

2. **Login**
   - Switch to "Login" tab
   - Enter username and password
   - Click "Login"

3. **Take Assessment**
   - Navigate to "📝 Take Assessment"
   - Answer all 8 questions thoughtfully
   - Click "Submit Assessment"

4. **View Results**
   - Navigate to "📊 My Results"
   - Review your interest profile visualization
   - Explore personalized recommendations
   - Check college suggestions and career paths

#### For Returning Users

1. Login with existing credentials
2. View updated dashboard
3. Review previous results
4. Retake assessment if needed

## 📁 Project Structure

```
career_guidance_app/
│
├── app.py                  # Main Streamlit application
│   ├── CareerGuidanceApp   # Main application class
│   ├── Page configurations
│   ├── UI components
│   └── Visualization methods
│
├── models.py               # Data models and business logic
│   ├── User                # Base user class (Encapsulation)
│   ├── Student             # Student class (Inheritance)
│   ├── Assessment          # Abstract base class (Polymorphism)
│   ├── TenthGradeAssessment    # 10th grade implementation
│   └── TwelfthGradeAssessment  # 12th grade implementation
│
├── auth_manager.py         # Authentication and user management
│   └── AuthManager         # Handles registration, login, data persistence
│
├── requirements.txt        # Project dependencies
├── README.md              # This file
└── users.json             # User data storage (auto-generated)
```

## 🎨 Key Components Explained

### 1. Models (models.py)

#### User Class
- Manages basic user information
- Implements password hashing
- Provides secure access through getters

#### Student Class
- Extends User with student-specific data
- Stores assessment results and recommendations
- Tracks profile completion status

#### Assessment Classes
- Abstract base defines common interface
- TenthGradeAssessment implements stream selection logic
- TwelfthGradeAssessment implements career field analysis
- Both calculate scores and generate recommendations

### 2. Authentication Manager (auth_manager.py)

- User registration with validation
- Secure login verification
- JSON-based data persistence
- Session management support

### 3. Main Application (app.py)

- Streamlit UI orchestration
- Navigation and routing
- Form handling
- Data visualization
- Result presentation

## 📊 Assessment Logic

### 10th Grade Assessment

**Question Categories**:
1. Subject preferences
2. Career interests
3. Problem-solving approach
4. Activity preferences
5. Personal strengths
6. Field excitement
7. Free time activities
8. Motivational factors

**Scoring System**:
- Each answer contributes points to one or more streams
- Points range from 0-3 per question
- Total scores determine primary and alternative recommendations

**Recommendation Confidence**:
- High: ≥60% of total score
- Moderate: 40-59% of total score
- Low: <40% of total score

### 12th Grade Assessment

**Question Categories**:
1. Field alignment
2. Work environment preferences
3. Skill set analysis
4. Subject performance
5. Career priorities
6. Study duration willingness
7. Challenge preferences
8. Industry trend interests

**Scoring System**:
- Evaluates 6 career fields: Engineering, Medical, Business, Law, Design, Social Sciences
- Point allocation based on answer relevance
- Multi-dimensional scoring for comprehensive analysis

## 🔐 Security Features

1. **Password Hashing**: SHA-256 encryption
2. **Input Validation**: Server-side validation for all inputs
3. **Session Management**: Secure session state handling
4. **Data Privacy**: Local JSON storage, no external sharing

## 🎯 Future Enhancements

### Planned Features

1. **Database Integration**
   - PostgreSQL/MySQL for better data management
   - User activity logging
   - Historical data analysis

2. **Advanced Analytics**
   - Machine learning for better recommendations
   - Predictive career success modeling
   - Trend analysis

3. **Enhanced Features**
   - Email verification
   - Password reset functionality
   - Profile editing
   - Assessment retake with comparison

4. **Content Expansion**
   - More detailed college information
   - Scholarship opportunities
   - Alumni testimonials
   - Video guidance

5. **Social Features**
   - Discussion forums
   - Mentor connections
   - Peer comparison (anonymized)

6. **Export Options**
   - PDF report generation
   - Resume building
   - Progress tracking dashboard

7. **Mobile Optimization**
   - Responsive design improvements
   - Progressive Web App (PWA)
   - Native mobile app

## 📝 Contributing

This is an educational project demonstrating OOP principles and Streamlit development. Feel free to:
- Fork the project
- Add new features
- Improve the UI/UX
- Enhance the recommendation algorithm
- Add more assessment questions

## 📄 License

This project is created for educational purposes. Feel free to use and modify as needed.

## 👥 Credits

**Developed by**: Professional Python Developer
**Framework**: Streamlit
**Visualization**: Plotly

---

## 🎓 Educational Value

This project demonstrates:
- Real-world application of OOP principles
- Professional Python development practices
- Modern web application architecture
- User-centric design
- Data-driven decision making

Perfect for:
- Learning OOP concepts in practice
- Understanding Streamlit development
- Building career guidance systems
- Creating assessment applications

---

**For questions or support, please open an issue in the repository.**

Made with ❤️ for students pursuing their dreams!
