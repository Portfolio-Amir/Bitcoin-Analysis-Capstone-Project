import csv
import pandas as pd
from datetime import datetime, timedelta
import os

# in this scenario, we'll be buying and selling based on the weekly percentage difference of bitcoin based on the cash we hold
# e.g. bitcoin weekly change is 3% and have $100,000, we sell 3,000$ worth of bitcoin. we buy that amount if its -3%


price_dict = {}
bitcoin_wallet = [0]
cash_wallet = [1000000]
transaction_date = ['']
transaction_bitcoin_price = ['']
transaction_fee = ['']
bitcoin_change = ['']
cash_change = ['']
percent_changes = ['']
net_worth = [cash_wallet[0]]


def scenario2(filename):
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

    def is_asset_enough(percent_change, current_price):
        if percent_change < 0:
            # if price goes down we buy and because we are always buying a percentage of our current money we will
            # not run out of money
            return True
        else:
            # if price goes up we sell, so we need to make sure out bitcoin is enough
            money_owned_currently = cash_wallet[len(cash_wallet) - 1]
            bitcoin_to_sell = percent_change * money_owned_currently / current_price
            bitcoin_owned_currently = bitcoin_wallet[len(bitcoin_wallet) - 1]
            if (bitcoin_owned_currently - bitcoin_to_sell) < 0:
                return False
            else:
                return True

    def cash_wallet_change(percent_change, current_price):
        if is_asset_enough(percent_change, current_price):
            # if we have enough assets to buy or sell without our money or bitcoin going below 0
            if percent_change < 0:
                # if price goes down we buy the dip, which means our money will go down
                money_owned_currently = cash_wallet[len(cash_wallet) - 1]
                amount_to_buy = money_owned_currently * percent_change * -1
                new_money_owned = money_owned_currently - amount_to_buy
                cash_wallet.append(new_money_owned)
                cash_change.append(-amount_to_buy)
                percent_changes.append(percent_change)
            else:
                # if price goes up we take profit and sell, which means our money will go up
                money_owned_currently = cash_wallet[len(cash_wallet) - 1]
                amount_to_sell = money_owned_currently * percent_change
                new_money_owned = money_owned_currently + amount_to_sell
                cash_wallet.append(new_money_owned)
                cash_change.append(amount_to_sell)
                percent_changes.append(percent_change)
        else:
            # if our bitcoin or cash will dip below 0 with action than we don't do anything and fill our lists
            # accordingly
            cash_wallet.append(cash_wallet[len(cash_wallet) - 1])
            cash_change.append(0)
            percent_changes.append(percent_change)

    def bitcoin_wallet_change(percent_change, current_price):
        if is_asset_enough(percent_change, current_price):
            # if we have enough assets to buy or sell without our money or bitcoin going below 0
            if percent_change < 0:
                # if price goes down we buy the dip, which means our bitcoin goes up
                money_owned_currently = cash_wallet[len(cash_wallet) - 1]
                bitcoin_currently_owned = bitcoin_wallet[len(cash_wallet) - 1]
                amount_to_buy_dollars = money_owned_currently * percent_change * -1
                # network fee deducted from investment amount
                network_fee = amount_to_buy_dollars * 0.02
                amount_to_buy_bitcoin = (amount_to_buy_dollars - network_fee) / current_price
                new_bitcoin_holding = bitcoin_currently_owned + amount_to_buy_bitcoin
                bitcoin_wallet.append(new_bitcoin_holding)
                bitcoin_change.append(amount_to_buy_bitcoin)
                transaction_fee.append(network_fee)
            else:
                # if price goes up we take profit and sell, which means our bitcoin will go down
                money_owned_currently = cash_wallet[len(cash_wallet) - 1]
                bitcoin_currently_owned = bitcoin_wallet[len(cash_wallet) - 1]
                amount_to_sell_dollars = money_owned_currently * percent_change
                # network fee deducted from investment amount
                network_fee = amount_to_sell_dollars * 0.02
                amount_to_sell_bitcoin = (amount_to_sell_dollars - network_fee) / current_price
                new_bitcoin_holding = bitcoin_currently_owned - amount_to_sell_bitcoin
                bitcoin_wallet.append(new_bitcoin_holding)
                bitcoin_change.append(-amount_to_sell_bitcoin)
                transaction_fee.append(network_fee)
        else:
            # if our bitcoin or cash will dip below 0 with action than we don't do anything and fill our lists
            # accordingly
            bitcoin_wallet.append(bitcoin_wallet[len(bitcoin_wallet) - 1])
            bitcoin_change.append(0)
            transaction_fee.append(0)

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
            'percent_changes': percent_changes,
            'bitcoin_change': bitcoin_change,
            'cash_change': cash_change,
            'net_worth': net_worth
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
        # Loop that runs through the given data set and runs the simulation functions on each 7th day.
        day = 1
        for date in sorted(price_dict):
            date = datetime.strptime(date, "%Y-%m-%d") + timedelta(days=+1)
            date = date.strftime("%Y-%m-%d")

            if day % 7 == 0:
                bitcoin_wallet_change(percent_change(current_price(date), last_week_price(date)), current_price(date))
                cash_wallet_change(percent_change(current_price(date), last_week_price(date)), current_price(date))
                update_lists(date)
                total_assets_in_dollars = bitcoin_wallet[len(bitcoin_wallet)-1] * current_price(date) + cash_wallet[len(cash_wallet)-1]
                net_worth.append(total_assets_in_dollars)
                day += 1
            else:
                day += 1
        results()

    main_iteration()
