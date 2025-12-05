@echo off
REM Massive Attack Simulation - 20,000 attacks
REM High-performance large-scale testing

echo ============================================================
echo MASSIVE ATTACK SIMULATION - 20,000 ATTACKS
echo ============================================================
echo.
echo This will simulate 20,000 attacks against your honeypot
echo with 100 concurrent workers for maximum performance.
echo.
echo Make sure your logging server is running first!
echo.
pause

python run_massive_attack_simulation.py 20000 100 --force

pause

