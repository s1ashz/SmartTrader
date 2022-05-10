import datetime
import backtrader as bt
import matplotlib.pyplot as plt

import yfinance as yf

from BotConfig import BotConfig
from DCAStrat import DCAStrat


# ONI  bo: 10.00, so: 10.00, sos: 1,    os: 1.4,  ss: 1.45, mstc: 8,  p_mstc: 9,  risk: 100, dec_p: 4}
# Mars bo: 10.00, so: 10.00, sos: 1.8,  os: 1.4, ss: 1.3,   mstc: 9,  p_mstc: 8,  risk: 100, dec_p: 4}

# bo: 10.00, so: 10.00, sos: 1,    os: 1.4,  ss: 1.45, mstc: 9,  p_mstc: 8,  risk: 100, dec_p: 4}

taStandardConfig = BotConfig(config_name="Trade alts standard",
                             order_tp=10,
                             base_order_volume=10.00,
                             safety_order_volume=10.00,
                             order_safety_sos=1,
                             order_volume_scale=1.4,
                             order_step_scale=1.45,
                             mstc=9,
                             profit_mstc=8,
                             risk_value=100,
                             is_coin_token=True, # TODO: CAREFUL coping configs
                             round_decimal=4)

initial_BR = 20000
cerebro = bt.Cerebro()
cerebro.broker.setcash(initial_BR)

df = yf.download('NEAR-USD', start='2022-01-01' , end='2022-05-01')
print(df.keys())

feed = bt.feeds.PandasData(dataname=df)

cerebro.broker.set_coc(False)
cerebro.broker.set_coo(False)
cerebro.broker.setcommission(commission=0.001)
cerebro.adddata(feed)
cerebro.addstrategy(DCAStrat, config=taStandardConfig)

print("Starting Portfolio Value %.2f" % cerebro.broker.getvalue())
cerebro.run()
print("")
# TODO: TRY TO CALCULATE BOT PROFFIT WITH BROKER INFORMATION
# print("Final Portfolio Value %.2f" % cerebro.broker.getvalue())
# print("Final Profit: {}".format(cerebro.broker.getvalue() - initial_BR))
# print("Final Profit: {}".format(cerebro.broker.cash + 10))

plt.rcParams['figure.dpi'] = 100
# plt.rcParams['figure.figsize'] = [20, 12]
plt.rcParams['figure.figsize'] = [10, 8]

#cerebro.plot(style='candlestick', height=3000, width=2000, dpi=10000)


# fig = cerebro.plot(numfigs = num, barupfill = False, bardownfill = False, style = 'candle', plotdist = 0.5,
# figsize=(30,30), volume = False, barup = 'green', valuetags = False, subtxtsize = 7,
# start = startdate, end = enddate)
