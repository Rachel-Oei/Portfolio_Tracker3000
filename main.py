from models import Asset, Portfolio

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
            portfolio.print_asset_table()
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