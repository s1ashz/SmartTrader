import backtrader as bt
import yfinance as yf

import BotConfig
from BotConfig import BotConfig
from DCAStrat import DCAStrat

bn = "bot_name"
tp = "tp"
bo = "bo"
so = "so"
sos = "sos"
os = "os"
ss = "ss"
mstc = "mstc"
p_mstc = "profit_mstc"
risk = "risk"
is_coin = "is_coin"
dec_p = "decimal_places"

test_bots = []

take_profits = [1, 1.25, 2, 3, 4, 5, 10, 15, 20]
ta_bot = {bn: "Trade alts standard", bo: 10.00, so: 20.00, sos: 2, os: 1.05, ss: 1, mstc: 30, p_mstc: 30, risk: 100,
          is_coin: True, dec_p: 4}


def run_dca_bot(config, coin=None, start_date=None, end_date=None):
    coin = 'FTM-USD'
    start_date = '2022-01-01'
    df = yf.download(coin, start=start_date)  # , end='2022-02-01')
    initial_BR = 200000
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(initial_BR)
    feed = bt.feeds.PandasData(dataname=df)
    cerebro.broker.set_coc(False)
    cerebro.broker.set_coo(False)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.adddata(feed)
    cerebro.addstrategy(DCAStrat, config=config)
    print("\n=========================  {}  ===============================".format(config.config_name))
    print("Running Coin: {} bot {} with tp {} from {} to {} \n".format(coin, config.config_name, config.config_order_tp, start_date, end_date))
    cerebro.run()

def set_test_bots():
    test_bots.append(ta_bot)


def run_test_bots():
    for bot in test_bots:
        for tp in take_profits:
            bot_config = create_config(bot, tp)
            run_dca_bot(config=bot_config)


def create_config(bot, tp):
    return BotConfig(config_name=bot[bn],
                     order_tp=tp,
                     base_order_volume=bot[bo],
                     safety_order_volume=bot[so],
                     order_safety_sos=bot[sos],
                     order_volume_scale=bot[os],
                     order_step_scale=bot[ss],
                     mstc=bot[mstc],
                     profit_mstc=bot[p_mstc],
                     risk_value=bot[risk],
                     round_decimal=bot[dec_p],
                     is_coin_token=bot[is_coin])


if __name__ == "__main__":
    print(">main")
    set_test_bots()
    run_test_bots()
