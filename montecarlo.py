import yfinance as yf
import numpy as np
import pandas as pd

# User inputs
stock = input('Enter stock ticker: ').upper()
num_simulations = 100_000  # total simulations you want
days = 252 * 15  # 15 years of trading days

# Download 1 year of historical data for mu and sigma calculation
data = yf.download(stock, period='1y', auto_adjust=True)['Close']
returns = data.pct_change().dropna()
mu = returns.mean().item()
sigma = returns.std().item()
S0 = data.iloc[-1].item()

print(f"Using mu={mu:.6f}, sigma={sigma:.6f}, S0={S0:.2f}")

# Set batch size (e.g., 25k simulations per batch)
batch_size = 25_000
batches = num_simulations // batch_size

all_final_prices = []

for batch_num in range(batches):
    # Generate random normal shocks for this batch
    Z = np.random.normal(0, 1, size=(days, batch_size)).astype(np.float32)

    drift = (mu - 0.5 * sigma**2)
    daily_returns = np.exp(drift + sigma * Z).astype(np.float32)

    # Starting prices array
    initial_prices = np.full(batch_size, S0, dtype=np.float32)

    # Calculate price paths
    price_paths = np.vstack([initial_prices, daily_returns]).cumprod(axis=0)

    # Store final prices from this batch
    all_final_prices.append(price_paths[-1])

# Combine all batches
all_final_prices = np.concatenate(all_final_prices)

# Output statistics
print(f"Mean final price after {days} days: ${all_final_prices.mean():.2f}")
print(f"Median final price after {days} days: ${np.median(all_final_prices):.2f}")

summary = {
    'mean_final_price': all_final_prices.mean(),
    'median_final_price': np.median(all_final_prices),
    '5th_percentile': np.percentile(all_final_prices, 5),
    '95th_percentile': np.percentile(all_final_prices, 95),
}
print(summary)
