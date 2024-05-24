import csv
import pandas as pd
from datetime import datetime, timedelta

# In this Scenario we buy and sell based on percentage change of the bitcoin price from out current portfolio
# e.g. we have 1 bitcoin. weekly price change is +3% we sell 3% of our current holdings.
# if weekly price change is -3%. we buy 3% worth of our current holdings.
price_dict = {}
bitcoin_wallet = [47.19764]
cash_wallet = [500000]
transaction_date = [0]
transaction_bitcoin_price = [0]
transaction_fee = [0]

with open('BITCOIN(06-2018-06-2022).csv', mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        date = row[0]
        price = float(row[1])
        price_dict[date] = price


def current_price(current_date):
    return price_dict[current_date]


def last_week_price(current_date):
    start_date = datetime.strptime(current_date, "%Y-%m-%d")
    last_week_date = start_date + timedelta(days=-7)
    return price_dict[last_week_date.strftime("%Y-%m-%d")]


def percent_change(current_price, last_week_price):
    return ((current_price - last_week_price) / last_week_price)


def bitcoin_wallet_change(percent_change):
    global bitcoin_wallet
    # If bitcoin goes down we buy that percent change in bitcoin. If it goes up we sell that percent change. e.g.
    # 1 bitcoin we hold. If bitcoin goes down in price by 1% we buy 0.01 bitcoin and returns the amount bought or sold
    if percent_change < 0:
        percent_to_purchase = percent_change * (-1)
        current_bitcoin_owned = bitcoin_wallet[len(bitcoin_wallet) - 1]
        bitcoin_purchase_amount = percent_to_purchase * current_bitcoin_owned
        new_bitcoin_amount = current_bitcoin_owned + bitcoin_purchase_amount
        bitcoin_wallet.append(new_bitcoin_amount)
        return bitcoin_purchase_amount
    else:
        current_bitcoin_owned = bitcoin_wallet[len(bitcoin_wallet) - 1]
        bitcoin_sell_amount = percent_change * current_bitcoin_owned
        new_bitcoin_amount = current_bitcoin_owned - bitcoin_sell_amount
        bitcoin_wallet.append(new_bitcoin_amount)
        return bitcoin_sell_amount * -1


def cash_wallet_change(bitcoin_wallet_change, current_price):
    global cash_wallet
    if bitcoin_wallet_change < 0:
        amount_sold = (bitcoin_wallet_change * -1) * current_price
        current_cash = cash_wallet[len(cash_wallet) - 1]
        selling_fee = (amount_sold * .02)
        new_cash_owned = current_cash + amount_sold - selling_fee
        cash_wallet.append(new_cash_owned)
        transaction_fee.append(selling_fee)
    else:
        amount_bought = bitcoin_wallet_change * current_price
        purchase_fee = amount_bought * .02
        current_cash = cash_wallet[len(cash_wallet) - 1]
        new_cash_owned = current_cash - amount_bought - purchase_fee
        cash_wallet.append(new_cash_owned)
        transaction_fee.append(purchase_fee)


def results():
    df = pd.DataFrame({
        'transaction_date': transaction_date,
        'bitcoin_wallet': bitcoin_wallet,
        'cash_wallet': cash_wallet,
        'bitcoin_price': transaction_bitcoin_price,
        'transaction_fee': transaction_fee
    })
    excel_file = 'results2018-2022.xlsx'
    df.to_excel(excel_file, index=False)


def main_iteration():
    global purchases, transaction_date, transaction_bitcoin_price

    day = 1
    for date in sorted(price_dict):
        date = datetime.strptime(date, "%Y-%m-%d") + timedelta(days=+1)
        date = date.strftime("%Y-%m-%d")

        if day % 7 == 0:
            transaction_date.append(date)
            transaction_bitcoin_price.append(current_price(date))
            cash_wallet_change(bitcoin_wallet_change(percent_change(current_price(date), last_week_price(date))),
                               current_price(date))
            day += 1
        else:
            day += 1


main_iteration()
results()
