from pypfopt import EfficientFrontier, risk_models, expected_returns
import pandas as pd

def optimize_portfolio(price_data, esg_data):
    mu = expected_returns.mean_historical_return(price_data)
    S = risk_models.sample_cov(price_data)

    ef = EfficientFrontier(mu, S)
    raw_weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()

    portfolio_df = pd.DataFrame.from_dict(cleaned_weights, orient='index', columns=['Weight'])
    portfolio_df.index.name = 'Ticker'
    portfolio_df.reset_index(inplace=True)

    portfolio_df = pd.merge(portfolio_df, esg_data, on='Ticker')

    return cleaned_weights, portfolio_df