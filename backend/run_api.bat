@echo off
cd /d "%~dp0"
echo ===================================================
echo   PLACEMENT IQ — FastAPI Backend Server
echo ===================================================
python -m pip install -r requirements.txt
python -m uvicorn api:app --reload --host 127.0.0.1 --port 8000
