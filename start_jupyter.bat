@echo off
echo Starting Jupyter Notebook...
echo.
echo Trying method 1: python -m notebook
python -m notebook
if %errorlevel% neq 0 (
    echo.
    echo Method 1 failed. Trying method 2: python -m jupyterlab
    python -m jupyterlab
)
pause
