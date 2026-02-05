
@echo off
TITLE ABLETON RACK GENERATOR (CLEAN LAUNCH)

echo.
echo ==================================================
echo   1. PULIZIA PROCESSI VECCHI (KILL ZOMBIES)
echo ==================================================
echo Killing processes via PowerShell...
powershell -Command "Stop-Process -Name node,python,uvicorn -Force -ErrorAction SilentlyContinue"

echo.
echo ==================================================
echo   2. AVVIO BACKEND (PYTHON)
echo ==================================================
start "ABLETON BACKEND" cmd /c "cd backend && ..\.venv\Scripts\python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000 & pause"

echo Aspetto 5 secondi che il server parta...
timeout /t 5 /nobreak >nul

echo.
echo ==================================================
echo   3. AVVIO FRONTEND (NEXT.JS)
echo ==================================================
start "ABLETON FRONTEND" cmd /c "cd frontend && npm run dev & pause"

echo.
echo ==================================================
echo   TUTTO AVVIATO!
echo   Vai su: http://localhost:3000
echo ==================================================
pause
