import yfinance as yf

class Asset:
    def __init__(self, ticker, sector, asset_class, quantity, purchase_price):
        self.ticker = ticker
        self.sector = sector
        self.asset_class = asset_class
        self.quantity = quantity
        self.purchase_price = purchase_price
        self.adj_close = None

    def update_adjusted_close(self):
        data = yf.Ticker(self.ticker)
        hist = data.history(period="max")  
        adj_close_series = hist['Adj Close']      
        self.adj_close = adj_close_series.iloc[-1] 
        
    def transaction_value(self):
        return self.quantity * self.purchase_price

    def current_value(self):
        if self.adj_close is None:
            return None
        return self.quantity * self.adj_close