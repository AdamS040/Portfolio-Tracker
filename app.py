import streamlit as st
import pandas as pd
import yaml
import os
from datetime import datetime
from fpdf import FPDF

from src.analysis import analyze_portfolio
from src.visualization import (
    plot_cumulative_returns,
    plot_drawdown,
    plot_rolling_volatility
)

def export_pdf_report(metrics, figures, output_path="portfolio_report.pdf"):
    """
    Exports portfolio analysis to a PDF with a title page and embedded plots.

    Args:
        metrics (dict): Dictionary with performance metrics.
        figures (list): List of matplotlib Figure objects.
        output_path (str): Output PDF file name.
    """
    class PDF(FPDF):
        def header(self):
            pass  # No header on all pages

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128)
            self.cell(0, 10, f"Page {self.page_no()}", 0, 0, 'C')

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Calculate effective page width
    epw = pdf.w - 2 * pdf.l_margin

    # --- Title Page ---
    pdf.add_page()
    pdf.set_font("Arial", 'B', 26)
    pdf.set_text_color(0, 51, 102)  # Dark blue
    pdf.cell(0, 60, "", ln=True)  # Spacer
    pdf.cell(0, 15, "Portfolio Analysis Report", ln=True, align='C')
    pdf.set_font("Arial", '', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
             ln=True, align='C')

    # --- Metrics Page ---
    pdf.add_page()
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 15, "Key Metrics", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 14)
    col_width = epw / 2  # divide page width into two columns
    row_height = 10

    # Table header
    pdf.set_fill_color(200, 220, 255)  # Light blue fill
    pdf.cell(col_width, row_height, "Metric", border=1, align='C', fill=True)
    pdf.cell(col_width, row_height, "Value", border=1, align='C', fill=True)
    pdf.ln(row_height)

    pdf.set_font("Arial", '', 12)
    pdf.set_text_color(0, 0, 0)
    for metric, value in metrics.items():
        pdf.cell(col_width, row_height, metric, border=1, align='L')
        pdf.cell(col_width, row_height, value, border=1, align='C')
        pdf.ln(row_height)

    # --- Figures ---
    for fig in figures:
        # Save figure temporarily
        img_path = f"temp_fig_{datetime.now().strftime('%H%M%S%f')}.png"
        fig.savefig(img_path, bbox_inches='tight')
        pdf.add_page()
        pdf.image(img_path, x=10, y=20, w=pdf.w - 20)  # leave margin 10 each side
        os.remove(img_path)

    pdf.output(output_path)

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

            metrics = {
                "Sharpe Ratio": f"{sr:.2f}",
                "Max Drawdown": f"{mdd:.2%}",
                "Alpha": f"{ab['alpha']:.2%}",
                "Beta": f"{ab['beta']:.2f}"
            }

            # Show plots & store figures
            figs = []

            st.markdown("### Portfolio vs Benchmark: Cumulative Returns")
            fig1 = plot_cumulative_returns(cum_port, cum_bench, return_fig=True)
            st.pyplot(fig1)
            figs.append(fig1)

            st.markdown("### Drawdown Curve")
            fig2 = plot_drawdown(cum_port, return_fig=True)
            st.pyplot(fig2)
            figs.append(fig2)

            st.markdown("### Rolling Volatility")
            fig3 = plot_rolling_volatility(port_returns, return_fig=True)
            st.pyplot(fig3)
            figs.append(fig3)

            # Save results in session state
            st.session_state['metrics'] = metrics
            st.session_state['figs'] = figs

    # Show export button only if analysis has run
    if 'metrics' in st.session_state and 'figs' in st.session_state:
        if st.button("Export Report to PDF"):
            try:
                output_file = "portfolio_report.pdf"
                st.write("Generating PDF report...")  # Debug message
                export_pdf_report(st.session_state['metrics'], st.session_state['figs'], output_file)
                st.write(f"Report saved at {output_file}")
                with open(output_file, "rb") as f:
                    st.download_button(
                        label="📄 Download PDF Report",
                        data=f,
                        file_name=output_file,
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"Error generating PDF report: {e}")

if __name__ == "__main__":
    main()
