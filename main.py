import backtrader as bt
import yfinance as yf

from TestStrategy import TestStrat, Omg

cerebro = bt.Cerebro()


df = yf.download('DNT-USD', start='2022-01-01')  # , end='2022-02-01')
print(df.keys())

feed = bt.feeds.PandasData(dataname=df)

cerebro.broker.set_coc(False)
cerebro.broker.set_coo(False)
cerebro.adddata(feed)


TestStrat

cerebro.addstrategy(TestStrat, config=Omg("puta"))

cerebro.run()