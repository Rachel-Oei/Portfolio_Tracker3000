from models import Asset

def test_asset():
    # Create an asset instance
    asset = Asset("AAPL", "Technology", "Stock", 10, 150)
    
    # Update the adjusted close price from Yahoo Finance
    asset.update_adjusted_close()
    
    # Print relevant info to verify functionality
    print(f"Ticker: {asset.ticker}")
    print(f"Sector: {asset.sector}")
    print(f"Quantity: {asset.quantity}")
    print(f"Purchase price: ${asset.purchase_price}")
    print(f"Latest adjusted close price: ${asset.adj_close}")
    print(f"Transaction value: ${asset.transaction_value():.2f}")
    print(f"Current value: ${asset.current_value():.2f}")

if __name__ == "__main__":
    test_asset()