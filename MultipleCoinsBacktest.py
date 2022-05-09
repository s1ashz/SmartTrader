import backtrader as bt
import yfinance as yf

import BotConfig
from BotConfig import BotConfig
from DCAStrat import DCAStrat

bn = "bot_name"
bo = "bo"
so = "so"
sos = "sos"
os = "os"
ss = "ss"
mstc = "mstc"
p_mstc = "profit_mstc"
risk = "risk"
is_token = "is_token"
dec_p = "decimal_places"

cn = "coin_name"
start_date = "start_date"
end_date = "end_date"

override_start_date = '2022-01-01'
override_end_date = '2022-05-01'

test_bots = []
test_coins = []

take_profits = [1, 1.25, 2, 3]#, 3, 4, 5, 10, 15, 20]

btc_coin   = {cn: "BTC-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_token: False}
eth_coin   = {cn: "ETH-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_token: False}
ada_coin   = {cn: "ADA-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_token: False}
sol_coin   = {cn: "SOL-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_token: False}
matic_coin = {cn: "MATIC-USD",  start_date: '2022-01-01', end_date: '2022-05-01', is_token: True}
lrc_coin   = {cn: "LRC-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_token: False}
ftm_coin   = {cn: "FTM-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_token: True}
near_coin  = {cn: "NEAR-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_token: True}
celo_coin  = {cn: "CELO-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_token: False}
one_coin   = {cn: "ONE-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_token: False}
mana_coin  = {cn: "MANA-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_token: True}
fet_coin   = {cn: "FET-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_token: True}
ankr_coin  = {cn: "ANKR-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_token: False}
shib_coin  = {cn: "SHIB-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_token: True}
ctsi_coin  = {cn: "CTSI-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_token: True}
enj_coin   = {cn: "ENJ-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_token: False}
hnt_coin   = {cn: "HNT-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_token: False}
axs_coin   = {cn: "AXS-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_token: False}


ta_bot           = {bn: "Trade alts standard", bo: 10.00, so: 20.00, sos: 2,    os: 1.05, ss: 1,    mstc: 30, p_mstc: 30, risk: 100, dec_p: 4}
mars_bot         = {bn: "Mars",                bo: 10.00, so: 10.00, sos: 1.8,  os: 1.4, ss: 1.3,   mstc: 9,  p_mstc: 8,  risk: 100, dec_p: 4}
oni_bot          = {bn: "Oni",                 bo: 10.00, so: 10.00, sos: 1,    os: 1.4,  ss: 1.45, mstc: 9,  p_mstc: 8,  risk: 100, dec_p: 4}
phillipe_bot     = {bn: "Phillipe",            bo: 10.00, so: 18.00, sos: 1.42, os: 1.56, ss: 1.23, mstc: 10, p_mstc: 10, risk: 100, dec_p: 4}
phillipe_025_bot = {bn: "Phillipe 0.25",       bo: 10.00, so: 20.00, sos: 0.98, os: 1.48, ss: 1.11, mstc: 11, p_mstc: 11, risk: 100, dec_p: 4}



def set_test_coins():
    test_coins.append(btc_coin)
    test_coins.append(eth_coin)
    test_coins.append(ada_coin)
    test_coins.append(sol_coin)
    test_coins.append(matic_coin)
    test_coins.append(lrc_coin)
    test_coins.append(ftm_coin)
    test_coins.append(near_coin)
    test_coins.append(celo_coin)
    test_coins.append(one_coin)
    test_coins.append(mana_coin)
    test_coins.append(fet_coin)
    test_coins.append(ankr_coin)
    #test_coins.append(shib_coin)
    test_coins.append(ctsi_coin)
    test_coins.append(enj_coin)
    test_coins.append(hnt_coin)
    test_coins.append(axs_coin)


def set_test_bots():
    test_bots.append(ta_bot)
    test_bots.append(mars_bot)
    test_bots.append(oni_bot)
    test_bots.append(phillipe_bot)
    test_bots.append(phillipe_025_bot)


def run_test_bots():
    for coin in test_coins:
        df = get_data_from_api(coin)
        for bot in test_bots:
            print("\n=========================  {}  ===============================".format(bot[bn]))
            for take_profit in take_profits:
                bot_config = create_config(bot, coin, take_profit)
                #print("Running Coin: {} bot {} with tp {} from {} to {} \n".format(coin, bot_config, take_profit, coin[start_date],coin[end_date]))
                run_dca_bot(config=bot_config, dfData=df)

def get_data_from_api(coin):
    sd = coin[start_date]
    ed = coin[end_date]
    if override_start_date != "":
        sd = override_start_date

    if override_end_date != "":
        ed = override_end_date
    print("\n******************************************************  {} : {} - {} ******************************************************".format(coin[cn], sd, ed))
    return yf.download(coin[cn], start=sd, end=ed)

def create_config(bot, coin, take_profit):
    return BotConfig(config_name=bot[bn],
                     order_tp=take_profit,
                     base_order_volume=bot[bo],
                     safety_order_volume=bot[so],
                     order_safety_sos=bot[sos],
                     order_volume_scale=bot[os],
                     order_step_scale=bot[ss],
                     mstc=bot[mstc],
                     profit_mstc=bot[p_mstc],
                     risk_value=bot[risk],
                     round_decimal=bot[dec_p],
                     is_coin_token=coin[is_token],
                     is_multi_bot=True)


def run_dca_bot(config, coin=None, start_date=None, end_date=None, dfData=None):
    initial_BR = 200000
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(initial_BR)
    feed = bt.feeds.PandasData(dataname=dfData)
    cerebro.broker.set_coc(False)
    cerebro.broker.set_coo(False)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.adddata(feed)
    cerebro.addstrategy(DCAStrat, config=config)
    cerebro.run()


if __name__ == "__main__":
    print(">main")
    set_test_coins()
    set_test_bots()
    run_test_bots()
