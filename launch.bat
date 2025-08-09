@echo off
echo Starting Secure File Encryption Tool...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if in correct directory
if not exist "src\main.py" (
    echo ERROR: Please run this script from the securityapplication directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

REM Install dependencies if needed
echo Installing/checking dependencies...
python -m pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Failed to install some dependencies
    echo You may need to run: pip install -r requirements.txt
    echo.
)

REM Launch the application
echo Launching application...
python src\main.py

REM If we get here, the application has closed
echo.
echo Application closed.
pause
