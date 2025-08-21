#!/bin/bash
set -e

# Navigate to repo folder
cd "$(dirname "$0")"

echo "Creating virtual environment (if not exists)..."
if [ ! -d "env" ]; then
    python3 -m venv env
fi

echo "Activating virtual environment..."
source env/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip >/dev/null 2>&1
pip install -r requirements.txt

echo "Running portfolio tracker (app.py)..."
python -m streamlit run src/app.py

echo
echo "Done!"
echo "To change stocks or risk-free rate, edit:"
echo "  - data/sample_portfolio.csv"
echo "  - config/config.yaml"
