#!/bin/bash
set -e  # Exit immediately if any command fails

# Optional: Uncomment to clone repo if needed
# git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
# cd YOUR-REPO-NAME

echo "Creating Python virtual environment..."
python -m venv env

echo "Activating virtual environment..."
source env/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running portfolio tracker..."
python src/main.py --portfolio data/sample_portfolio.csv

echo "Done!"
echo "To change stocks or risk-free rate, edit:"
echo "  - data/sample_portfolio.csv"
echo "  - config/config.yaml"
