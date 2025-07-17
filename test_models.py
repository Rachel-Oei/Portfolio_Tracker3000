from models import Asset, Portfolio

def test_asset():
    asset = Asset("AAPL", 10, 150)
    asset.update_close()

    print(f"Ticker: {asset.ticker}")
    print(f"Sector: {asset.sector}")
    print(f"Asset class: {asset.asset_class}")
    print(f"Market Cap: {asset.market_cap}")
    print(f"Daily Return={asset.daily_return:.2f}%, ")
    print(f"Quantity: {asset.quantity}")
    print(f"Purchase price: ${asset.purchase_price}")
    print(f"Latest adjusted close price: ${asset.close}")
    print(f"Transaction value: ${asset.transaction_value():.2f}")
    print(f"Current value: ${asset.current_value():.2f}")

def test_portfolio():
    portfolio = Portfolio()
    asset1 = Asset("AAPL", 10, 150)
    asset2 = Asset("MSFT", 5, 200)
    portfolio.add_asset(asset1)
    portfolio.add_asset(asset2)
    portfolio.update_all_closes()
    portfolio.summary()
    
if __name__ == "__main__":
    test_asset()
    test_portfolio()