from models import Asset, Portfolio

def add_assets(portfolio):
    while True:
        choice = input("Do you wish to add an asset (y/n)? ").lower()
        if choice == 'y':
            ticker = input("Enter the ticker: ").upper()
            quantity = int(input("Enter the quantity: "))
            purchase_price = float(input("Enter the purchase price (USD): "))
            asset = Asset(ticker, quantity, purchase_price)
            asset.update_close()
            portfolio.add_asset(asset)
        else:
            break

def main():
    # all the main steps here
    portfolio = Portfolio()
    add_assets(portfolio)
    portfolio.summary()

if __name__ == "__main__":
    main()