# 📊 Portfolio Tracker  

A Python + Streamlit dashboard for tracking **real** or **simulated** investment portfolios.  

This tool calculates key performance and risk metrics (e.g. **Sharpe Ratio**, **Drawdown**, **Alpha/Beta**) and visualizes results with an interactive web app. Market data is pulled from public APIs like **Yahoo Finance**.  

---

## 🚀 Features  

- 🔄 **Real-time market data** via `yfinance`  
- 📈 **Performance tracking**: daily returns, cumulative growth, rolling performance  
- 📉 **Risk analysis**: Sharpe Ratio, Max Drawdown, volatility  
- 📊 **Factor metrics**: Alpha, Beta vs. a benchmark index  
- 🖼️ **Interactive dashboards** powered by Streamlit & Plotly  
- ✅ Works with both **real portfolios** and **mock test portfolios**  
- ⚙️ Configurable **risk-free rate & benchmark** in `config/config.yaml`  
- 📁 Ready-to-use structure for projects, GitHub, and interviews  

---

## 🛠️ Prerequisites  

- Python **3.8+**  
- Git (optional, for cloning the repo)  

---

## 🏁 Getting Started  

### 1. **Clone the repo**  
```bash
git clone https://github.com/AdamS040/portfolio-tracker.git
cd portfolio-tracker
```

### 2. **Setup and Run**  
On **Windows**, double-click **setup_and_run.bat**  
On **macOS/Linux**, run:
   ```bash
   chmod +x setup_and_run.sh
   ./setup_and_run.sh
   ```
   This will create a virtual environment, install required packages, and launch the dashboard.  
  
### 3. **How to Use**  
The portfolio file is at data/sample_portfolio.csv. Edit this file to change the stocks or weights.
The config file is at config/config.yaml. Change the risk-free rate or benchmark ticker here.
You can run the tracker manually like this:
  ```bash
   python src/main.py --portfolio data/sample_portfolio.csv
```
### 4. **Project Structure**
  ```bash
config/
  config.yaml           # Risk-free rate and benchmark settings
data/
  sample_portfolio.csv  # Portfolio stocks and weights
src/
  app.py                # Streamlit dashboard entry point
  main.py               # CLI-based version (optional)
  data_fetcher.py       # Fetch price data
  portfolio.py          # Load & process portfolio
  metrics.py            # Calculate financial metrics
  visualization.py      # Plotting & chart functions
setup_and_run.bat       # Windows setup & run script
setup_and_run.sh        # macOS/Linux setup & run script
requirements.txt        # Python dependencies
README.md               # Project readme
```

Dependencies are listed in requirements.txt and installed automatically by the setup scripts

