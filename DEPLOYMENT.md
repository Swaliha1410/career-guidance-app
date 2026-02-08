# 🚀 Deployment & Usage Instructions

## Complete Guide to Running the Career Guidance Application

---

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Running the Application](#running-the-application)
4. [User Guide](#user-guide)
5. [Testing the Application](#testing-the-application)
6. [Troubleshooting](#troubleshooting)
7. [Project Files Overview](#project-files-overview)

---

## System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum
- **Storage**: 100MB free space
- **OS**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 20.04+)
- **Browser**: Chrome, Firefox, Safari, or Edge (latest versions)

### Required Python Packages
- streamlit >= 1.31.0
- plotly >= 5.18.0

---

## Installation Steps

### Step 1: Verify Python Installation

```bash
# Check Python version
python --version
# or
python3 --version

# Should show Python 3.8 or higher
```

If Python is not installed, download from: https://www.python.org/downloads/

### Step 2: Navigate to Project Directory

```bash
cd career_guidance_app
```

### Step 3: Install Dependencies

**Option A: Using requirements.txt (Recommended)**
```bash
pip install -r requirements.txt
```

**Option B: Manual Installation**
```bash
pip install streamlit==1.31.0
pip install plotly==5.18.0
```

**For systems requiring --break-system-packages:**
```bash
pip install -r requirements.txt --break-system-packages
```

### Step 4: Verify Installation

```bash
python -c "import streamlit; import plotly; print('✅ All packages installed successfully!')"
```

---

## Running the Application

### Method 1: Quick Start (Recommended)

```bash
streamlit run app.py
```

The application will automatically open in your default browser at `http://localhost:8501`

### Method 2: Custom Port

If port 8501 is busy:
```bash
streamlit run app.py --server.port 8502
```

### Method 3: Background Mode

**Windows:**
```bash
start streamlit run app.py
```

**Mac/Linux:**
```bash
streamlit run app.py &
```

### Stopping the Application

- Press `Ctrl+C` in the terminal
- Or close the terminal window

---

## User Guide

### Complete Workflow

#### 1️⃣ Registration (First Time Users)

1. Open the application
2. Click the **"Sign Up"** tab
3. Fill in all required fields:
   - **Full Name**: Your complete name (e.g., "John Doe")
   - **Username**: Choose a unique identifier (e.g., "john_doe123")
   - **Email**: Valid email address (e.g., "john@example.com")
   - **Age**: Must be between 14-25
   - **Academic Level**: Select "10th" or "12th"
   - **Password**: Minimum 6 characters (will be encrypted)
4. Check "I agree to the terms and conditions"
5. Click **"Sign Up"**
6. Success message appears

#### 2️⃣ Login

1. Switch to **"Login"** tab
2. Enter your username
3. Enter your password
4. Click **"Login"**
5. Dashboard loads

#### 3️⃣ Dashboard Overview

After login, you'll see:
- **Sidebar**: Navigation menu
  - 🏠 Home
  - 📝 Take Assessment
  - 📊 My Results
  - ℹ️ About
  - 🚪 Logout

- **Main Area**: Dashboard with status cards
  - Academic Level
  - Assessment Status
  - Available Recommendations

#### 4️⃣ Taking the Assessment

1. Click **"📝 Take Assessment"** from sidebar
2. Read the introduction carefully
3. Answer all 8 questions:
   - Read each question thoroughly
   - Select the option that best represents you
   - Be honest - this affects your recommendations
4. Monitor progress bar (shows X/8 questions answered)
5. Click **"Submit Assessment"** when all questions are answered
6. Wait for processing (2-3 seconds)
7. Success message and confetti appear!

#### 5️⃣ Viewing Results

1. Click **"📊 My Results"** from sidebar
2. View visualizations:
   - **For 10th Grade**: Bar charts and pie charts showing stream preferences
   - **For 12th Grade**: Radar charts and ranking charts showing career fields
3. Review recommendations:
   - Primary recommendation (detailed)
   - Alternative recommendation (if applicable)
4. Explore detailed information:
   - Click on recommendation cards to expand
   - View subjects/courses
   - Check college recommendations
   - See entrance exam requirements
   - Review salary information (12th grade)

---

## Testing the Application

### Sample Test Scenarios

#### Test Case 1: 10th Grade - Science Stream

**Profile:**
- Academic Level: 10th
- Answers: Select options emphasizing:
  - Mathematics and Physics
  - Engineering or Medical careers
  - Logical thinking
  - Science experiments
  - Problem-solving strengths

**Expected Result:**
- Primary recommendation: Science stream
- High confidence level
- IIT/Medical college recommendations

#### Test Case 2: 10th Grade - Commerce Stream

**Profile:**
- Academic Level: 10th
- Answers: Select options emphasizing:
  - Economics and Business
  - Finance careers
  - Data analysis
  - Business projects
  - Numerical abilities

**Expected Result:**
- Primary recommendation: Commerce stream
- Business and finance career paths
- CA/CS suggestions

#### Test Case 3: 12th Grade - Engineering

**Profile:**
- Academic Level: 12th
- Answers: Select options emphasizing:
  - Technology and Innovation
  - Tech companies
  - Coding skills
  - Mathematics/CS subjects
  - High salary priority

**Expected Result:**
- Primary recommendation: Engineering & Technology
- B.Tech courses with specializations
- IIT/NIT college recommendations
- Salary range information

#### Test Case 4: 12th Grade - Medical

**Profile:**
- Academic Level: 12th
- Answers: Select options emphasizing:
  - Healthcare and Medicine
  - Hospital environments
  - Empathy and care
  - Biology/Chemistry
  - Helping people

**Expected Result:**
- Primary recommendation: Medical & Healthcare
- MBBS/BDS courses
- AIIMS/Medical college recommendations

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Module Not Found Error
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution:**
```bash
pip install streamlit plotly --upgrade
```

#### Issue 2: Port Already in Use
```
Error: Port 8501 is already in use
```

**Solution:**
```bash
# Use different port
streamlit run app.py --server.port 8502

# Or kill existing process
# Windows: netstat -ano | findstr :8501
# Mac/Linux: lsof -ti:8501 | xargs kill
```

#### Issue 3: Permission Denied

**Solution:**
```bash
# Install with user flag
pip install --user -r requirements.txt

# Or use sudo (Mac/Linux)
sudo pip install -r requirements.txt
```

#### Issue 4: Browser Doesn't Open

**Solution:**
- Manually open browser and go to: `http://localhost:8501`
- Or disable auto-open:
```bash
streamlit run app.py --server.headless true
```

#### Issue 5: Data Not Persisting

**Solution:**
- Check if `users.json` file is created in the project directory
- Ensure write permissions for the directory
- Verify file is not corrupted (should be valid JSON)

#### Issue 6: Slow Performance

**Solution:**
- Close other browser tabs
- Restart the Streamlit server
- Clear browser cache
- Ensure sufficient RAM available

---

## Project Files Overview

### Core Application Files

```
career_guidance_app/
│
├── app.py                      # Main Streamlit application (Run this!)
├── models.py                   # Data models (User, Student, Assessment)
├── auth_manager.py             # Authentication system
├── requirements.txt            # Python dependencies
│
├── users.json                  # User database (auto-generated)
│
├── README.md                   # Complete documentation
├── QUICK_START.md             # Quick start guide
├── OOP_PRINCIPLES.md          # OOP concepts explained
└── DEPLOYMENT.md              # This file
```

### File Descriptions

| File | Purpose | Size |
|------|---------|------|
| `app.py` | Main application entry point, UI logic | ~600 lines |
| `models.py` | OOP classes and business logic | ~800 lines |
| `auth_manager.py` | User management and authentication | ~150 lines |
| `requirements.txt` | Package dependencies | ~2 lines |
| `users.json` | User data storage | Auto-generated |

### Auto-Generated Files

- **users.json**: Created when first user registers
  - Stores user credentials (hashed passwords)
  - Stores assessment results
  - Stores recommendations
  - Format: JSON

---

## Development Mode

### Running with Debug Output

```bash
streamlit run app.py --logger.level=debug
```

### Enabling File Watching

```bash
streamlit run app.py --server.fileWatcherType=auto
```

### Development Server Configuration

Create `.streamlit/config.toml`:
```toml
[server]
port = 8501
headless = false
runOnSave = true

[browser]
gatherUsageStats = false
```

---

## Production Deployment

### Option 1: Streamlit Cloud (Free)

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect repository
4. Deploy!

### Option 2: Local Server

```bash
# Run on all network interfaces
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```

### Option 3: Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t career-guidance .
docker run -p 8501:8501 career-guidance
```

---

## Security Best Practices

### For Production Use

1. **Change Default Settings**
   - Use environment variables for sensitive data
   - Enable HTTPS
   - Add rate limiting

2. **Database Migration**
   - Replace JSON with PostgreSQL/MySQL
   - Add proper indexing
   - Implement backup strategy

3. **Authentication Enhancement**
   - Add email verification
   - Implement password reset
   - Add two-factor authentication
   - Set session timeouts

4. **Input Validation**
   - Already implemented basic validation
   - Add CAPTCHA for registration
   - Implement rate limiting

---

## Performance Optimization

### Tips for Better Performance

1. **Caching**
   ```python
   @st.cache_data
   def load_college_data():
       # Expensive operations
       pass
   ```

2. **Lazy Loading**
   - Load data only when needed
   - Implement pagination for large datasets

3. **Session State Management**
   - Clear unused session variables
   - Implement session cleanup

---

## Monitoring and Logging

### View Application Logs

**Terminal Output:**
- Shows all Streamlit logs
- Displays user actions
- Shows errors and warnings

**Custom Logging:**
Add to `app.py`:
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("User logged in: " + username)
```

---

## Backup and Recovery

### Backup User Data

```bash
# Create backup
cp users.json users_backup_$(date +%Y%m%d).json

# Restore from backup
cp users_backup_20240201.json users.json
```

### Automated Backup (Linux/Mac)

Add to crontab:
```bash
0 0 * * * cp /path/to/users.json /path/to/backup/users_$(date +\%Y\%m\%d).json
```

---

## Getting Help

### Resources

1. **Documentation**
   - Read README.md for overview
   - Check OOP_PRINCIPLES.md for code understanding
   - Review QUICK_START.md for basic usage

2. **Code Comments**
   - All files have detailed comments
   - Docstrings explain each class/method

3. **Streamlit Documentation**
   - https://docs.streamlit.io

4. **Python OOP Resources**
   - https://docs.python.org/3/tutorial/classes.html

---

## Version Information

- **Application Version**: 1.0.0
- **Python Version**: 3.8+
- **Streamlit Version**: 1.31.0+
- **Last Updated**: February 2026

---

## Success Checklist

Before running the application, ensure:

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Project files in correct directory
- [ ] Port 8501 available (or using custom port)
- [ ] Browser available for UI
- [ ] Write permissions in project directory

---

## Quick Commands Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py

# Run on custom port
streamlit run app.py --server.port 8502

# Stop application
Ctrl + C

# Check Streamlit version
streamlit version

# Clear cache
streamlit cache clear
```

---

**🎉 You're all set! Run `streamlit run app.py` to start your career guidance journey!**

For questions or issues, refer to the troubleshooting section or check the detailed documentation in README.md.

Good luck with your career exploration! 🚀
