import yfinance as yf
from view import print_asset_table, print_weight_table
import numpy as np
import pandas as pd

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
        self.asset_class = info.get("quoteType", "UNKNOWN")
        self.sector = info.get("sector", self.name) # if sector is unknown, use long/ short name of ticker
        self.market_cap = info.get("marketCap", None)

    def update_close(self):
        data = yf.Ticker(self.ticker)
        hist = data.history(period="max")  
        close_series = hist['Close']    
        if len(close_series) >= 2:
            self.daily_return = (close_series.iloc[-1] - close_series.iloc[-2]) / close_series.iloc[-2] * 100
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
        quantity = int(input("Enter the quantity: "))
        purchase_price = float(input("Enter the purchase price (USD): "))
        asset = Asset(ticker, quantity, purchase_price)
        asset.update_close()
        self.add_asset(asset)
        print_asset_table(self)

    def print_total_cost_and_value(self):
        print("\nCalculation for Total Cost (Quantity * Purchase Price):")
        total_cost = 0
        for asset in self.assets:
            cost = asset.transaction_value()
            total_cost += cost
            print(f"{asset.ticker}: {asset.quantity} * ${asset.purchase_price:.2f} = ${cost:.2f}")
        print(f"Total Cost = ${total_cost:.2f}")

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
        print(f"Total Value = ${total_value:.2f}")

    def summary(self):
        print("Portfolio Summary:")
        for asset in self.assets:
            weight = self.weights().get(asset.ticker, 0)
            market_cap = asset.market_cap if asset.market_cap is not None else 0
            daily_return = f"{asset.daily_return:.2f}%" if asset.daily_return is not None else "N/A"

        print_asset_table(self)
        print_weight_table("Weights by Asset", self.weights())
        print_weight_table("Weights by Asset Class", self.weights_by_asset_class())
        print_weight_table("Weights by Sector", self.weights_by_sector())

        self.print_total_cost_and_value()

    def monte_carlo_portfolio(self, days=252*15, total_simulations=100000, batch_size=10000):
        if not self.assets:
            print("Portfolio is empty, cannot run simulation.")
            return

        tickers = [asset.ticker for asset in self.assets]
        quantities = np.array([asset.quantity for asset in self.assets])
        
        # Download historical price data for all tickers
        data = yf.download(tickers, period="1y", auto_adjust=True)['Close'].dropna()
        
        returns = data.pct_change().dropna()
        mu = returns.mean().values
        cov = returns.cov().values
        S0 = data.iloc[-1].values
        L = np.linalg.cholesky(cov)

        num_batches = total_simulations // batch_size
        all_final_values = []

        for batch in range(num_batches):
            portfolio_values = np.zeros((days+1, batch_size))
            portfolio_values[0, :] = np.dot(S0, quantities)

            for sim in range(batch_size):
                Z = np.random.normal(size=(days, len(tickers)))
                correlated_Z = Z @ L.T
                daily_returns = correlated_Z + mu
                price_relatives = 1 + daily_returns
                prices = np.zeros((days+1, len(tickers)))
                prices[0] = S0
                for t in range(1, days+1):
                    prices[t] = prices[t-1] * price_relatives[t-1]
                portfolio_values[:, sim] = prices @ quantities
            
            all_final_values.append(portfolio_values[-1])

            print(f"Batch {batch + 1} of {num_batches} completed.")

        all_final_values = np.concatenate(all_final_values)

        summary = {
            'mean_final_value': np.mean(all_final_values),
            'median_final_value': np.median(all_final_values),
            '5th_percentile': np.percentile(all_final_values, 5),
            '95th_percentile': np.percentile(all_final_values, 95)
        }
        
        print(f"After {days} trading days (~{days//252} years):")
        print(f"Mean portfolio value: ${summary['mean_final_value']:.2f}")
        print(f"Median portfolio value: ${summary['median_final_value']:.2f}")
        print(f"5th percentile: ${summary['5th_percentile']:.2f}")
        print(f"95th percentile: ${summary['95th_percentile']:.2f}")

        return summary