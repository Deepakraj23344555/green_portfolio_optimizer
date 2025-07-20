import pandas as pd

def load_esg_data(path):
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Ticker", "ESG_Score", "Carbon_Intensity"])

def calculate_carbon_footprint(portfolio_df):
    return (portfolio_df["Weight"] * portfolio_df["Carbon_Intensity"]).sum()