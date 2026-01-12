@echo off
echo ========================================
echo Heart Disease Prediction Web App
echo ========================================
echo.
echo Starting Streamlit web application...
echo.
echo IMPORTANT: Look below for the URL!
echo It will look like: http://localhost:8501/?token=...
echo.
echo Copy the ENTIRE URL (including ?token=...) and paste it in your browser
echo.
echo Press Ctrl+C to stop the server when done
echo.
echo ========================================
echo.
python -m streamlit run app.py
echo.
echo ========================================
echo Server stopped.
pause
