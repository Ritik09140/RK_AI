@echo off
title RK AI Server
cd /d R:\RK_AI
echo Installing dependencies...
venv\Scripts\pip install fastapi uvicorn g4f --quiet
echo.
echo Starting RK AI on http://127.0.0.1:8000
echo.
start "" "http://127.0.0.1:8000"
venv\Scripts\uvicorn rk_ai.backend:app --host 127.0.0.1 --port 8001 --reload
pause
