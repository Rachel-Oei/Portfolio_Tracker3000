
import yfinance as yf
import numpy as np

def run_monte_carlo(ticker, num_simulations=100000, years=15, batch_size=25000):
    days = 252 * years
    data = yf.download(ticker, period='1y', auto_adjust=True)['Close']
    returns = data.pct_change().dropna()
    mu = returns.mean().item()
    sigma = returns.std().item()
    S0 = data.iloc[-1].item()

    print(f"Using mu={mu:.6f}, sigma={sigma:.6f}, S0={S0:.2f}")

    batches = num_simulations // batch_size
    all_final_prices = []

    for batch_num in range(batches):
        Z = np.random.normal(0, 1, size=(days, batch_size)).astype(np.float32)
        drift = (mu - 0.5 * sigma ** 2)
        daily_returns = np.exp(drift + sigma * Z).astype(np.float32)
        initial_prices = np.full(batch_size, S0, dtype=np.float32)
        price_paths = np.vstack([initial_prices, daily_returns]).cumprod(axis=0)
        all_final_prices.append(price_paths[-1])

    all_final_prices = np.concatenate(all_final_prices)

    summary = {
        'mean_final_price': all_final_prices.mean(),
        'median_final_price': np.median(all_final_prices),
        '5th_percentile': np.percentile(all_final_prices, 5),
        '95th_percentile': np.percentile(all_final_prices, 95),
    }

    return summary