@echo off
cd /d "%~dp0backend"
echo ===================================================
echo   PLACEMENT IQ — FastAPI Backend Server (Port 8000)
echo ===================================================
python -m uvicorn api:app --reload --host 127.0.0.1 --port 8000
