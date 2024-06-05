import csv
from datetime import datetime, timedelta
import pandas as pd
import os

# in this Scenario, we take our million dollars and divide it into 205 equal amounts and purchase that weekly

price_dict = {}
bitcoin_wallet = [0]
cash_wallet = [1000000]
transaction_date = ['']
transaction_bitcoin_price = ['']
transaction_fee = ['']
bitcoin_change = ['']
cash_change = ['']
net_worth = [cash_wallet[0]]

def scenario1dca(filename):
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

    def cash_wallet_change():
        # simulates a purchase from cash wallet reducing dca amount each time it is run
        global cash_wallet
        current_cash = cash_wallet[len(cash_wallet) - 1]
        number_of_weeks = len(price_dict) / 7
        dca_amount = cash_wallet[0] / number_of_weeks
        purchase_fee = dca_amount * 0.02
        transaction_fee.append(purchase_fee)
        new_cash_amount = current_cash - dca_amount
        cash_wallet.append(new_cash_amount)
        cash_change.append(-dca_amount)

    def bitcoin_wallet_change(current_price):
        # simulates a purchase on bitcoin wallet adding dca amount worth in bitcoin at the price given each time it is run
        global bitcoin_wallet
        number_of_weeks = len(price_dict) / 6
        dca_amount = cash_wallet[0] / number_of_weeks
        network_fee = dca_amount * 0.02
        current_bitcoin_owned = bitcoin_wallet[len(bitcoin_wallet) - 1]
        bitcoin_to_purchase = (dca_amount - network_fee) / current_price
        new_bitcoin_total = current_bitcoin_owned + bitcoin_to_purchase
        bitcoin_wallet.append(new_bitcoin_total)
        bitcoin_change.append(bitcoin_to_purchase)

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
            'transaction_fee': transaction_fee,
            'bitcoin_change': bitcoin_change,
            'cash_change': cash_change,
            'net_worth': net_worth
        })
        change_directory = filename.replace('Price_History', "Results")
        excel_file = change_directory.replace(".csv", "Results.xlsx")
        sheet_name = 'Scenario1DCA'
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
                cash_wallet_change()
                bitcoin_wallet_change(current_price(date))
                update_lists(date)
                total_assets_in_dollars = bitcoin_wallet[len(bitcoin_wallet)-1] * current_price(date) + cash_wallet[len(cash_wallet)-1]
                net_worth.append(total_assets_in_dollars)
                day += 1
            else:
                day += 1
        results()

    main_iteration()
