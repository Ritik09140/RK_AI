@echo off
title RK AI Server
echo.
echo  ██████╗ ██╗  ██╗     █████╗ ██╗
echo  ██╔══██╗██║ ██╔╝    ██╔══██╗██║
echo  ██████╔╝█████╔╝     ███████║██║
echo  ██╔══██╗██╔═██╗     ██╔══██║██║
echo  ██║  ██║██║  ██╗    ██║  ██║██║
echo  ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝
echo.
echo  Created by Ritik Boss
echo  Starting RK AI on http://127.0.0.1:8001
echo.

cd /d %~dp0

echo [1/2] Installing dependencies...
venv\Scripts\pip install fastapi uvicorn python-multipart --quiet

echo [2/2] Launching RK AI...
start "" "http://127.0.0.1:8001"
venv\Scripts\uvicorn main:app --reload --port 8001

pause
