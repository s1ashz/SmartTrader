import datetime
import backtrader as bt
import matplotlib.pyplot as plt

import yfinance as yf

from DCAStrat import DCAStrat

initial_BR = 20000
cerebro = bt.Cerebro()
cerebro.broker.setcash(initial_BR)

df = yf.download('DNT-USD', start='2022-04-11')#, end='2022-05-01')
print(df.keys())

feed = bt.feeds.PandasData(dataname=df)

cerebro.broker.set_coc(False)
cerebro.broker.set_coo(False)
cerebro.broker.setcommission(commission=0.001)
cerebro.adddata(feed)
cerebro.addstrategy(DCAStrat)

print("Starting Portfolio Value %.2f" % cerebro.broker.getvalue())
cerebro.run()
print("")
# TODO: TRY TO CALCULATE BOT PROFFIT WITH BROKER INFORMATION
# print("Final Portfolio Value %.2f" % cerebro.broker.getvalue())
# print("Final Profit: {}".format(cerebro.broker.getvalue() - initial_BR))
# print("Final Profit: {}".format(cerebro.broker.cash + 10))

plt.rcParams['figure.dpi'] = 100
plt.rcParams['figure.figsize'] = [20, 12]

#cerebro.plot(style='candlestick', height=3000, width=2000, dpi=10000)


# fig = cerebro.plot(numfigs = num, barupfill = False, bardownfill = False, style = 'candle', plotdist = 0.5,
# figsize=(30,30), volume = False, barup = 'green', valuetags = False, subtxtsize = 7,
# start = startdate, end = enddate)
