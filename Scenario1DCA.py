import csv
from datetime import datetime, timedelta
import pandas as pd
import os

# in this Scenario, we take our million dollars and divide it into 205 equal amounts and purchase that weekly

price_dict = {}
bitcoin_wallet = [0]
cash_wallet = [1000000]
transaction_date = [0]
transaction_bitcoin_price = [0]
transaction_fee = [0]



def scenario1DCA(filename):
    with open(filename, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            date = row[0]
            price = float(row[1])
            price_dict[date] = price

    def current_price(current_date):
        return float(price_dict[current_date])

    def cash_wallet_change():
        global cash_wallet
        current_cash = cash_wallet[len(cash_wallet) - 1]
        number_of_weeks = len(price_dict)/7
        dca_amount = cash_wallet[0] / number_of_weeks
        purchase_fee = dca_amount * 0.02
        transaction_fee.append(purchase_fee)
        new_cash_amount = current_cash - dca_amount - purchase_fee
        cash_wallet.append(new_cash_amount)

    def bitcoin_wallet_change(current_price):
        global bitcoin_wallet
        number_of_weeks = len(price_dict)/6
        dca_amount = cash_wallet[0] / number_of_weeks
        current_bitcoin_owned = bitcoin_wallet[len(bitcoin_wallet) - 1]
        bitcoin_to_purchase = dca_amount / current_price
        new_bitcoin_total = current_bitcoin_owned + bitcoin_to_purchase
        bitcoin_wallet.append(new_bitcoin_total)

    def update_lists(date):
        transaction_date.append(date)
        transaction_bitcoin_price.append(current_price(date))

    def results():
        df = pd.DataFrame({
            'transaction_date': transaction_date,
            'bitcoin_wallet': bitcoin_wallet,
            'cash_wallet': cash_wallet,
            'bitcoin_price': transaction_bitcoin_price,
            'transaction_fee': transaction_fee,
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
        global purchases, transaction_date, transaction_bitcoin_price

        day = 1
        for date in sorted(price_dict):
            date = datetime.strptime(date, "%Y-%m-%d") + timedelta(days=+1)
            date = date.strftime("%Y-%m-%d")

            if day % 7 == 0:
                cash_wallet_change()
                bitcoin_wallet_change(current_price(date))
                update_lists(date)
                day += 1
            else:
                day += 1
        results()

    main_iteration()
