import os
from datetime import datetime

import pandas as pd
import streamlit as st
import yaml

from src.analysis import analyze_portfolio
from src.visualization import (
    plot_cumulative_returns,
    plot_drawdown,
    plot_rolling_volatility,
)


def export_pdf_report(metrics, figures, output_path="portfolio_report.pdf"):
    """
    Export portfolio analysis to a PDF with a title page and embedded plots.

    Args:
        metrics (dict): Dictionary with performance metrics (strings already formatted).
        figures (list): List of matplotlib Figure objects.
        output_path (str): Output PDF file name.
    """
    # Import here to keep app startup light if export isn't used
    from fpdf import FPDF

    class PDF(FPDF):
        def header(self):
            pass  # No header

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.set_text_color(128)
            self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    epw = pdf.w - 2 * pdf.l_margin  # effective page width

    # --- Title Page ---
    pdf.add_page()
    pdf.set_font("Arial", "B", 26)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 60, "", ln=True)  # Spacer
    pdf.cell(0, 15, "Portfolio Analysis Report", ln=True, align="C")
    pdf.set_font("Arial", "", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(
        0,
        10,
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ln=True,
        align="C",
    )

    # --- Metrics Page ---
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 15, "Key Metrics", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 14)
    col_width = epw / 2
    row_height = 10

    # Header
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(col_width, row_height, "Metric", border=1, align="C", fill=True)
    pdf.cell(col_width, row_height, "Value", border=1, align="C", fill=True)
    pdf.ln(row_height)

    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)
    for metric, value in metrics.items():
        pdf.cell(col_width, row_height, metric, border=1, align="L")
        pdf.cell(col_width, row_height, value, border=1, align="C")
        pdf.ln(row_height)

    # --- Figures ---
    for fig in figures:
        img_path = f"temp_fig_{datetime.now().strftime('%H%M%S%f')}.png"
        fig.savefig(img_path, bbox_inches="tight")
        try:
            pdf.add_page()
            pdf.image(img_path, x=10, y=20, w=pdf.w - 20)  # margins
        finally:
            try:
                os.remove(img_path)
            except OSError:
                pass

    pdf.output(output_path)


def _load_config(config_path: str = "config/config.yaml") -> dict:
    if not os.path.exists(config_path):
        st.error(f"Config file not found at '{config_path}'. Please create it before running.")
        st.stop()

    try:
        with open(config_path, "r") as f:
            return yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        st.error(f"Failed to parse YAML config: {e}")
        st.stop()


def _offer_sample_csv(sidebar, path="data/sample_portfolio.csv"):
    if os.path.exists(path):
        with open(path, "rb") as f:
            sidebar.download_button(
                label="Download sample portfolio CSV",
                data=f.read(),
                file_name=os.path.basename(path),
                mime="text/csv",
                key="download_sample_csv",
            )
    else:
        sidebar.warning("Sample CSV file not found.")


def main():
    st.title("📊 Interactive Portfolio Tracker")

    cfg = _load_config("config/config.yaml")

    risk_free_rate = st.sidebar.number_input(
        "Risk-free rate (annual decimal, e.g. 0.01 for 1%)",
        value=float(cfg.get("risk_free_rate", 0.01)),
        format="%.4f",
        step=0.0001,
    )
    benchmark = st.sidebar.text_input("Benchmark ticker", value=cfg.get("benchmark", "SPY"))

    st.sidebar.markdown("### Upload your portfolio CSV")
    st.sidebar.markdown("Expected columns: `ticker` and `weight`")
    uploaded_file = st.sidebar.file_uploader("Choose CSV file", type=["csv"])
    _offer_sample_csv(st.sidebar, "data/sample_portfolio.csv")

    if uploaded_file is None:
        st.info("Upload a portfolio CSV to begin.")
        st.stop()

    # Read & validate
    try:
        pf = pd.read_csv(uploaded_file)
    except pd.errors.EmptyDataError:
        st.error("The uploaded CSV file is empty or invalid. Please upload a valid portfolio CSV.")
        st.stop()
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        st.stop()

    if pf is None or pf.empty:
        st.error("Portfolio CSV not loaded or is empty. Please upload a valid file.")
        return

    if not {"ticker", "weight"}.issubset(pf.columns):
        st.error("CSV must contain at least 'ticker' and 'weight' columns.")
        return
    
    tickers_selected = st.multiselect(
        "Select tickers to analyze",
        options=pf["ticker"].tolist(),
        default=pf["ticker"].tolist(),
    )

    start_date = st.date_input("Start date", datetime(2023, 1, 1))
    end_date = st.date_input("End date", datetime.today())
    if start_date > end_date:
        st.error("Start date must be before end date.")
        st.stop()

    pf_filtered = pf[pf["ticker"].isin(tickers_selected)].reset_index(drop=True)

    if st.button("Run Analysis"):
        if pf_filtered.empty:
            st.error("Please select at least one ticker to analyze.")
            st.stop()
        with st.spinner("Analyzing portfolio..."):
            try:
                sr, mdd, ab, cum_port, cum_bench, port_returns = analyze_portfolio(
                    pf_filtered,
                    risk_free_rate,
                    benchmark,
                    start_date.strftime("%Y-%m-%d"),
                    end_date.strftime("%Y-%m-%d"),
                )
            except Exception as e:
                st.error(f"Error during analysis: {e}")
                st.stop()

        # Cache results for rendering & export
        st.session_state["analysis_results"] = {
            "sr": sr,
            "mdd": mdd,
            "ab": ab,
            "cum_port": cum_port,
            "cum_bench": cum_bench,
            "port_returns": port_returns,
        }

    # Render results if present
    if "analysis_results" in st.session_state:
        results = st.session_state["analysis_results"]
        sr = results["sr"]
        mdd = results["mdd"]
        ab = results["ab"]
        cum_port = results["cum_port"]
        cum_bench = results["cum_bench"]
        port_returns = results["port_returns"]

        st.markdown("### Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Sharpe Ratio", f"{sr:.2f}")
        col2.metric("Max Drawdown", f"{mdd:.2%}")
        col3.metric("Alpha", f"{ab['alpha']:.2%}")
        col4.metric("Beta", f"{ab['beta']:.2f}")

        st.markdown("### Portfolio vs Benchmark: Cumulative Returns")
        fig1 = plot_cumulative_returns(cum_port, cum_bench, return_fig=True)
        st.pyplot(fig1)

        st.markdown("### Drawdown Curve")
        fig2 = plot_drawdown(cum_port, return_fig=True)
        st.pyplot(fig2)

        st.markdown("### Rolling Volatility")
        fig3 = plot_rolling_volatility(port_returns, return_fig=True)
        st.pyplot(fig3)

        # Export
        if st.button("Export Report to PDF"):
            try:
                metrics = {
                    "Sharpe Ratio": f"{sr:.2f}",
                    "Max Drawdown": f"{mdd:.2%}",
                    "Alpha": f"{ab['alpha']:.2%}",
                    "Beta": f"{ab['beta']:.2f}",
                }
                export_pdf_report(metrics, [fig1, fig2, fig3], "portfolio_report.pdf")
                st.success("PDF report generated: portfolio_report.pdf")
                with open("portfolio_report.pdf", "rb") as f:
                    st.download_button(
                        label="📄 Download PDF Report",
                        data=f,
                        file_name="portfolio_report.pdf",
                        mime="application/pdf",
                    )
            except Exception as e:
                st.error(f"Error generating PDF report: {e}")


if __name__ == "__main__":
    main()
