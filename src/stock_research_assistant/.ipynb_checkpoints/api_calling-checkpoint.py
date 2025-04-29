import os
from dotenv import load_dotenv
load_dotenv()

########## This is where pullin the symbol from 
import finnhub
import json
import requests

fin_api = os.getenv("FINNHUB_API_KEY")

def client_setup():
    client = finnhub.Client(api_key=fin_api)
    return client

def symbol_lookup(search_term):
    c = client_setup()
    print("Fetching US stock symbols for NASDAQ (MIC: XNAS)...")
    us_symbols_list = c.stock_symbols(exchange="US", mic='XNAS')
    print(f"Fetched {len(us_symbols_list)} symbols for NASDAQ.")
    print(f"\nSearching for stocks with '{search_term}' in their name/description...")
    for symbol_info in us_symbols_list:
    
        description = symbol_info.get('description', '')
        symbol = symbol_info.get('symbol', '')
        display_symbol = symbol_info.get('displaySymbol', '')
        
        # Check if the search term is in the description (case-insensitive)
        if search_term.lower() in description.lower():
            a = symbol_info
            
            print(f"Found the display symbol: {a['displaySymbol']}")
            break

    return f"Symbol_lookup_api_response: {a['displaySymbol']}"    

##### This is where we are pulling the stocks data from
market_api = os.getenv("MARKETDATA_API_KEY")

def get_response(sym,start_date,end_date):
    url = f"https://api.marketdata.app/v1/stocks/candles/D/{sym}/?from={start_date}&to={end_date}&token={market_api}"
    r = requests.get(url)
    res = r.json()
    return {'timeframe_in_unix_encoding':res['t'] , 'opening_price':res['o'] , 'highest_price_of_the_day':res['h'] , 'lowest_price_of_the_day':res['l'] ,'closing_price_of_the_day':res['c']}
