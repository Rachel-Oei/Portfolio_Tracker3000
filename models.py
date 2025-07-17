import yfinance as yf

class Asset:
    def __init__(self, ticker, quantity, purchase_price):
        self.ticker = ticker
        self.quantity = quantity
        self.purchase_price = purchase_price
        self.close = None

        info = yf.Ticker(ticker).info
        self.asset_class = info.get("quoteType", "UNKNOWN")
        self.sector = info.get("sector", "UNKNOWN")

    def update_adjusted_close(self):
        data = yf.Ticker(self.ticker)
        hist = data.history(period="max")  
        close_series = hist['Close']     
        self.close = close_series.iloc[-1] 
        
    def transaction_value(self):
        return self.quantity * self.purchase_price

    def current_value(self):
        if self.close is None:
            return None
        return self.quantity * self.close