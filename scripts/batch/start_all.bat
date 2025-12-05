@echo off
REM ========================================
REM   HoneyTrace - Multi-Layer Honeypot
REM   Complete System Startup Script
REM ========================================

cd /d "%~dp0\..\.."
set PROJECT_ROOT=%CD%

echo.
echo ========================================
echo   HoneyTrace - Multi-Layer Honeypot
echo   Starting All Services
echo ========================================
echo.
echo Project Root: %PROJECT_ROOT%
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo [INFO] Install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Starting Logging Server...
echo ----------------------------------------
start "HoneyTrace - Logging Server" cmd /k "cd /d %PROJECT_ROOT%\logging_server && python logging_server.py"
timeout /t 3 /nobreak >nul

echo.
echo [2/4] Starting Honeypot Services...
echo ----------------------------------------
start "HoneyTrace - Honeypot Services" cmd /k "cd /d %PROJECT_ROOT% && python scripts\start_all.py --no-frontend"
timeout /t 3 /nobreak >nul

echo.
echo [3/4] Checking Frontend...
echo ----------------------------------------
if exist "%PROJECT_ROOT%\db1\package.json" (
    echo [INFO] Frontend found, starting...
    start "HoneyTrace - Frontend Dashboard" cmd /k "cd /d %PROJECT_ROOT%\db1 && npm start"
    timeout /t 2 /nobreak >nul
) else (
    echo [WARN] Frontend not found, skipping...
)

echo.
echo ========================================
echo   All services are starting!
echo ========================================
echo.
echo Services:
echo   - Logging Server:    http://localhost:5000
echo   - Honeypot Services: http://localhost:8000-8002
echo   - Frontend Dashboard: http://localhost:3000
echo.
echo Each service is running in a separate window.
echo Close the windows or press Ctrl+C to stop services.
echo.
echo [INFO] To start everything in one window, run:
echo        python scripts\start_all.py
echo.
pause
