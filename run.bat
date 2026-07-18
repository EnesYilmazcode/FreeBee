@echo off
REM FreeBee one-click launcher -- starts the laptop relay (phone connects to it).
cd /d "%~dp0"
echo Starting FreeBee... a Chrome window will open when a bee is dispatched.
python agent\server.py
pause
