@echo off
REM This batch file starts both backend and frontend for the AI Security Dashboard

echo.
echo ====================================================
echo   AI Security Dashboard - Day 1/10 War Challenge
echo ====================================================
echo.

REM Check if we're in the correct directory
if not exist "Day1-Backend" (
    echo Error: Day1-Backend folder not found!
    echo Please run this script from the 10-Day-War directory
    pause
    exit /b 1
)

if not exist "Day1-Frontend" (
    echo Error: Day1-Frontend folder not found!
    echo Please run this script from the 10-Day-War directory
    pause
    exit /b 1
)

echo Starting Backend (Flask API on port 5000)...
echo.
start "Backend - Flask API" cmd /k "cd Day1-Backend && venv\Scripts\activate && python app.py"

timeout /t 3

echo Starting Frontend (React on port 3000)...
echo.
cd Day1-Frontend
start "Frontend - React Dashboard" cmd /k "set NODE_PATH=C:\Program Files\nodejs && set PATH=C:\Program Files\nodejs;%PATH% && npm run dev"

echo.
echo ====================================================
echo   Both servers are starting...
echo ====================================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Documentation: Open README.md for more details
echo.
pause
