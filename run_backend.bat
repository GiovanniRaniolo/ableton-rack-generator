@echo off
TITLE ABLETON RACK BACKEND
echo STARTING BACKEND...
cd backend
..\.venv\Scripts\python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
pause
