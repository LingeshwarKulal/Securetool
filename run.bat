@echo off
REM Secure File Encryption Tool Launcher
REM This script launches the application on Windows

echo Starting Secure File Encryption Tool...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    echo.
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "src\main.py" (
    echo Error: Cannot find main.py
    echo Please run this script from the project root directory
    echo.
    pause
    exit /b 1
)

REM Check if requirements are installed
python -c "import cryptography" >nul 2>&1
if errorlevel 1 (
    echo Installing required dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        echo Please run: python -m pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)

REM Launch the application
echo Launching application...
python src\main.py

if errorlevel 1 (
    echo.
    echo Application exited with an error
    pause
)
