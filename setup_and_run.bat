@echo off
setlocal enabledelayedexpansion

REM Navigate to repo folder if needed
cd /d %~dp0

echo Creating virtual environment (if not exists)...
if not exist env (
    python -m venv env
)

echo Activating virtual environment...
call env\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt

echo Running portfolio tracker (app.py)...
python src\app.py --portfolio data\sample_portfolio.csv

echo.
echo Done!
echo To change stocks or risk-free rate, edit:
echo   - data\sample_portfolio.csv
echo   - config\config.yaml
pause
