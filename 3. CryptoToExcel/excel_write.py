import os
import requests
from dotenv import load_dotenv
import json
import xlsxwriter
local_currency = 'USD'
local_currency_symbol = '$'

load_dotenv()
api_key = os.getenv('api_key')
headers = {'X-CMC_PRO_API_KEY': api_key}

base_url = 'https://pro-api.coinmarketcap.com'

crypto_workbook = xlsxwriter.Workbook('cryptocurrencies.xlsx')
crypto_sheet = crypto_workbook.add_worksheet()

crypto_sheet.write('A1', 'Name')
crypto_sheet.write('B1', 'Symbol')
crypto_sheet.write('C1', 'Market Cap')
crypto_sheet.write('D1', 'Price')
crypto_sheet.write('E1', '24H Volume')
crypto_sheet.write('F1', 'Hour Change')
crypto_sheet.write('G1', 'Day Change')
crypto_sheet.write('H1', 'Week Change')

start = 1
row = 1

for i in range(10):
    listings_url = base_url + '/v1/cryptocurrency/listings/latest?convert='+local_currency+'&start='+str(start)

    request = requests.get(listings_url, headers=headers)
    results = request.json()

    data = results['data']

    for currency in data:
        name = currency['name']
        symbol = currency['symbol']

        quote = currency['quote'][local_currency]
        market_cap = round(quote['market_cap'], 2)
        hour_change = round(quote['percent_change_1h'], 2)
        day_change = round(quote['percent_change_24h'], 2)
        week_change = round(quote['percent_change_7d'], 2)
        price = round(quote['price'], 2)
        volume = round(quote['volume_24h'], 2)

        volume_string = '{:,}'.format(volume)
        market_cap_string = '{:,}'.format(market_cap)

        crypto_sheet.write(row,0,name)
        crypto_sheet.write(row,1,symbol)
        crypto_sheet.write(row,2,local_currency_symbol + market_cap_string)
        crypto_sheet.write(row,3,local_currency_symbol + str(price))
        crypto_sheet.write(row,4,local_currency_symbol + volume_string)
        crypto_sheet.write(row,5,str(hour_change) + '%')
        crypto_sheet.write(row,6,str(day_change) + '%')
        crypto_sheet.write(row,7,str(week_change) + '%')
        row += 1
    # print(json.dumps(data, sort_keys=True, indent=4))
    start += 100

crypto_workbook.close()
