import csv
import pandas as pd
from datetime import datetime, timedelta
import os

# in this scenario, we'll be buying and selling based on the weekly percentage difference of bitcoin based on the cash we hold
# e.g. bitcoin weekly change is 3% and have $100,000, we sell 3,000$ worth of bitcoin. we buy that amount if its -3%


price_dict = {}
bitcoin_wallet = [0]
cash_wallet = [1000000]
transaction_date = [0]
transaction_bitcoin_price = [0]
transaction_fee = [0]


def scenario2(filename):
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

    def percent_change(current_price, last_week_price):
        return (current_price - last_week_price) / last_week_price

    def cash_wallet_change(percent_change):
        global cash_wallet, transaction_fee
        # if price goes up we sell bitcoin therefore gain money
        current_cash = cash_wallet[len(cash_wallet) - 1]
        amount_to_sell_or_buy = current_cash * percent_change
        if amount_to_sell_or_buy < 0:
            selling_fee = amount_to_sell_or_buy * .02 * -1
        else:
            selling_fee = amount_to_sell_or_buy * .02
        new_cash_amount = current_cash + amount_to_sell_or_buy - selling_fee
        cash_wallet.append(new_cash_amount)
        transaction_fee.append(selling_fee)
        return amount_to_sell_or_buy

    def update_lists(date):
        transaction_date.append(date)
        transaction_bitcoin_price.append(current_price(date))

    def bitcoin_wallet_change(cash_wallet_change, current_price):
        global bitcoin_wallet
        current_bitcoin_owned = bitcoin_wallet[len(bitcoin_wallet) - 1]
        new_bitcoin_added = cash_wallet_change / current_price
        new_bitcoin_owned = current_bitcoin_owned + new_bitcoin_added
        bitcoin_wallet.append(new_bitcoin_owned)

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
        sheet_name = 'Scenario2'
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
                bitcoin_wallet_change(cash_wallet_change(percent_change(current_price(date), last_week_price(date))),
                                      current_price(date))
                update_lists(date)
                day += 1
            else:
                day += 1
        results()

    main_iteration()
