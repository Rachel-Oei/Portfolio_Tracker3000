from models import Asset, Portfolio

def main():
    portfolio = Portfolio()

    while True:
        print("\nWhat do you wish to do?")
        print("1. Add an asset")
        print("2. View portfolio summary")
        print("3. Exit")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        match choice:
            case 1:
                portfolio.add_assets()
            case 2:
                portfolio.print_asset_table()
                portfolio.print_weight_table("Weights by Asset", portfolio.weights())
                portfolio.print_weight_table("Weights by Asset Class", portfolio.weights_by_asset_class())
                portfolio.print_weight_table("Weights by Sector", portfolio.weights_by_sector())
                portfolio.summary()
            case 3:
                print("Thanks for using the Portfolio Tracker. Goodbye!")
                break
            case _:
                print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()