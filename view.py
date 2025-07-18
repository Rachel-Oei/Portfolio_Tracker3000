import matplotlib.pyplot as plt
import yfinance as yf
import os

def plot_multiple_assets(assets, period, interval):
    plt.figure(figsize=(12, 6))
    
    for asset in assets:
        data = yf.Ticker(asset.ticker).history(period=period, interval=interval)
        if data.empty:
            print(f"⚠️  No data for {asset.ticker}, skipping.")
            continue

        plt.plot(data.index, data['Close'], label=asset.ticker)

    plt.title(f"Historical Price Comparison ({period})")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("historical_prices.png")
    print("Graph saved as 'historical_prices.png'")
    print(f"\nOpen the image manually from the sidebar or at: file://{os.path.abspath("historical_prices.png")}\n")

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
    print("\nCurrent Portfolio Overview:")
    print(f"{'Ticker':<10} {'Asset Class':<15} {'Sector':<30} {'Mkt Cap':<10} {'Qty':<5} {'Purchase Price':<15} {'Current Price':<15} {'Daily Return':<15}")
    print("-" * 115)

    for a in portfolio.assets:
        market_cap = f"${int(a.market_cap / 1_000_000_000)}B" if isinstance(a.market_cap, (int, float)) else "N/A"
        current_price = f"${a.close:.2f}" if a.close else "N/A"
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