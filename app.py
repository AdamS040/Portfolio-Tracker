import streamlit as st

st.title("Portfolio Tracker")

uploaded_file = st.file_uploader("Upload your portfolio CSV", type=["csv"])

if uploaded_file is not None:
    import pandas as pd
    pf = pd.read_csv(uploaded_file)
    st.write("Portfolio Preview:")
    st.dataframe(pf.head())

