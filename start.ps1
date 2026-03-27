http://localhost:3000# AI Security Dashboard - Startup Script for PowerShell

Write-Host "====================================================`r`n" -ForegroundColor Cyan
Write-Host "   AI Security Dashboard - Day 1/10 War Challenge`r`n" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""

# Verify directories exist
if (-not (Test-Path "Day1-Backend")) {
    Write-Host "Error: Day1-Backend folder not found!" -ForegroundColor Red
    Write-Host "Please run this script from the 10-Day-War directory"
    Read-Host "Press Enter to exit"
    exit
}

if (-not (Test-Path "Day1-Frontend")) {
    Write-Host "Error: Day1-Frontend folder not found!" -ForegroundColor Red
    Write-Host "Please run this script from the 10-Day-War directory"
    Read-Host "Press Enter to exit"
    exit
}

# Set up Node.js environment
$env:NODE_PATH = "C:\Program Files\nodejs"
$env:PATH = "C:\Program Files\nodejs;" + $env:PATH

Write-Host "Starting Backend (Flask API on port 5000)..." -ForegroundColor Green
Write-Host "Starting Frontend (React on port 3000)..." -ForegroundColor Green
Write-Host ""

# Start Backend in new PowerShell window
Start-Process powershell -ArgumentList "-NoExit -Command `"cd '$PWD\Day1-Backend'; .\venv\Scripts\Activate.ps1; python app.py`"" -WindowStyle Normal

# Wait a bit before starting frontend
Start-Sleep -Seconds 3

# Start Frontend in new PowerShell window
Start-Process powershell -ArgumentList "-NoExit -Command `"cd '$PWD\Day1-Frontend'; npm run dev`"" -WindowStyle Normal

Write-Host "====================================================`r`n" -ForegroundColor Cyan
Write-Host "   Both servers are starting in separate windows..." -ForegroundColor Yellow
Write-Host "`r`n====================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend:  http://localhost:5000" -ForegroundColor Green
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Green
Write-Host ""
Write-Host "Documentation: Open README.md for more details" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to close this window (servers will continue running)"
