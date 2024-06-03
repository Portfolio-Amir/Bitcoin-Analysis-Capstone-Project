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
dca_amount = 4878
dca_fee = dca_amount * .02


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

    def last_week_price(current_date):
        start_date = datetime.strptime(current_date, "%Y-%m-%d")
        last_week_date = start_date + timedelta(days=-7)
        return price_dict[last_week_date.strftime("%Y-%m-%d")]

    def cash_wallet_change():
        global cash_wallet, dca_amount
        current_cash = cash_wallet[len(cash_wallet) - 1]
        purchase_fee = dca_amount * 0.02
        new_cash_amount = current_cash - dca_amount - purchase_fee
        cash_wallet.append(new_cash_amount)

    def bitcoin_wallet_change(current_price):
        global bitcoin_wallet, dca_amount
        current_bitcoin_owned = bitcoin_wallet[len(bitcoin_wallet) - 1]
        bitcoin_to_purchase = dca_amount / current_price
        new_bitcoin_total = current_bitcoin_owned + bitcoin_to_purchase
        bitcoin_wallet.append(new_bitcoin_total)

    def update_lists(date):
        transaction_date.append(date)
        transaction_bitcoin_price.append(current_price(date))
        transaction_fee.append(dca_fee)

    def results():
        df = pd.DataFrame({
            'transaction_date': transaction_date,
            'bitcoin_wallet': bitcoin_wallet,
            'cash_wallet': cash_wallet,
            'bitcoin_price': transaction_bitcoin_price,
            'transaction_fee': transaction_fee
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
                update_lists(date)
                cash_wallet_change()
                bitcoin_wallet_change(current_price(date))
                day += 1
            else:
                day += 1
        results()

    main_iteration()
