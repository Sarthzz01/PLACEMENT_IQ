@echo off
echo ===================================================
echo   PLACEMENT IQ — Starting Full-Stack Platform
echo ===================================================
start "Placement IQ — FastAPI Backend" cmd /k "cd /d %~dp0backend && python -m uvicorn api:app --reload --host 127.0.0.1 --port 8000"
start "Placement IQ — React Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"
echo.
echo FastAPI Backend running at:  http://127.0.0.1:8000
echo React Frontend running at:   http://localhost:5173
echo.
