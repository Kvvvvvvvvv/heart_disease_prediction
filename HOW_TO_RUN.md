# How to Run This Project

## ✅ EASIEST METHOD (Recommended)
Just run this command in PowerShell/Command Prompt:
```bash
python run_project.py
```
This will execute the entire notebook automatically and show you all the results!

---

## 📓 Method 2: Use Jupyter Notebook (Interactive)

### Option A: Try this command:
```bash
python -m notebook
```

### Option B: If that doesn't work, try:
```bash
python -m jupyterlab
```

### Option C: Use the batch file:
Double-click `start_jupyter.bat` or run:
```bash
start_jupyter.bat
```

**After starting Jupyter:**
1. Your browser should open automatically
2. If not, look for a URL in the terminal like: `http://localhost:8888/?token=...`
3. Copy that URL and paste it in your browser
4. Click on `UCI-heart-disease.ipynb` to open the notebook
5. Click "Run All" from the menu or press Shift+Enter to run cells one by one

---

## 🔧 Troubleshooting

**If you get "command not found" errors:**
- Make sure you're in the project directory
- Try: `python -m pip install --upgrade notebook jupyterlab`

**If the browser doesn't open:**
- Check the terminal output for the URL with token
- Copy the full URL including the token part
- Paste it in your browser

**If you just want to see results quickly:**
- Use Method 1 (`python run_project.py`) - it's the simplest!

---

## 📊 What the Project Does

This project:
- Loads heart disease data (303 patients)
- Performs exploratory data analysis
- Trains 3 machine learning models (KNN, Logistic Regression, Random Forest)
- Evaluates model performance
- Shows feature importance
- Achieves ~89% accuracy

---

## 💡 Quick Start

**Fastest way to run:**
```bash
python run_project.py
```

That's it! 🎉
