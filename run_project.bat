@echo off
title Blood Report Analysis System
cd /d "%~dp0"

echo ==========================================
echo   Blood Report Analysis System
echo ==========================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found. Install Python 3 and enable "Add Python to PATH".
    pause
    exit /b 1
)

python -m pip install -r requirements.txt
if errorlevel 1 (
    echo Dependency installation failed. Check your internet connection.
    pause
    exit /b 1
)

start "" http://127.0.0.1:5000
python app.py

pause
