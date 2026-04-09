@echo off
chcp 65001 >nul
title RK AI - By Ritik Boss
cd /d R:\RK_AI

:START
echo.
echo  ====================================
echo   RK AI - Created by Ritik Boss
echo   http://127.0.0.1:8001
echo  ====================================
echo.

:: Kill anything on port 8001
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8001 2^>nul') do (
    taskkill /PID %%a /F >nul 2>&1
)

:: Open Chrome after 3 seconds
start /b cmd /c "ping 127.0.0.1 -n 4 >nul && start chrome http://127.0.0.1:8001"

:: Start server
echo Starting server...
venv\Scripts\uvicorn main:app --host 127.0.0.1 --port 8001

:: If server crashes, restart after 2 seconds
echo Server stopped. Restarting in 2 seconds...
timeout /t 2 >nul
goto START
