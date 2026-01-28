@echo off
echo ===============================================
echo BSOD Analyzer Parser Tool - Launcher
echo ===============================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or later from python.org
    pause
    exit /b 1
)

REM Run the GUI application
echo Starting BSOD Analyzer Parser Tool...
python gui_app.py

pause
