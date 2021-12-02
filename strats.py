# import modules
from datetime import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
import torch


def dummy():
    # initialize parameters
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2021, 1, 1)
    
    # get the data
    data = yf.download('SPY', start = start_date,
                    end = end_date)
    
    # display as line chart
    plt.figure(figsize = (20,10))
    plt.title('Opening Prices from {} to {}'.format(start_date,
                                                    end_date))
    plt.plot(data['Open'])
    plt.show()

    #display as candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'])])
    fig.show()

def strategy1(data):
    '''
    Buy if the prev day returns 0-0.5
    '''
    trend = []
    currtrend = []
    prevtrend = []
    ftrtrend = []
    negtrend = []
    prev = 1
    prevgrowth = 1
    for index, row in data.iterrows():
        #print(row["Open"])
        growth = row["Open"]/prev
        growth = growth*100 - 100
        
        prev = row["Open"]
        trend.append(growth)
        if growth > 1:
            #print(growth)
            currtrend.append(growth)
            prevtrend.append(prevgrowth)
        if prevgrowth < 0 :
            #print(growth)
            #negtrend.append((prevgrowth, growth))
            negtrend.append(growth)
            #prevtrend.append(prevgrowth)
        if prevgrowth > 1:
            ftrtrend.append(growth)

        prevgrowth = growth
    #print(trend)
    #print(currtrend)
    #print(sum(currtrend[1:]))
    #print(prevtrend)
    #print(sum(prevtrend[2:]))
    #print(ftrtrend)
    #print(sum(ftrtrend))
    print(negtrend)
    print(sum(negtrend[1:]))
    return negtrend

def strategy2(data):
    '''
    Buy stock if stock increases two days in a row

    Todo: Keep track of data
    '''
    trend = []
    currtrend = []
    prev1 = 1
    pgrowth1 = 1
    pgrowth2 = 1
    for _, row in data.iterrows():
        growth = (row["Open"]/prev1) * 100 - 100
        prev1 = row["Open"]
        trend.append(growth)

        if pgrowth1 > 0 and pgrowth2 > 0:
            currtrend.append((growth, pgrowth1, pgrowth2))

        pgrowth2 = pgrowth1
        pgrowth1 = growth

    out = []
    for i in currtrend:
        out.append(i[0])

    print(currtrend)
    print(sum(out[1:]))
    return out

def portfolio(stocks, strategy):
    crossdata = []
    for stock in stocks:
        data = yf.download(tickers=stock, period='50d', interval='1d')
        out = strategy(data)
        if out: 
            crossdata.append(out)

class LinearRegressionModel(torch.nn.Module):
 
    def __init__(self):
        super(LinearRegressionModel, self).__init__()
        self.linear = torch.nn.Linear(1, 1)  # One in and one out
 
    def forward(self, x):
        y_pred = self.linear(x)
        return y_pred



'''
References

https://stackoverflow.com/questions/68331065/json-decode-error-with-yfinance-jsondecodeerror-expecting-value-line-1-column
https://stackoverflow.com/questions/30101369/how-can-i-print-out-just-the-index-of-a-pandas-dataframe
https://towardsdatascience.com/algorithmic-trading-bot-python-ab8f42c37145

Crypto Bot Scam
https://towardsdatascience.com/crypto-trading-bots-a-helpful-guide-for-beginners-60decb40e434

Linear Regression
https://www.geeksforgeeks.org/linear-regression-using-pytorch/

'''