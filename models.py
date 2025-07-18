import yfinance as yf

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

    def summary(self):
        print("Portfolio Summary:")
        for asset in self.assets:
            weight = self.weights().get(asset.ticker, 0)
            market_cap = asset.market_cap if asset.market_cap is not None else 0
            daily_return = f"{asset.daily_return:.2f}%" if asset.daily_return is not None else "N/A"
            
            print(
                f"{asset.ticker}: "
                f"Quantity={asset.quantity}, "
                f"Current Value=${asset.current_value() or 0:.2f}, "
                f"Weight={weight:.2%}, "
                f"Market Cap=${int(market_cap/1000000000)}B, "
                f"Daily Return={daily_return}"
            )
        print(f"Total Cost: ${self.total_cost():.2f}")
        print(f"Total Value: ${self.total_value():.2f}")

        print("Weights by Asset Class:")
        for asset_class, weight in self.weights_by_asset_class().items():
            print(f"{asset_class}: {weight:.2%}")

        print("Weights by Sector:")
        for sector, weight in self.weights_by_sector().items():
            print(f"{sector}: {weight:.2%}")
        
