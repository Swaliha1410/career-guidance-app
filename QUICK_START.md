# 🚀 Quick Start Guide

## Running the Career Guidance Application

### Option 1: Quick Start (Recommended)

```bash
# Navigate to the project directory
cd career_guidance_app

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The application will open automatically in your browser at `http://localhost:8501`

### Option 2: Step by Step

1. **Install Python Dependencies**
   ```bash
   pip install streamlit==1.31.0 plotly==5.18.0
   ```

2. **Run Application**
   ```bash
   streamlit run app.py
   ```

## First Time Usage

### Create an Account

1. Go to the **Sign Up** tab
2. Fill in your information:
   - **Full Name**: Your complete name
   - **Username**: Choose a unique username
   - **Email**: Your email address
   - **Age**: Your current age (14-25)
   - **Academic Level**: Select "10th" or "12th"
   - **Password**: Minimum 6 characters
3. Check "I agree to the terms and conditions"
4. Click **Sign Up**

### Login and Start

1. Switch to **Login** tab
2. Enter your username and password
3. Click **Login**
4. You'll see your personalized dashboard

### Take the Assessment

1. Click **"📝 Take Assessment"** from the sidebar
2. Read each question carefully
3. Select the answer that best matches your interests
4. Answer all 8 questions
5. Click **Submit Assessment**
6. View your results!

## Sample Test Accounts

You can create test accounts with different profiles:

### Test Student 1 (10th Grade - Science Interest)
- Username: `john_science`
- Sample answers: Select options related to Mathematics, Physics, Engineering

### Test Student 2 (10th Grade - Commerce Interest)
- Username: `jane_commerce`
- Sample answers: Select options related to Economics, Business, Finance

### Test Student 3 (12th Grade - Engineering Interest)
- Username: `alex_tech`
- Sample answers: Select options related to Technology, Innovation, Coding

## Troubleshooting

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### Missing Dependencies
```bash
pip install --upgrade streamlit plotly
```

### Permission Issues
```bash
# On Windows (run as administrator)
pip install --user -r requirements.txt

# On Mac/Linux
pip3 install -r requirements.txt
```

## Features to Explore

✅ **User Registration**: Secure signup with validation  
✅ **Assessment System**: Comprehensive questionnaire  
✅ **Visual Results**: Interactive charts and graphs  
✅ **Recommendations**: Personalized career guidance  
✅ **College Information**: Top institutions and cutoffs  
✅ **Salary Insights**: Career earning potential  

## Tips for Best Experience

1. **Answer Honestly**: The assessment works best with genuine responses
2. **Review All Options**: Check primary and alternative recommendations
3. **Explore Details**: Expand each recommendation card for full information
4. **Save Results**: Take screenshots or notes of your recommendations
5. **Retake if Needed**: You can retake the assessment anytime

## Getting Help

- Check the **About** section in the app for detailed information
- Review the README.md for technical details
- Examine the code comments for understanding the logic

---

**Ready to discover your perfect career path? Let's get started! 🎓**
