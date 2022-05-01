import datetime
import backtrader as bt
import yfinance as yf

from DCAStrat import DCAStrat

initial_BR = 10000
cerebro = bt.Cerebro()
cerebro.broker.setcash(initial_BR)

df = yf.download('FTM-USD', start='2021-10-10')#, end='2022-04-01')
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
#print("Final Portfolio Value %.2f" % cerebro.broker.getvalue())
#print("Final Profit: {}".format(cerebro.broker.getvalue() - initial_BR))
#print("Final Profit: {}".format(cerebro.broker.cash + 10))

#cerebro.plot(style='candlestick')