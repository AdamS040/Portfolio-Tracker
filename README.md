# 📊 Portfolio Tracker

A Python-based dashboard for tracking **real** or **simulated** investment portfolios.

This tool calculates key performance and risk metrics (like **Sharpe Ratio**, **Drawdown**, **Alpha/Beta**) and visualizes the results using data pulled from public APIs like **Yahoo Finance**.

---

## 🚀 Features

- 🔄 **Real-time market data** using `yfinance`  
- 📈 **Performance tracking** (daily returns, cumulative growth)  
- 📉 **Risk analysis** (Sharpe Ratio, Max Drawdown)  
- 📊 **Factor metrics** (Alpha, Beta vs. benchmark)  
- 🖼️ **Visual dashboards** with Matplotlib and Plotly  
- ✅ Supports both **real** and **mock** portfolios  
- 📁 Exportable structure for GitHub and interviews  

---

## 🛠️ Prerequisites

- Python 3.8 or higher installed  
- Git installed (optional, for cloning the repo)  

---

## 🏁 Getting Started


### 1. **Clone repo**  
   ```bash
   git clone https://github.com/AdamS040/portfolio-tracker.git
   cd portfolio-tracker
   ```

### 2. **Setup and Run**  
On **Windows**, double-click setup_and_run.bat  
On **macOS/Linux**, run:
   ```bash
   chmod +x setup_and_run.sh
   ./setup_and_run.sh
   ```
   This will create a virtual environment, install required packages, and run the tracker.  
  
### 3. **How to Use**  
The portfolio file is at data/sample_portfolio.csv. Edit this file to change the stocks or weights.
The config file is at config/config.yaml. Change the risk-free rate or benchmark ticker here.
You can run the tracker manually like this:
  ```bash
   python src/main.py --portfolio data/sample_portfolio.csv
```
### 4. Running the Streamlit App
Install Streamlit:
```bash
pip install streamlit
```  

Run App:
```bash
streamlit run app.py
```
### 5. **Project Structure**
  ```bash
   config/
  config.yaml           # Risk-free rate and benchmark settings
data/
  sample_portfolio.csv  # Portfolio stocks and weights
src/
  main.py               # Main program
  data_fetcher.py       # Fetch price data
  portfolio.py          # Load and process portfolio
  metrics.py            # Calculate financial metrics
  visualization.py      # Plotting functions
  app.py                #Streamlit adaptation
setup_and_run.bat       # Windows setup & run script
setup_and_run.sh        # macOS/Linux setup & run script
requirements.txt        # Python dependencies
README.md               # This file
```

Dependencies are listed in requirements.txt and installed automatically by the setup scripts

