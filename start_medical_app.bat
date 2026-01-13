@echo off
echo 🏥 Starting Medical Dashboard Application...
echo ================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python and try again.
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "heart_disease_model.pkl" (
    echo Warning: heart_disease_model.pkl not found!
    echo Please ensure the model file is in the project root directory.
)

if not exist "feature_names.json" (
    echo Warning: feature_names.json not found!
    echo Please ensure the feature names file is in the project root directory.
)

REM Install dependencies if requirements.txt exists
if exist "requirements.txt" (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Run the application
echo Starting the medical dashboard application...
python run_medical_app.py

pause