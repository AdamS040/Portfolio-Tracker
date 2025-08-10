# app.py
import streamlit as st
import pandas as pd
import yaml

from src.analysis import analyze_portfolio
from src.visualization import plot_cumulative_returns, plot_drawdown, plot_rolling_volatility


def main():
    st.title("Interactive Portfolio Tracker")

    # Load config for default values
    with open('config/config.yaml', 'r') as f:
        cfg = yaml.safe_load(f)

    risk_free_rate = st.number_input(
        "Risk-free rate (decimal)", value=cfg.get('risk_free_rate', 0.01), format="%.4f"
    )

    benchmark = st.text_input("Benchmark ticker", value=cfg.get('benchmark', 'SPY'))

    uploaded_file = st.file_uploader("Upload your portfolio CSV", type=["csv"])

    if uploaded_file is not None:
        pf = pd.read_csv(uploaded_file)

        if 'ticker' not in pf.columns or 'weight' not in pf.columns:
            st.error("Portfolio CSV must contain 'ticker' and 'weight' columns.")
            return

        if st.button("Run Analysis"):
            with st.spinner("Analyzing portfolio..."):
                sr, mdd, ab, cum_port, cum_bench, port_returns = analyze_portfolio(pf, risk_free_rate, benchmark)

            # Show metrics
            st.metric("Sharpe Ratio", f"{sr:.2f}")
            st.metric("Max Drawdown", f"{mdd:.2%}")
            st.metric("Alpha", f"{ab['alpha']:.2%}")
            st.metric("Beta", f"{ab['beta']:.2f}")

            # Show plots
            st.pyplot(plot_cumulative_returns(cum_port, cum_bench, return_fig=True))
            st.pyplot(plot_drawdown(cum_port, return_fig=True))
            st.pyplot(plot_rolling_volatility(port_returns, return_fig=True))


if __name__ == "__main__":
    main()
