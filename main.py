from models import Asset, Portfolio

def add_assets(portfolio):
    while True:
        choice = input("Menu: \n1. Add asset \n2. View portfolio").lower()
        if choice == '1':
            ticker = input("Enter the ticker: ").upper()
            quantity = int(input("Enter the quantity: "))
            purchase_price = float(input("Enter the purchase price (USD): "))
            asset = Asset(ticker, quantity, purchase_price)
            asset.update_close()
            portfolio.add_asset(asset)

            print("\nCurrent Portfolio Overview:")
            print(f"{'Ticker':<10} {'Asset Class':<15} {'Sector':<30} {'Mkt Cap':<10} {'Qty':<5} {'Purchase Price':<15} {'Current Price':<15} {'Daily Return %':<15}")
            print("-" * 115)

            for a in portfolio.assets:
                market_cap = f"${int(a.market_cap / 1_000_000_000)}B" if isinstance(a.market_cap, (int, float)) else "N/A"
                current_price = f"${a.close:.2f}" if a.close else "N/A"
                daily_return = f"{a.daily_return:.2f}%" if a.daily_return is not None else "N/A"
                print(f"{a.ticker:<10} {a.asset_class:<15} {a.sector:<30} {market_cap:<10} {a.quantity:<5} ${a.purchase_price:<14.2f} {current_price:<15} {daily_return:<15}")
            print()

            def print_weight_table(title, weight_dict):
                print(f"\n{title}")
                print(f"{'Name':<25} {'Weight %':<10} {'Bar':<50}")
                print("-" * 85)

                colors = ["\033[90m", "\033[97m"]  # dark gray, white
                reset = "\033[0m"

                for i, (name, weight) in enumerate(sorted(weight_dict.items(), key=lambda x: -x[1])):
                    color = colors[i % 2]  # alternate color per row
                    bar = '█' * int(weight * 50)
                    print(f"{name:<25} {weight * 100:>6.2f}%   {color}{bar}{reset}")
            
            print_weight_table("Weights by Asset", portfolio.weights())
            print_weight_table("Weights by Asset Class", portfolio.weights_by_asset_class())
            print_weight_table("Weights by Sector", portfolio.weights_by_sector())
        else:
            break

def main():
    # all the main steps here
    portfolio = Portfolio()
    add_assets(portfolio)
    portfolio.summary()

if __name__ == "__main__":
    main()