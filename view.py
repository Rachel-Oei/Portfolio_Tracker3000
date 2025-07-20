import matplotlib.pyplot as plt
import yfinance as yf
import os
from colorama import Fore, Style, init

def print_main_menu():
    print(Fore.BLACK + "\n" + "=" * 40)
    print(Fore.BLACK + "PORTFOLIO TRACKER 3000 MENU".center(40))
    print(Fore.BLACK + "=" * 40)
    print(Fore.BLACK + "1." + Fore.WHITE + " ➕ Add an asset")
    print(Fore.BLACK + "2." + Fore.WHITE + " 📈 View historical prices")
    print(Fore.BLACK + "3." + Fore.WHITE + " 🧾 View portfolio summary")
    print(Fore.BLACK + "4." + Fore.WHITE + " 🎲 Run Monte Carlo simulation")
    print(Fore.BLACK + "5." + Fore.WHITE + " ❌ Exit")
    print(Fore.BLACK + "=" * 40)

def plot_multiple_assets(assets, period, interval):
    plt.figure(figsize=(12, 6))
    
    for asset in assets:
        data = yf.Ticker(asset.ticker).history(period=period, interval=interval)
        if data.empty:
            print(f"No data for {asset.ticker}, skipping.")
            continue

        plt.plot(data.index, data['Close'], label=asset.ticker)

    plt.title(f"Historical Prices ({period})")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.grid(True)
    plt.legend()
    plt.grid(False)
    plt.tight_layout()
    plt.savefig("historical_prices.png")
    print("Graph saved as 'historical_prices.png'")

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

def print_asset_table(portfolio):
    print("\n\033[1mCurrent Portfolio Overview:\033[0m")
    print(f"{'Ticker':<10} {'Asset Class':<15} {'Sector':<30} {'Mkt Cap':<10} {'Qty':<5} {'Purchase Price':<15} {'Current Price':<15} {'Daily Return':<15}")
    print("-" * 135)

    for a in portfolio.assets:
        market_cap = f"${int(a.market_cap / 1_000_000_000)}B" if isinstance(a.market_cap, (int, float)) else "N/A"
        current_price = f"${a.close:.2f}" if a.close else "N/A"

        # Format daily_return with colors
        if a.daily_return is not None:
            if a.daily_return > 0:
                color = "\033[92m"  # Green
                return_str = f"+{a.daily_return:.2f}%"
            elif a.daily_return < 0:
                color = "\033[91m"  # Red
                return_str = f"{a.daily_return:.2f}%"
            else:
                color = "\033[0m"   # Default
                return_str = "0.00%"
            daily_return = f"{color}{return_str}\033[0m"
        else:
            daily_return = "N/A"

        print(f"{a.ticker:<10} {a.asset_class:<15} {a.sector:<30} {market_cap:<10} {a.quantity:<5} ${a.purchase_price:<14.2f} {current_price:<15} {daily_return:<15}")
