import streamlit as st
import pandas as pd
import yaml
import os

from src.analysis import analyze_portfolio
from src.visualization import plot_cumulative_returns, plot_drawdown, plot_rolling_volatility

def main():
    st.title("📊 Interactive Portfolio Tracker")

    # Load config.yaml safely
    config_path = 'config/config.yaml'
    if not os.path.exists(config_path):
        st.error(f"Config file not found at '{config_path}'. Please create it before running.")
        st.stop()

    try:
        with open(config_path, 'r') as f:
            cfg = yaml.safe_load(f)
    except yaml.YAMLError as e:
        st.error(f"Failed to parse YAML config: {e}")
        st.stop()

    # Config inputs with defaults from config.yaml
    risk_free_rate = st.number_input(
        "Risk-free rate (annual decimal, e.g. 0.01 for 1%)",
        value=cfg.get('risk_free_rate', 0.01),
        format="%.4f",
        step=0.0001
    )

    benchmark = st.text_input("Benchmark ticker", value=cfg.get('benchmark', 'SPY'))

    st.markdown("### Upload your portfolio CSV")
    st.markdown("Expected columns: `ticker` and `weight`")
    uploaded_file = st.file_uploader("Choose CSV file", type=["csv"])

    # Sample portfolio download link
    st.markdown("[Download sample portfolio CSV](data/sample_portfolio.csv)")

    if uploaded_file is not None:
        try:
            pf = pd.read_csv(uploaded_file)
        except pd.errors.EmptyDataError:
            st.error("The uploaded CSV file is empty or invalid. Please upload a valid portfolio CSV.")
            st.stop()
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
            st.stop()

        # Validate columns
        if 'ticker' not in pf.columns or 'weight' not in pf.columns:
            st.error("Portfolio CSV must contain 'ticker' and 'weight' columns.")
            st.stop()

        if st.button("Run Analysis"):
            with st.spinner("Analyzing portfolio..."):
                try:
                    sr, mdd, ab, cum_port, cum_bench, port_returns = analyze_portfolio(
                        pf, risk_free_rate, benchmark
                    )
                except Exception as e:
                    st.error(f"Error during analysis: {e}")
                    st.stop()

            # Show metrics
            st.markdown("### Key Metrics")
            st.metric("Sharpe Ratio", f"{sr:.2f}")
            st.metric("Max Drawdown", f"{mdd:.2%}")
            st.metric("Alpha", f"{ab['alpha']:.2%}")
            st.metric("Beta", f"{ab['beta']:.2f}")

            # Show plots
            st.markdown("### Portfolio vs Benchmark: Cumulative Returns")
            fig = plot_cumulative_returns(cum_port, cum_bench, return_fig=True)
            st.pyplot(fig)

            st.markdown("### Drawdown Curve")
            fig = plot_drawdown(cum_port, return_fig=True)
            st.pyplot(fig)

            st.markdown("### Rolling Volatility")
            fig = plot_rolling_volatility(port_returns, return_fig=True)
            st.pyplot(fig)

if __name__ == "__main__":
    main()
