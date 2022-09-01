import csv
# from locale import currency
import os
import json
import csv
import requests
from prettytable import PrettyTable
from colorama import Fore, Back, Style
from dotenv import load_dotenv
local_currency = 'USD'
local_currency_symbol = '$'

load_dotenv()
api_key = os.getenv('api_key')
headers = {'X-CMC_PRO_API_KEY': api_key}

base_url = 'https://pro-api.coinmarketcap.com'


portfolio_value = 0.0

table = PrettyTable(['Asset', 'Amount Owned', 'Value', 'Price', '1H', '24H', '7D'])

# csv_file = open("my_portfolio.csv")

with open("my.csv", 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        if 'ï»¿' in line[0]:                    #some special character in csv file
            line[0] = line[0][3:].upper()
        else:
            line[0] = line[0].upper()
        # print(line)
        symbol = line[0]
        amount = line[1]
        quote_url = base_url + '/v1/cryptocurrency/quotes/latest?convert=' + local_currency + '&symbol=' + symbol
        request = requests.get(quote_url, headers=headers)
        results = request.json()
        # print(json.dumps(results, sort_keys=True, indent=4))

        currency = results['data'][symbol]
        quote = currency['quote'][local_currency]

        name = currency['name']
        price = quote['price']
        value = float(price) * float(amount)
        hour_change = round(quote['percent_change_1h'],1)        
        day_change = round(quote['percent_change_24h'],1)
        week_change = round(quote['percent_change_7d'],1)

        if hour_change > 0:
            hour_change = Back.GREEN + str(hour_change) + '%' + Style.RESET_ALL
        else:
            hour_change = Back.RED + str(hour_change) + '%' + Style.RESET_ALL

        if day_change > 0:
            day_change = Back.GREEN + str(day_change) + '%' + Style.RESET_ALL
        else:
            day_change = Back.RED + str(day_change) + '%' + Style.RESET_ALL

        if week_change > 0:
            week_change = Back.GREEN + str(week_change) + '%' + Style.RESET_ALL
        else:
            week_change = Back.RED + str(week_change) + '%' + Style.RESET_ALL





        portfolio_value += value

        price_string = '{:,}'.format(round(price,2))
        value_string = '{:,}'.format(round(value,2))

        table.add_row([name + ' (' + symbol + ')', 
                    amount,
                    local_currency_symbol + value_string,
                    local_currency_symbol + price_string,
                    str(hour_change),
                    str(day_change),
                    str(week_change)])

print()
print("**********************************MY PORTFOLIO**********************************")
print()

print(table)

portfolio_value_string = '{:,}'.format(round(portfolio_value, 2))

print()
print('Total Portfolio value: ' + Back.GREEN + local_currency_symbol + portfolio_value_string + Style.RESET_ALL)
print()
print("********************************************************************************")
print()