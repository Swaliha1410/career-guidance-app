"""
Career Guidance Application - Main Streamlit Interface
Professional UI with modular design and OOP principles
"""

import streamlit as st

from auth_manager import AuthManager

from models import Student, TenthGradeAssessment, TwelfthGradeAssessment
import plotly.graph_objects as go
import plotly.express as px


class CareerGuidanceApp:
    """Main application class orchestrating the career guidance system"""
    
    def __init__(self):
        self.auth_manager = AuthManager()
        self._initialize_session_state()
        self._configure_page()
    
    def _configure_page(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="Career Guidance System",
            page_icon="🎓",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS for professional look
        st.markdown("""
            <style>
            .main-header {
                font-size: 3rem;
                font-weight: bold;
                color: #1f77b4;
                text-align: center;
                padding: 20px;
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .sub-header {
                font-size: 1.5rem;
                color: #555;
                text-align: center;
                margin-bottom: 30px;
            }
            .info-card {
                background-color: #f0f2f6;
                padding: 20px;
                border-radius: 10px;
                border-left: 5px solid #1f77b4;
                margin: 10px 0;
            }
            .success-card {
                background-color: #d4edda;
                padding: 20px;
                border-radius: 10px;
                border-left: 5px solid #28a745;
                margin: 10px 0;
            }
            .warning-card {
                background-color: #fff3cd;
                padding: 20px;
                border-radius: 10px;
                border-left: 5px solid #ffc107;
                margin: 10px 0;
            }
            .stButton>button {
                width: 100%;
                background-color: #1f77b4;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
            }
            .stButton>button:hover {
                background-color: #145a8c;
            }
            </style>
        """, unsafe_allow_html=True)
    
    def _initialize_session_state(self):
        """Initialize session state variables"""
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'current_student' not in st.session_state:
            st.session_state.current_student = None
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'home'
        if 'assessment_started' not in st.session_state:
            st.session_state.assessment_started = False
        if 'answers' not in st.session_state:
            st.session_state.answers = {}
    
    def run(self):
        """Main application run method"""
        if not st.session_state.logged_in:
            self._show_landing_page()
        else:
            self._show_dashboard()
    
    def _show_landing_page(self):
        """Display landing page with login/signup"""
        # Left-aligned title at top
        st.markdown('<h1 style="font-size: 2.5rem; font-weight: 700; color: #000; margin: 0; text-align: left;">🎓 Career Guidance System</h1>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 1.1rem; color: #555; margin-top: 8px; text-align: left;">Your personalized path to academic and career success</p>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Full-width hero image with cover
        try:
            st.image("c.jpg", use_container_width=True)
        except:
            st.warning("Image file 'c.jpg' not found. Please add it to the app folder.")
        
        # Login/Signup tabs
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
        
        with tab1:
            self._show_login_form()
        
        with tab2:
            self._show_signup_form()
        
        # Features section
        st.markdown("---")
        st.markdown("### ✨ Why Choose Our Platform?")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div class="info-card">
                    <h4>🎯 Personalized Assessment</h4>
                    <p>Take our comprehensive interest-based questionnaire designed by education experts.</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="info-card">
                    <h4>🏆 Expert Recommendations</h4>
                    <p>Get tailored stream and course suggestions based on your unique profile.</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="info-card">
                    <h4>🏛️ Top Institutions</h4>
                    <p>Discover the best colleges and universities matching your aspirations.</p>
                </div>
            """, unsafe_allow_html=True)
    
    def _show_login_form(self):
        """Display login form"""
        st.markdown("### Welcome Back!")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if not username or not password:
                    st.error("Please fill in all fields!")
                else:
                    success, student, message = self.auth_manager.login(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.current_student = student
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
    
    def _show_signup_form(self):
        """Display signup form"""
        st.markdown("### Create Your Account")
        
        with st.form("signup_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input("Full Name", placeholder="John Doe")
                username = st.text_input("Username", placeholder="johndoe123")
                email = st.text_input("Email", placeholder="john@example.com")
            
            with col2:
                age = st.number_input("Age", min_value=14, max_value=25, value=16)
                academic_level = st.selectbox("Current Academic Level", ["10th", "12th"])
                password = st.text_input("Password", type="password", placeholder="Minimum 6 characters")
            
            agree = st.checkbox("I agree to the terms and conditions")
            submit = st.form_submit_button("Sign Up")
            
            if submit:
                if not all([full_name, username, email, password]):
                    st.error("Please fill in all fields!")
                elif not agree:
                    st.error("Please agree to the terms and conditions!")
                else:
                    success, message = self.auth_manager.register_student(
                        username, password, email, full_name, age, academic_level
                    )
                    if success:
                        st.success(message + " Please login to continue.")
                    else:
                        st.error(message)
    
    def _show_dashboard(self):
        """Display main dashboard after login"""
        student = st.session_state.current_student
        
        # Sidebar
        with st.sidebar:
            st.markdown(f"### Welcome, {student.get_full_name()}! 👋")
            st.markdown(f"**Academic Level:** {student.get_academic_level()}")
            st.markdown("---")
            
            menu_options = ["🏠 Home", "📝 Take Assessment", "📊 My Results", "ℹ️ About"]
            # give the radio a stable session key so we can set it programmatically
            choice = st.radio("Navigation", menu_options, key="nav_choice")
            
            st.markdown("---")
            if st.button("🚪 Logout"):
                st.session_state.logged_in = False
                st.session_state.current_student = None
                st.session_state.assessment_started = False
                st.session_state.answers = {}
                st.rerun()
        
        # Allow programmatic navigation via `current_page` flag (set elsewhere)
        if 'current_page' in st.session_state and st.session_state.current_page == 'assessment':
            # prefer the programmatic navigation, then clear the flag
            choice = "📝 Take Assessment"
            st.session_state.current_page = 'home'

        # Main content
        if choice == "🏠 Home":
            self._show_home_dashboard()
        elif choice == "📝 Take Assessment":
            self._show_assessment()
        elif choice == "📊 My Results":
            self._show_results()
        elif choice == "ℹ️ About":
            self._show_about()
    
    def _show_home_dashboard(self):
        """Show home dashboard"""
        student = st.session_state.current_student
        
        st.markdown('<h1 class="main-header">Your Career Journey Dashboard</h1>', unsafe_allow_html=True)
        
        # Status cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Academic Level", student.get_academic_level())
        
        with col2:
            status = "✅ Completed" if student.is_profile_completed() else "⏳ Pending"
            st.metric("Assessment Status", status)
        
        with col3:
            recs = len(student.get_recommendations())
            st.metric("Recommendations", f"{recs} Available" if recs > 0 else "Take Assessment")
        
        st.markdown("---")
        
        # Quick actions
        if not student.is_profile_completed():
            st.markdown("""
                <div class="warning-card">
                    <h3>🎯 Get Started!</h3>
                    <p>Complete your interest assessment to receive personalized career guidance and recommendations.</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("Start Assessment Now →", key="start_assessment"):
                # set a navigation flag instead of touching the radio's session key
                st.session_state.current_page = 'assessment'
                st.rerun()
        else:
            st.markdown("""
                <div class="success-card">
                    <h3>🎉 Assessment Completed!</h3>
                    <p>View your personalized recommendations in the 'My Results' section.</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Information section
        st.markdown("---")
        st.markdown("### 📚 What's Next?")
        
        if student.get_academic_level() == "10th":
            st.markdown("""
                - **Complete the Assessment**: Answer questions about your interests and skills
                - **Review Stream Options**: Explore Science, Commerce, and Arts streams
                - **Find Junior Colleges**: Get recommendations for top institutions
                - **Plan Your Path**: Understand future career opportunities
            """)
        else:
            st.markdown("""
                - **Complete the Assessment**: Discover your ideal career field
                - **Explore Courses**: Learn about trending graduation programs
                - **Check Salary Insights**: Understand career prospects and packages
                - **Find Universities**: Get matched with top colleges nationwide
            """)
    
    def _show_assessment(self):
        """Show assessment questionnaire"""
        student = st.session_state.current_student
        
        st.markdown('<h1 class="main-header">Career Interest Assessment</h1>', unsafe_allow_html=True)
        
        # Create appropriate assessment based on academic level
        if student.get_academic_level() == "10th":
            assessment = TenthGradeAssessment(student)
            st.markdown("### 📋 Stream Selection Questionnaire")
            st.info("Answer these questions to help us recommend the best stream for your 11th and 12th grade.")
        else:
            assessment = TwelfthGradeAssessment(student)
            st.markdown("### 📋 Career Path Questionnaire")
            st.info("Answer these questions to discover your ideal graduation course and career field.")
        
        questions = assessment.generate_questions()
        
        # Progress bar
        answered = len(st.session_state.answers)
        progress = answered / len(questions)
        st.progress(progress)
        st.markdown(f"**Progress:** {answered}/{len(questions)} questions answered")
        
        st.markdown("---")
        
        # Display questions
        with st.form("assessment_form"):
            for question in questions:
                st.markdown(f"### Q{question['id']}: {question['question']}")
                
                # Get current answer if exists
                current_answer = st.session_state.answers.get(question['id'])
                
                # Radio button for options
                answer = st.radio(
                    "Select your answer:",
                    options=list(question['options'].keys()),
                    key=f"q_{question['id']}",
                    index=list(question['options'].keys()).index(current_answer) if current_answer else 0
                )
                
                st.session_state.answers[question['id']] = answer
                st.markdown("---")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                submit = st.form_submit_button("Submit Assessment")
            
            if submit:
                if len(st.session_state.answers) < len(questions):
                    st.error("Please answer all questions before submitting!")
                else:
                    # Calculate scores
                    scores = assessment.calculate_scores(st.session_state.answers)
                    
                    # Generate recommendations
                    recommendations = assessment.generate_recommendations(scores)
                    
                    # Update student record
                    student.set_assessment_results(scores)
                    student.set_recommendations(recommendations)
                    
                    # Save to database
                    self.auth_manager.update_student_results(
                        student.get_username(),
                        scores,
                        recommendations
                    )
                    
                    st.success("✅ Assessment completed successfully!")
                    st.balloons()
                    
                    # Reset answers
                    st.session_state.answers = {}
                    
                    # Wait a moment before rerun
                    import time
                    time.sleep(2)
                    st.rerun()
    
    def _show_results(self):
        """Display assessment results and recommendations"""
        student = st.session_state.current_student
        
        st.markdown('<h1 class="main-header">Your Personalized Recommendations</h1>', unsafe_allow_html=True)
        
        if not student.is_profile_completed():
            st.warning("⚠️ Please complete the assessment first to view recommendations.")
            if st.button("Take Assessment Now"):
                # set navigation flag instead of directly mutating radio widget state
                st.session_state.current_page = 'assessment'
                st.rerun()
            return
        
        # Get results
        scores = student.get_assessment_results()
        recommendations = student.get_recommendations()
        
        # Display scores visualization
        st.markdown("### 📊 Your Interest Profile")
        
        # Create visualization based on academic level
        if student.get_academic_level() == "10th":
            self._visualize_10th_results(scores)
        else:
            self._visualize_12th_results(scores)
        
        st.markdown("---")
        
        # Display recommendations
        st.markdown("### 🎯 Recommended Paths")
        
        for idx, rec in enumerate(recommendations):
            with st.expander(f"{'⭐ PRIMARY' if idx == 0 else '🔸 ALTERNATIVE'}: {rec.get('stream') or rec.get('field')}", expanded=(idx == 0)):
                self._display_recommendation(rec, student.get_academic_level())
    
    def _visualize_10th_results(self, scores: dict):
        """Visualize 10th grade assessment scores"""
        # Bar chart
        fig = go.Figure(data=[
            go.Bar(
                x=list(scores.keys()),
                y=list(scores.values()),
                marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1'],
                text=list(scores.values()),
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Stream Preference Scores",
            xaxis_title="Stream",
            yaxis_title="Score",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Pie chart
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pie = go.Figure(data=[go.Pie(
                labels=list(scores.keys()),
                values=list(scores.values()),
                hole=.3,
                marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1']
            )])
            fig_pie.update_layout(title="Score Distribution", height=300)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("#### Score Breakdown")
            total = sum(scores.values())
            for stream, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
                percentage = (score / total * 100) if total > 0 else 0
                st.metric(stream.capitalize(), f"{score} points", f"{percentage:.1f}%")
    
    def _visualize_12th_results(self, scores: dict):
        """Visualize 12th grade assessment scores"""
        # Radar chart
        categories = list(scores.keys())
        values = list(scores.values())
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=[cat.replace('_', ' ').title() for cat in categories],
            fill='toself',
            marker_color='#667eea'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(values) + 5]
                )),
            showlegend=False,
            title="Career Field Interest Profile",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Bar chart comparison
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        fig_bar = go.Figure(data=[
            go.Bar(
                x=[s[0].replace('_', ' ').title() for s in sorted_scores],
                y=[s[1] for s in sorted_scores],
                marker_color=px.colors.sequential.Viridis,
                text=[s[1] for s in sorted_scores],
                textposition='auto',
            )
        ])
        
        fig_bar.update_layout(
            title="Career Field Preference Ranking",
            xaxis_title="Field",
            yaxis_title="Interest Score",
            height=400
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    def _display_recommendation(self, rec: dict, academic_level: str):
        """Display individual recommendation details"""
        # Confidence badge
        confidence = rec.get('confidence', 'Moderate')
        confidence_color = {
            'High': '🟢',
            'Moderate': '🟡',
            'Low': '🔴'
        }
        st.markdown(f"**Confidence Level:** {confidence_color.get(confidence, '⚪')} {confidence}")
        
        st.markdown("---")
        
        if academic_level == "10th":
            # 10th grade recommendations
            st.markdown("#### 📚 Subjects")
            subjects_cols = st.columns(len(rec.get('subjects', [])))
            for idx, subject in enumerate(rec.get('subjects', [])):
                with subjects_cols[idx]:
                    st.info(subject)
            
            st.markdown("#### 🚀 Career Paths")
            for career in rec.get('career_paths', []):
                st.markdown(f"- {career}")
            
            st.markdown("#### 🏫 Recommended Junior Colleges")
            for college in rec.get('colleges', []):
                # Check if it's from the dataset (has more fields)
                if 'tier' in college and 'rating' in college:
                    st.markdown(f"""
                        <div class="info-card">
                            <strong>{college['name']}</strong> | ⭐ {college.get('rating', 'N/A')}/5.0<br>
                            🏆 {college.get('tier', 'N/A')} | 📊 NAAC: {college.get('naac_grade', 'N/A')} | 🎖️ NIRF Rank: {college.get('nirf_rank', 'N/A')}<br>
                            📍 {college['location']} | 🎯 Cutoff: {college.get('cutoff', 'N/A')}<br>
                            💰 Fees: {college.get('fees', 'N/A')} | 🏠 Hostel: {college.get('hostel_fees', 'N/A')}<br>
                            💼 {college.get('placement', 'N/A')} | 🎓 {college.get('scholarships', 'Merit/Need based')}<br>
                            🏫 Campus: {college.get('campus_size', 'N/A')}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    # Fallback for old format
                    st.markdown(f"""
                        <div class="info-card">
                            <strong>{college['name']}</strong><br>
                            📍 {college['location']} | 📄 {college.get('type', 'N/A')}
                        </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("#### 📝 Entrance Exams to Prepare")
            exam_cols = st.columns(min(3, len(rec.get('entrance_exams', []))))
            for idx, exam in enumerate(rec.get('entrance_exams', [])):
                with exam_cols[idx % 3]:
                    st.success(exam)
            
            st.markdown("#### 💡 Skills to Develop")
            for skill in rec.get('skills_needed', []):
                st.markdown(f"- {skill}")
        
        else:
            # 12th grade recommendations
            st.markdown("#### 🎓 Recommended Courses")
            for course in rec.get('courses', []):
                st.markdown(f"""
                    <div class="success-card">
                        <h4>{course['name']}</h4>
                        <p><strong>Duration:</strong> {course.get('duration', 'N/A')}</p>
                        <p><strong>Trending Specializations:</strong> {', '.join(course.get('trending_specializations', []))}</p>
                        <p><strong>💰 Average Salary:</strong> {course.get('average_salary', 'N/A')}</p>
                        <p><strong>🌟 Top Package:</strong> {course.get('top_salary', 'N/A')}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("#### 🏛️ Top Colleges & Universities")
            for college in rec.get('top_colleges', []):
                # Check if it's from the dataset (has more fields)
                if 'tier' in college and 'rating' in college:
                    st.markdown(f"""
                        <div class="info-card">
                            <strong>{college['name']}</strong> | ⭐ {college.get('rating', 'N/A')}/5.0<br>
                            🏆 {college.get('tier', 'N/A')} | 📊 NAAC: {college.get('naac_grade', 'N/A')} | 🎖️ NIRF Rank: {college.get('ranking', 'N/A')}<br>
                            📍 {college['location']} | 🎯 {college.get('cutoff', 'N/A')}<br>
                            💰 Fees: {college.get('fees', 'N/A')} | 🏠 Hostel: {college.get('hostel_fees', 'N/A')}<br>
                            💼 {college.get('placement', 'N/A')}<br>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    # Fallback for old format
                    st.markdown(f"""
                        <div class="info-card">
                            <strong>{college['name']}</strong> - Rank: {college.get('ranking', 'N/A')}<br>
                            📍 {college['location']} | 🎯 Cutoff: {college.get('cutoff', 'N/A')}
                        </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("#### 📝 Entrance Exams")
            exam_text = ", ".join(rec.get('entrance_exams', []))
            st.info(f"**Key Exams:** {exam_text}")
            
            st.markdown("#### 💼 Career Opportunities")
            for opportunity in rec.get('career_opportunities', []):
                st.markdown(f"- {opportunity}")
            
            st.markdown("#### 📈 Growth Prospects")
            st.success(rec.get('growth_prospects', 'Good career prospects in this field'))
    
    def _show_about(self):
        """Show about page"""
        st.markdown('<h1 class="main-header">About Career Guidance System</h1>', unsafe_allow_html=True)
        
        st.markdown("""
            ### 🎯 Our Mission
            
            To empower students with data-driven, personalized career guidance that helps them make informed 
            decisions about their academic and professional futures.
            
            ### 💡 How It Works
            
            1. **Sign Up**: Create your account with basic information
            2. **Take Assessment**: Complete our comprehensive questionnaire
            3. **Get Recommendations**: Receive personalized stream/course suggestions
            4. **Explore Options**: Learn about colleges, careers, and salary prospects
            
            ### 🛠️ Technology Stack
            
            This application is built using:
            - **Python**: Core programming language
            - **Streamlit**: Interactive web interface
            - **Object-Oriented Programming**: Modular, scalable architecture
            - **Plotly**: Data visualization
            
            ### 📊 Features
            
            #### For 10th Grade Students
            - Stream recommendation (Science, Commerce, Arts)
            - Junior college suggestions
            - Career pathway guidance
            - Skills development roadmap
            
            #### For 12th Grade Students
            - Graduation course recommendations
            - Trending field analysis
            - Salary package insights
            - Top university suggestions
            - Entrance exam guidance
            
            ### 🔒 Privacy & Security
            
            Your data is securely stored and never shared with third parties. We use industry-standard
            encryption for password protection.
            
            ### 📞 Support
            
            For queries or support, please contact: support@careerguidance.com
            
            ---
            
            <div class="info-card">
                <p style="text-align: center; margin: 0;">
                    <strong>Version 1.0.0</strong> | Developed with ❤️ for Students
                </p>
            </div>
        """, unsafe_allow_html=True)


def main():
    """Main entry point"""
    app = CareerGuidanceApp()
    app.run()


if __name__ == "__main__":
    main()
