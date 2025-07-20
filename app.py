import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
from optimizer import optimize_portfolio
from utils import load_esg_data, calculate_carbon_footprint

st.set_page_config(page_title="🌱 Green Investment Portfolio Optimizer", layout="wide")
st.title("🌍 Green Investment Portfolio Optimizer")

# Input Tickers
tickers = st.text_input("Enter comma-separated tickers (e.g., AAPL,MSFT,TSLA):", "AAPL,MSFT,TSLA,XOM")
start_date = st.date_input("Start Date", datetime.date(2020, 1, 1))
end_date = st.date_input("End Date", datetime.date.today())

esg_data = load_esg_data("esg_data.csv")

if st.button("🔍 Optimize Portfolio"):
    tickers_list = [t.strip().upper() for t in tickers.split(",")]
    price_data = yf.download(tickers_list, start=start_date, end=end_date)['Adj Close']

    valid_tickers = [t for t in tickers_list if t in esg_data['Ticker'].values]
    price_data = price_data[valid_tickers]
    esg_filtered = esg_data[esg_data['Ticker'].isin(valid_tickers)]

    weights, portfolio_df = optimize_portfolio(price_data, esg_filtered)

    st.subheader("📈 Optimized Portfolio")
    st.dataframe(portfolio_df.style.format({"Weight": "{:.2%}"}))

    st.subheader("🧪 ESG & Carbon Metrics")
    carbon_score = calculate_carbon_footprint(portfolio_df)
    st.metric(label="Estimated Carbon Impact (lower is better)", value=f"{carbon_score:.2f} kg CO₂")

    st.download_button("📥 Download Portfolio CSV", portfolio_df.to_csv(index=False), file_name="optimized_portfolio.csv")