import yfinance as yf
from view import print_asset_table, print_weight_table
import numpy as np
import pandas as pd
from colorama import Fore, Style, init
import matplotlib.pyplot as plt

class Asset:
    def __init__(self, ticker, quantity, purchase_price):
        self.ticker = ticker
        self.quantity = quantity
        self.purchase_price = purchase_price
        self.close = None
        self.market_cap = None
        self.daily_return = None
        info = yf.Ticker(ticker).info
        self.name = info.get("longName", info.get("shortName", "UNKNOWN"))
        self.sector = info.get("sector", self.name) # if sector is unknown, use long/ short name of ticker
        self.asset_class = info.get("quoteType", "UNKNOWN")
        self.market_cap = info.get("marketCap", None)

    def update_close(self):
        data = yf.Ticker(self.ticker)
        hist = data.history(period="max")  
        close_series = hist['Close']    
        if len(close_series) >= 2:
            self.daily_return = np.log(close_series.iloc[-1] / close_series.iloc[-2]) * 100 #use log returns 
        else:
            self.daily_return = 0.0
        self.close = close_series.iloc[-1] 

    def transaction_value(self):
        return self.quantity * self.purchase_price

    def current_value(self):
        if self.close is None:
            return None
        return self.quantity * self.close

class Portfolio:
    def __init__(self):
        self.assets = []

    def add_asset(self, asset):
        self.assets.append(asset)

    def update_all_closes(self):
        for asset in self.assets:
            asset.update_close()

    def total_cost(self):
        return sum(asset.transaction_value() for asset in self.assets)

    def total_value(self):
       return sum(asset.current_value() or 0 for asset in self.assets)

    def weights(self):
        total = self.total_value()
        return {asset.ticker: (asset.current_value() or 0) / total for asset in self.assets if total > 0}

    def weights_by_asset_class(self):
        total = self.total_value()
        weights = {}
        if total == 0:
            return weights
        class_sums = {}
        for asset in self.assets:
            class_sums[asset.asset_class] = class_sums.get(asset.asset_class, 0) + (asset.current_value() or 0)
        for asset_class, value_sum in class_sums.items():
            weights[asset_class] = value_sum / total
        return weights

    def weights_by_sector(self):
        total = self.total_value()
        weights = {}
        if total == 0:
            return weights
        sector_sums = {}
        for asset in self.assets:
            sector_sums[asset.sector] = sector_sums.get(asset.sector, 0) + (asset.current_value() or 0)
        for sector, value_sum in sector_sums.items():
            weights[sector] = value_sum / total
        return weights

    def add_assets(self):
        ticker = input("Enter the ticker: ").upper()

        if any(existing_asset.ticker.upper() == ticker for existing_asset in self.assets):
            print(Fore.RED + f"\nAsset '{ticker}' is already in the portfolio. Duplicate not added." + Style.RESET_ALL)
            return

        quantity = int(input("Enter the quantity: "))
        purchase_price = float(input("Enter the purchase price (USD): "))
        asset = Asset(ticker, quantity, purchase_price)
        asset.update_close()
        self.add_asset(asset)
        print_asset_table(self)

    def print_total_cost_and_value(self):
        print("\nCalculation for Transaction Value (Quantity * Purchase Price):")
        total_cost = 0
        for asset in self.assets:
            cost = asset.transaction_value()
            total_cost += cost
            print(f"{asset.ticker}: {asset.quantity} * ${asset.purchase_price:.2f} = ${cost:.2f}")
        print(f"\033[1mTotal Cost = $\033[0m{total_cost:.2f}")

        print("\nCalculation for Total Value (Quantity * Current Price):")
        total_value = 0
        for asset in self.assets:
            current_val = asset.current_value()
            if current_val is None:
                print(f"{asset.ticker}: current price unknown, skipping")
                current_val = 0
            else:
                print(f"{asset.ticker}: {asset.quantity} * ${asset.close:.2f} = ${current_val:.2f}")
            total_value += current_val
        print(f"\033[1mTotal Value = $\033[0m{total_value:.2f}")

    def summary(self):
        for asset in self.assets:
            weight = self.weights().get(asset.ticker, 0)
            market_cap = asset.market_cap if asset.market_cap is not None else 0
            daily_return = f"{asset.daily_return:.2f}%" if asset.daily_return is not None else "N/A"

        print("\n" + "="*150)
        print("\033[1mPortfolio Summary:\033[0m")
        print_asset_table(self)
        print_weight_table("\n\033[1mWeights by Asset:\033[0m", self.weights())
        print_weight_table("\n\033[1mWeights by Asset Class:\033[0m", self.weights_by_asset_class())
        print_weight_table("\n\033[1mWeights by Sector:\033[0m", self.weights_by_sector())

        self.print_total_cost_and_value()
        print("="*150 + "\n")
        print(Fore.GREEN + Style.BRIGHT + "Portfolio Summary successfully created! Scroll up to view." + Style.RESET_ALL)

    def monte_carlo(self, total_simulations=100_000, batch_size=10_000):
        if not self.assets:
            print("Portfolio is empty, cannot run simulation.")
            return

        tickers = [asset.ticker for asset in self.assets]
        weights_dict = self.weights()
        weights_array = np.array([weights_dict[ticker] for ticker in tickers])

        data = yf.download(tickers, period="20y", auto_adjust=True)['Close'].dropna()
        if data.empty:
            print("No historical data retrieved.")
            return

        log_returns = np.log(data / data.shift(1)).dropna()
        mu = log_returns.mean().values          # Mean daily log return
        cov = log_returns.cov().values          # Covariance matrix

        num_days = 252 * 15  # 15 years of trading days
        num_batches = total_simulations // batch_size
        cumulative_returns = []

        print(f"Running {total_simulations} simulations in {num_batches} batches...")

        for i in range(num_batches):
            simulated_returns = np.random.multivariate_normal(mu, cov, size=(batch_size, num_days))
            portfolio_daily_returns = simulated_returns @ weights_array
            cumulative_log_returns = np.sum(portfolio_daily_returns, axis=1)
            batch_returns = np.exp(cumulative_log_returns) - 1 #compounding because of log
            cumulative_returns.extend(batch_returns)

            print(f"Batch {i+1}/{num_batches} completed.")

        cumulative_returns = np.array(cumulative_returns)

        mean_return = np.mean(cumulative_returns)
        std_dev = np.std(cumulative_returns)
        var_5 = np.percentile(cumulative_returns, 5)
        var_95 = np.percentile(cumulative_returns, 95)

        print(f"\nMean simulated 15-year cumulative return: {mean_return:.2%}")
        print(f"Std deviation: {std_dev:.2%}")
        print(f"5% percentile (VaR): {var_5:.2%}")
        print(f"95% percentile (VaR): {var_95:.2%}")