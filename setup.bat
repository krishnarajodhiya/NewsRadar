@echo off
REM NewsVerify AI - Setup and Run Script for Windows

echo.
echo 🚀 NewsVerify AI - Setup Script
echo ================================
echo.

REM Check Python installation
echo ✓ Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python not found. Please install Python 3.8+
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Found Python %PYTHON_VERSION%
echo.

REM Create virtual environment
echo ✓ Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ⚠ Virtual environment already exists
)
echo.

REM Activate virtual environment
echo ✓ Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

REM Install dependencies
echo ✓ Installing dependencies...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ✗ Failed to install dependencies
    exit /b 1
)
echo ✓ Dependencies installed successfully
echo.

REM Train model
echo ✓ Training ML model...
cd backend
python train_model.py
if errorlevel 1 (
    echo ✗ Model training failed
    exit /b 1
)
echo ✓ Model training completed
cd ..
echo.

echo ================================
echo ✓ Setup Complete!
echo ================================
echo.
echo 📝 Next Steps:
echo.
echo 1. Start Flask Backend (in new terminal):
echo    cd backend ^&^& python app.py
echo.
echo 2. Open Frontend (in your browser):
echo    frontend/index.html
echo.
echo    Or serve with Python (in another terminal):
echo    cd frontend ^&^& python -m http.server 8000
echo    Then visit http://localhost:8000
echo.
echo 3. Backend will be available at: http://localhost:5000
echo.
echo Happy Fact-Checking! 🎉
echo.
pause
