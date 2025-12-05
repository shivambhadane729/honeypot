@echo off
REM ========================================
REM   HoneyTrace - Multi-Layer Honeypot
REM   Complete System Startup Script
REM   Starts all services in one command
REM ========================================

cd /d "%~dp0"
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

echo [INFO] Starting all services in separate windows...
echo.

REM Start Logging Server (Port 5000)
echo [1/5] Starting Logging Server (Port 5000)...
start "HoneyTrace - Logging Server" cmd /k "cd /d %PROJECT_ROOT%\logging_server && python logging_server.py"
timeout /t 3 /nobreak >nul

REM Start Fake Git Repository (Port 8001)
echo [2/5] Starting Fake Git Repository (Port 8001)...
start "HoneyTrace - Fake Git Repo" cmd /k "cd /d %PROJECT_ROOT% && python scripts\fake_git_repo.py"
timeout /t 2 /nobreak >nul

REM Start Fake CI/CD Runner (Port 8002)
echo [3/5] Starting Fake CI/CD Runner (Port 8002)...
start "HoneyTrace - Fake CI/CD Runner" cmd /k "cd /d %PROJECT_ROOT% && python scripts\fake_cicd_runner.py"
timeout /t 2 /nobreak >nul

REM Start Consolidated Honeypot (Port 8000)
echo [4/5] Starting Consolidated Honeypot (Port 8000)...
start "HoneyTrace - Consolidated Honeypot" cmd /k "cd /d %PROJECT_ROOT%\Honeypot && python honeypot_services.py"
timeout /t 2 /nobreak >nul

REM Check and start Frontend Dashboard (Port 3000)
echo [5/5] Starting Frontend Dashboard (Port 3000)...
if exist "%PROJECT_ROOT%\db1\package.json" (
    REM Check if Node.js is installed
    node --version >nul 2>&1
    if errorlevel 1 (
        echo [WARN] Node.js is not installed or not in PATH
        echo [INFO] Frontend will not start. Install Node.js from https://nodejs.org/
        echo [INFO] Skipping frontend startup...
    ) else (
        REM Check if node_modules exists
        if not exist "%PROJECT_ROOT%\db1\node_modules" (
            echo [INFO] node_modules not found. Installing dependencies...
            cd /d "%PROJECT_ROOT%\db1"
            call npm install
            if errorlevel 1 (
                echo [ERROR] Failed to install frontend dependencies
                echo [INFO] Skipping frontend startup...
            ) else (
                echo [OK] Dependencies installed successfully
                cd /d "%PROJECT_ROOT%"
                start "HoneyTrace - Frontend Dashboard" cmd /k "cd /d %PROJECT_ROOT%\db1 && npm start"
                timeout /t 3 /nobreak >nul
            )
        ) else (
            echo [OK] Frontend dependencies found, starting...
            start "HoneyTrace - Frontend Dashboard" cmd /k "cd /d %PROJECT_ROOT%\db1 && npm start"
            timeout /t 3 /nobreak >nul
        )
    )
) else (
    echo [WARN] Frontend not found at %PROJECT_ROOT%\db1
    echo [INFO] Skipping frontend startup...
)

echo.
echo ========================================
echo   All Services Started!
echo ========================================
echo.
echo Services Running:
echo   - Logging Server:        http://localhost:5000
echo   - Fake Git Repository:   http://localhost:8001
echo   - Fake CI/CD Runner:     http://localhost:8002
echo   - Consolidated Honeypot: http://localhost:8000
if exist "%PROJECT_ROOT%\db1\package.json" (
    node --version >nul 2>&1
    if not errorlevel 1 (
        echo   - Frontend Dashboard:    http://localhost:3000
    )
)
echo.
echo Each service is running in a separate window.
echo Close the windows or press Ctrl+C in each window to stop.
echo.
echo [INFO] To check service status, visit:
echo        http://localhost:5000/health
echo.
pause

