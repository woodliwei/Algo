import time
from binance.exceptions import BinanceAPIException, BinanceOrderException
from binance.enums import *
from time import sleep
from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor
from Clients.Util import *
from datetime import datetime

api_key = BA_K
api_secret = BA_S

client = Client(api_key, api_secret)

####!!! change !!!!
coinname = "ALICEUSDT"
asset = "ALICE"
buy_qty = 0.01
#asset = "TKO"
#coinname = "ALICEUSDT"

coin_price = client.get_symbol_ticker(symbol=coinname)
coin_price = float(coin_price['price'])


price = {coinname: None, 'error': False}
max_px = None

print(time.time())

def get_px():
        coin_price = client.get_symbol_ticker(symbol=coinname)
        return float(coin_price['price'])

def get_free_balance():
        balance = client.get_asset_balance(asset=asset)
        return float(balance['free'])

while True:
        # error check to make sure WebSocket is working
        try:
                # 此程序唯一缺点，币安限制,get_px() 一分钟只能拿1200次，我们大概十几秒用完，但我觉得足够。
                price = get_px()
                time = datetime.now().strftime('%H:%M:%S')

                print("{0} cur px: {1}".format(time, price))
                if max_px is None or max_px < price:
                        max_px = price
                if price <= max_px*0.9:
                        # sell all
                        free_qty = get_free_balance()
                        if free_qty > 0:
                                buy_order = client.create_order(symbol=coinname, side='SELL', type='MARKET', quantity=free_qty)
                                print("10% down. Selling all and quit...")
                        break

                if price < 5:
                        try:
                                buy_order = client.create_order(symbol=coinname, side='BUY', type='MARKET', quantity=buy_qty)
                                print("buy order created.")
                        except BinanceAPIException as e:
                                # error handling goes here
                                print(e)
                        except BinanceOrderException as e:
                                # error handling goes here
                                print(e)
        except BinanceAPIException as e:
                print(e)
