import csv
import pandas as pd
from datetime import datetime, timedelta
import os

# in this scenario, we'll be only buying based on the weekly percentage difference of bitcoin based on the cash we hold
# e.g. bitcoin weekly change is 3% and have $100,000, we buy 3,000$ worth of bitcoin.


price_dict = {}
bitcoin_wallet = [0]
cash_wallet = [1000000]
transaction_date = [0]
transaction_bitcoin_price = [0]
transaction_fee = [0]
bitcoin_change = [0]
cash_change = [0]
percent_changes = [0]


def scenario3(filename):
    with open(filename, mode='r') as file:
        # takes input file name and opens the data that will be used
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            date = row[0]
            price = float(row[1])
            price_dict[date] = price

    def current_price(current_date):
        # returns bitcoin price at date given
        return float(price_dict[current_date])

    def last_week_price(current_date):
        # find the price of bitcoin a week before given date
        start_date = datetime.strptime(current_date, "%Y-%m-%d")
        last_week_date = start_date + timedelta(days=-7)
        return price_dict[last_week_date.strftime("%Y-%m-%d")]

    def percent_change(current_price, last_week_price):
        # give the percent change of current price and last week's price as a float
        return (current_price - last_week_price) / last_week_price

    def cash_wallet_change(percent_change):
        # if percent change of bitcoin price is a negative meaning price has dropped, the fn will reduce current
        # money held by 2% simulating a purchase, otherwise fills information lists accordingly
        global cash_wallet
        current_cash = cash_wallet[len(cash_wallet) - 1]
        if percent_change < 0:
            amount_to_buy = current_cash * (percent_change * -1)
            new_cash_amount = current_cash - amount_to_buy
            cash_wallet.append(new_cash_amount)
            cash_change.append(-amount_to_buy)
            percent_changes.append(percent_change)
            return float(amount_to_buy)
        else:
            amount_to_buy = 0
            cash_change.append(0)
            cash_wallet.append(cash_wallet[len(cash_wallet) - 1])
            percent_changes.append(percent_change)
            return float(amount_to_buy)

    def bitcoin_wallet_change(amount_to_buy, current_price):
        # takes input of amount to buy in dollars reduces the network fee of 2% and divides by current price getting
        # the bitcoin amount bought. adds this amount to the current holdings and adds to the end of the bitcoin wallet
        global bitcoin_wallet
        current_bitcoin_owned = bitcoin_wallet[len(bitcoin_wallet) - 1]
        network_fee = amount_to_buy * .02
        transaction_fee.append(network_fee)
        new_bitcoin_added = (amount_to_buy - network_fee) / current_price
        new_bitcoin_owned = current_bitcoin_owned + new_bitcoin_added
        bitcoin_wallet.append(new_bitcoin_owned)
        bitcoin_change.append(new_bitcoin_added)

    def update_lists(date):
        # adds additional info to lists based on date given to analyze later
        transaction_date.append(date)
        transaction_bitcoin_price.append(current_price(date))

    def results():
        # creates a dataframe of the lists we want to analyze, makes new sheet for current simulation in given excel
        # file and exports dataframe into it
        df = pd.DataFrame({
            'transaction_date': transaction_date,
            'bitcoin_wallet': bitcoin_wallet,
            'cash_wallet': cash_wallet,
            'bitcoin_price': transaction_bitcoin_price,
            'transaction_fee': transaction_fee
        })
        change_directory = filename.replace('Price_History', "Results")
        excel_file = change_directory.replace(".csv", "Results.xlsx")
        sheet_name = 'Scenario3'
        if not os.path.isfile(excel_file):
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    def main_iteration():
        # Loop that runs through the given data set and runs the simulation functions on each 7th day.
        global purchases, transaction_date, transaction_bitcoin_price

        day = 1
        for date in sorted(price_dict):
            date = datetime.strptime(date, "%Y-%m-%d") + timedelta(days=+1)
            date = date.strftime("%Y-%m-%d")

            if day % 7 == 0:
                bitcoin_wallet_change(cash_wallet_change(percent_change(current_price(date), last_week_price(date))),
                                      current_price(date))
                update_lists(date)
                day += 1
            else:
                day += 1
        results()

    main_iteration()
