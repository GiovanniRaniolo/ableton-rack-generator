
@echo off
TITLE CLEAN SHUTDOWN (FORCE KILL)
echo.
echo ==================================================
echo   SPEGNIMENTO FORZATO (PULIZIA TOTALE)
echo ==================================================

taskkill /F /IM node.exe /T 2>nul
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM uvicorn.exe /T 2>nul

echo.
echo Tutte le finestre nere dovrebbero essersi chiuse.
echo Il sistema e' ora spente e pulito.
pause
