print(" Welcome to Portfolio Tracker 3000")

def stocks():
    while True: 
        choice = input("Do you wish to add a stock (y/n)? ").lower()
        if choice == 'y':
            stock_name = input("Enter the stock name: ").upper()
            if stock_name in stock_prices:
                stock_qty = int(input("Enter the quantity: "))
                portfolio[stock_name] = portfolio.get(stock_name, 0) + stock_qty
            else:
                print("Stock not found in our database.")
        else:
            break

def balance():
    total = 0
    print("\nPortfolio Summary:")
    for stock, qty in portfolio.items():
        price = stock_prices[stock]
        investment = price * qty
        total += investment
        print(f"{stock}: {qty} x ${price} = ${investment}")
    print("Total money invested: $", total)
    return total
while True:
    print("\nWhat do you wish to perform?\n1. Input your stocks\n2. Check your balance and stock summary\n3. Exit")
    n = int(input("Enter your choice: "))
    
    match n:
        case 1:
            stocks()
        case 2:
            balance()
        case 3:
            print("Thanks for using. See you again!")
            break
        case _:
            print("Invalid choice. Please enter 1, 2, or 3.")