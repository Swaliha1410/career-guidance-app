# 🔧 Installation Troubleshooting Guide

## Quick Fix for "Module Not Found" Error

### Step 1: Install Dependencies

Try each method below until one works:

#### Method 1: Standard Installation (Try First)
```bash
pip install streamlit plotly
```

#### Method 2: Using pip3
```bash
pip3 install streamlit plotly
```

#### Method 3: Using Python -m pip
```bash
python -m pip install streamlit plotly
```

#### Method 4: Using Python3 -m pip
```bash
python3 -m pip install streamlit plotly
```

#### Method 5: User Installation (If permission errors)
```bash
pip install --user streamlit plotly
```

#### Method 6: Upgrade pip first
```bash
python -m pip install --upgrade pip
pip install streamlit plotly
```

### Step 2: Verify Installation

After installing, verify with:
```bash
python -c "import streamlit; import plotly; print('✅ Success! All modules installed.')"
```

### Step 3: Run the Application

```bash
streamlit run app.py
```

---

## Common Error Solutions

### Error 1: "streamlit: command not found"

**Solution A:**
```bash
python -m streamlit run app.py
```

**Solution B:**
```bash
python3 -m streamlit run app.py
```

### Error 2: "No module named 'streamlit'"

**Solution:**
```bash
# Uninstall and reinstall
pip uninstall streamlit -y
pip install streamlit

# Then try again
streamlit run app.py
```

### Error 3: "No module named 'plotly'"

**Solution:**
```bash
pip install plotly
```

### Error 4: Permission Denied

**Solution (Windows - Run as Administrator):**
```bash
pip install --user streamlit plotly
```

**Solution (Mac/Linux):**
```bash
pip3 install --user streamlit plotly
```

### Error 5: Multiple Python Versions

**Check which Python you're using:**
```bash
which python
which python3
```

**Use the specific Python version:**
```bash
# If using Python 3.10
python3.10 -m pip install streamlit plotly
python3.10 -m streamlit run app.py
```

---

## Complete Installation Script

### For Windows (PowerShell):
```powershell
# Navigate to project folder
cd career_guidance_app

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
python -m pip install streamlit plotly

# Run application
python -m streamlit run app.py
```

### For Mac/Linux (Terminal):
```bash
# Navigate to project folder
cd career_guidance_app

# Upgrade pip
python3 -m pip install --upgrade pip

# Install dependencies
python3 -m pip install streamlit plotly

# Run application
python3 -m streamlit run app.py
```

---

## Virtual Environment Method (Recommended for Clean Install)

### Step-by-Step:

#### 1. Create Virtual Environment
```bash
# Windows
python -m venv venv

# Mac/Linux
python3 -m venv venv
```

#### 2. Activate Virtual Environment
```bash
# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Mac/Linux
source venv/bin/activate
```

#### 3. Install Packages
```bash
pip install streamlit plotly
```

#### 4. Run Application
```bash
streamlit run app.py
```

#### 5. Deactivate (When Done)
```bash
deactivate
```

---

## Still Having Issues?

### Check Python Version
```bash
python --version
```
**Required:** Python 3.8 or higher

If you have older Python, download from: https://www.python.org/downloads/

### Check if Modules are Installed
```bash
pip list | grep streamlit
pip list | grep plotly
```

### Reinstall Everything
```bash
pip uninstall streamlit plotly -y
pip install --upgrade pip
pip install streamlit plotly
```

---

## Alternative: Use Anaconda

If nothing works, try Anaconda:

```bash
# Install Anaconda from: https://www.anaconda.com/download

# Create environment
conda create -n career_app python=3.10

# Activate
conda activate career_app

# Install packages
conda install -c conda-forge streamlit plotly

# Run
streamlit run app.py
```

---

## Test Installation

Create a test file `test_install.py`:
```python
import streamlit as st
import plotly.graph_objects as go

st.title("✅ Installation Successful!")
st.success("All modules are working correctly.")

fig = go.Figure(data=[go.Bar(x=[1, 2, 3], y=[4, 5, 6])])
st.plotly_chart(fig)
```

Run it:
```bash
streamlit run test_install.py
```

If this works, your installation is correct!

---

## Quick Install Command (Copy-Paste)

**Windows:**
```bash
python -m pip install --upgrade pip && python -m pip install streamlit plotly && python -m streamlit run app.py
```

**Mac/Linux:**
```bash
python3 -m pip install --upgrade pip && python3 -m pip install streamlit plotly && python3 -m streamlit run app.py
```

---

## Get Help

If you see a specific error message, copy the exact error and:

1. Check which line mentions "ModuleNotFoundError"
2. Note the module name (streamlit or plotly)
3. Install that specific module
4. Try running again

**Example Error:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution:**
```bash
pip install streamlit
```

---

## Success Checklist

- [ ] Python 3.8+ installed
- [ ] pip working (`pip --version`)
- [ ] streamlit installed (`pip show streamlit`)
- [ ] plotly installed (`pip show plotly`)
- [ ] Can import modules (run test script)
- [ ] Streamlit command works

---

## Contact Support

If all methods fail, please share:
1. Your operating system (Windows/Mac/Linux)
2. Python version (`python --version`)
3. The exact error message
4. What you've tried so far

---

**Most Common Solution:**
```bash
python -m pip install streamlit plotly
python -m streamlit run app.py
```

This works 95% of the time! 🎉
