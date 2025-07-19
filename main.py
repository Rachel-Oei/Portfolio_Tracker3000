from models import Asset, Portfolio
from view import print_asset_table, print_weight_table, plot_multiple_assets, print_main_menu

from montecarlo import run_monte_carlo
from colorama import Fore

def main():
    portfolio = Portfolio()

    while True:
        print_main_menu()

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        match choice:
            case 1:
                portfolio.add_assets()
            case 2:
                plot_multiple_assets(portfolio.assets, period="20y", interval="1d")
            case 3:
                portfolio.summary()
            case 4:
                portfolio.monte_carlo_portfolio()
            case 5:
                print("Thanks for using the Portfolio Tracker. Goodbye!")
                break
            case _:
                print("Invalid choice. Please enter 1, 2, 3, 4 or 5.")

if __name__ == "__main__":
    main()