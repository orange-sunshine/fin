import numpy as np

import subprocess

rc = subprocess.call("./alpaca.sh")


#from zipline.api import order_target, record, symbol

import alpaca_trade_api as tradeapi
#api = tradeapi.REST()
#api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL)
api = tradeapi.REST()

# Get daily price data for AAPL over the last 5 trading days.
barset = api.get_barset('AAPL', 'day', limit=5)
aapl_bars = barset['AAPL']

print(barset)

# See how much AAPL moved in that timeframe.
week_open = aapl_bars[0].o
week_close = aapl_bars[-1].c
percent_change = (week_close - week_open) / week_open * 100
print('AAPL moved {}% over the last 5 days'.format(percent_change))

account = api.get_account()
print(account)

def setup():
	api = tradeapi.REST()
	account = api.get_account()

def model():
	pass

def trades():
	'''
	Buy all stocks at beginning of day and sell at end of day
	'''
	portfolio = ['AAPL']

	for stock in portfolio:
		print('Stock purchased')
		api.submit_order(
		    symbol=stock,
		    qty=1,
		    side='buy',
		    type='market',
		    time_in_force='gtc'
		)


def portfolio():
	portfolio = api.list_positions()
	print("Viewing positions")
	print(portfolio)
	for position in portfolio:
		print("{} shares of {}".format(position.qty, position.symbol))

def backtesting():
	pass

trades()
portfolio()
'''
References
https://www.youtube.com/watch?v=GsGeLHTOGAg
https://github.com/quantopian/pyfolio
https://github.com/quantopian/zipline
Executing bash script in python
https://www.kite.com/python/answers/how-to-execute-a-bash-script-in-python

'''