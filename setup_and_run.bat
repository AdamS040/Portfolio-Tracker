@echo off
setlocal enabledelayedexpansion

REM Optional: clone repo if not done
REM git clone https://github.com/AdamS040/Portfolio-Tracker.git
REM cd Portfolio-Tracker

echo Creating virtual environment...
python -m venv env

echo Activating virtual environment...
call env\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Running portfolio tracker...
python src\main.py --portfolio data\sample_portfolio.csv

echo.
echo Done!
echo To change stocks or risk-free rate, edit:
echo   - data\sample_portfolio.csv
echo   - config\config.yaml
pause
