@echo off
REM Massive Attack Simulation - 10,000 attacks
REM Optimized for large-scale testing

echo ============================================================
echo MASSIVE ATTACK SIMULATION - 10,000 ATTACKS
echo ============================================================
echo.
echo This will simulate 10,000 attacks against your honeypot
echo with 50 concurrent workers for optimal performance.
echo.
echo Make sure your logging server is running first!
echo.
pause

python run_massive_attack_simulation.py 10000 50 --force

pause

