import datetime
import backtrader as bt
import yfinance as yf

from DCAStrat import DCAStrat

initial_BR = 355
cerebro = bt.Cerebro()
cerebro.broker.setcash(initial_BR)

df = yf.download('FTM-USD', start='2022-01-20', end='2022-01-21')
print(df.keys())

feed = bt.feeds.PandasData(dataname=df)

cerebro.broker.set_coc(False)
cerebro.broker.set_coo(False)
cerebro.adddata(feed)
cerebro.addstrategy(DCAStrat)

print("Starting Portfolio Value %.2f" % cerebro.broker.getvalue())
cerebro.run()
print("")
print("Final Portfolio Value %.2f" % cerebro.broker.getvalue())
print("Final Profit: {}".format(cerebro.broker.getvalue() - initial_BR))

#cerebro.plot(style='candlestick')