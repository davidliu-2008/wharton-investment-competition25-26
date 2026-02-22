import numpy as np
import yfinance as yf

def estimate_mu_sigma_yfinance(
    ticker: str,
    start: str = "2022-01-01",
    end: str = None,
    trading_days: int = 252
):
    df = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)

    if df.empty:
        raise ValueError("No data returned. Check ticker or date range.")

    prices = df["Close"]

    # Log returns
    log_ret = np.log(prices / prices.shift(1)).dropna()

    # Daily estimates
    mu_daily = log_ret.mean()
    sigma_daily = log_ret.std(ddof=1)

    # Annualize
    mu_annual = mu_daily * trading_days
    sigma_annual = sigma_daily * np.sqrt(trading_days)

    return {
        "ticker": ticker,
        "start": start,
        "end": end,
        "mu_daily": float(mu_daily),
        "sigma_daily": float(sigma_daily),
        "mu_annual": float(mu_annual),
        "sigma_annual": float(sigma_annual),
        "n_returns": int(len(log_ret))
    }

# Example:
# stats = estimate_mu_sigma_yfinance("SPY", start="2020-01-01")
# print(stats)
