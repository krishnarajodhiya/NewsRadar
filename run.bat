@echo off
REM NewsVerify AI - Quick Start Script for Windows

echo.
echo 🚀 Starting NewsVerify AI Application...
echo.

REM Check if venv exists
if not exist "venv" (
    echo ⚠️ Virtual environment not found. Running setup first...
    call setup.bat
    if errorlevel 1 (
        echo Setup failed. Please run setup.bat manually.
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat

echo ✓ Virtual environment activated
echo.
echo Starting Flask backend on http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

REM Start backend
cd backend
python app.py
