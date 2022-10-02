import datetime
import time

import matplotlib.pyplot as plt


import backtrader as bt
import yfinance as yf
import pandas as pd

import BotConfig
from BotConfig import BotConfig
from BotProfitHistory import BotProfitHistory
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
is_not_divisible = "is_not_divisible"
dec_p = "decimal_places"

cn = "coin_name"
start_date = "start_date"
end_date = "end_date"
has_file = False
file_path = "none"

override_start_date = ''#'2022-01-01'
override_end_date = ''#'2022-05-01'

test_bots = []
test_coins = []

take_profits = [0.25, 0.8, 1, 1.25, 2, 3, 4, 5, 10, 15, 20]#, 30, 50, 100]

btc_coin   = {cn: "BTC-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: True,  file_path: "btcusd-f"}
eth_coin   = {cn: "ETH-USD",    start_date: '2022-08-09', end_date: '2022-09-26', is_not_divisible: False, has_file: True,  file_path: "ethusd-f"}
ada_coin   = {cn: "ADA-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: True,  file_path: "adausd-f"}
ftm_coin   = {cn: "FTM-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: True,  has_file: True,  file_path: "ftmusd-f"}
xrp_coin   = {cn: "XRP-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: True,  file_path: "xrpusd-f"}
dot_coin   = {cn: "DOT-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: True,  file_path: "dotusd-f"}
doge_coin  = {cn: "DOGE-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: True,  file_path: "dogeusd-f"}
sol_coin   = {cn: "SOL-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: True,  file_path: "solusd-f"}
near_coin  = {cn: "NEAR-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: True,  has_file: True,  file_path: "nearusd-f"}
enj_coin   = {cn: "ENJ-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: True,  file_path: "enjusd-f"}
bnb_coin   = {cn: "BNB-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
trx_coin   = {cn: "TRX-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
matic_coin = {cn: "MATIC-USD",  start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
lite_coin  = {cn: "LTC-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
cro_coin   = {cn: "CRO-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
leo_coin   = {cn: "LEO-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
ftt_coin   = {cn: "FTT-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
uni_coin   = {cn: "UNI1-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
link_coin  = {cn: "LINK-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
xlm_coin   = {cn: "XLM-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
atom_coin  = {cn: "ATOM-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
algo_coin  = {cn: "ALGO-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
flow_coin  = {cn: "FLOW-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
xmr_coin   = {cn: "XMR-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
ape_coin   = {cn: "APE-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
mana_coin  = {cn: "MANA-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: True,  has_file: False, file_path: "none"}
hbar_coin  = {cn: "HBAR-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
vet_coin   = {cn: "VET-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
icp_coin   = {cn: "ICP-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
egld_coin  = {cn: "EGLD-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
fil_coin   = {cn: "FIL-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
xtz_coin   = {cn: "XTZ-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
sand_coin  = {cn: "SAND-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
mkr_coin   = {cn: "MKR-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
zec_coin   = {cn: "ZEC-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
theta_coin = {cn: "THETA-USD",  start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
grp_coin   = {cn: "GRT-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
eos_coin   = {cn: "EOS-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
kcs_coin   = {cn: "KCS-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
axs_coin   = {cn: "AXS-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
cake_coin  = {cn: "CAKE-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
aave_coin  = {cn: "AAVE-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
hnt_coin   = {cn: "HNT-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
rune_coin  = {cn: "RUNE-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
klay_coin  = {cn: "KLAY-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
ht_coin    = {cn: "HT-USD",     start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
btt_coin   = {cn: "BTT-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
miota_coin = {cn: "MIOTA-USD",  start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
gmt_coin   = {cn: "GMT-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
qnt_coin   = {cn: "QNT-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
#xec_coin   = {cn: "XEC-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none}
okb_coin   = {cn: "OKB-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
nexo_coin  = {cn: "NEXO-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
neo_coin   = {cn: "NEO-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
stx_coin   = {cn: "STX-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
waves_coin = {cn: "WAVES-USD",  start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
chz_coin   = {cn: "CHZ-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
cvx_coin   = {cn: "CVX-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
celo_coin  = {cn: "CELO-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
gala_coin  = {cn: "GALA-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
dash_coin  = {cn: "DASH-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
zil_coin   = {cn: "ZIL-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
crv_coin   = {cn: "CRV-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
lrc_coin   = {cn: "LRC-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
ksm_coin   = {cn: "KSM-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
bat_coin   = {cn: "BAT-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
xdc_coin   = {cn: "XDC-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
one_coin   = {cn: "ONE-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
paxg_coin  = {cn: "PAXG-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
gno_coin   = {cn: "GNO-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
amp_coin   = {cn: "AMP-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
kda_coin   = {cn: "KDA-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
mina_coin  = {cn: "MINA-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
ar_coin    = {cn: "AR-USD",     start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
comp_coin  = {cn: "COMP1-USD",  start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
xem_coin   = {cn: "XEM-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
dcr_coin   = {cn: "DCR-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
hot_coin   = {cn: "HOT-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
ldo_coin   = {cn: "LDO-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
kava_coin  = {cn: "KAVA-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
gt_coin    = {cn: "GT-USD",     start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
qtum_coin  = {cn: "QTUM-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
fei_coin   = {cn: "FEI-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
bnt_coin   = {cn: "BNT-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
oinch_coin = {cn: "1INCH-USD",  start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
xym_coin   = {cn: "XYM-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
fet_coin   = {cn: "FET-USD",    start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: True,  has_file: False, file_path: "none"}
ankr_coin  = {cn: "ANKR-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: False, has_file: False, file_path: "none"}
shib_coin  = {cn: "SHIB-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: True,  has_file: False, file_path: "none"}
ctsi_coin  = {cn: "CTSI-USD",   start_date: '2022-01-01', end_date: '2022-05-01', is_not_divisible: True,  has_file: False, file_path: "none"}


phillipe_dev     = {bn: "phillipe_dev",        bo: 10.00, so: 10.00, sos: 0.9,  os: 1.35, ss: 1.15, mstc: 17,  p_mstc: 17,  risk: 100, dec_p: 4}
phillipe_025_bot = {bn: "Phillipe 0.25",       bo: 10.00, so: 20.00, sos: 0.98, os: 1.48, ss: 1.11, mstc: 11,  p_mstc: 11,  risk: 100, dec_p: 4}
sixtynineer      = {bn: "69ER",                bo: 11.00, so: 11.00, sos: 1.89, os: 0.85, ss: 1.05, mstc: 18,  p_mstc: 18,  risk: 100, dec_p: 4}
oni_aggressive   = {bn: "Oni Agrressive",      bo: 50.00, so: 50.00, sos: 1,    os: 1.4,  ss: 1.45, mstc: 10,  p_mstc: 10,  risk: 100, dec_p: 4}
phillipe_bot     = {bn: "Phillipe",            bo: 10.00, so: 18.00, sos: 1.42, os: 1.56, ss: 1.23, mstc: 10,  p_mstc: 10,  risk: 100, dec_p: 4}
ta_bot           = {bn: "TA standard",         bo: 10.00, so: 20.00, sos: 2,    os: 1.05, ss: 1,    mstc: 30,  p_mstc: 30,  risk: 100, dec_p: 4}
banshee          = {bn: "banshee",             bo: 28.20, so: 28.20, sos: 1.5,  os: 1.4,  ss: 1.13, mstc: 8,   p_mstc: 8,   risk: 100, dec_p: 4}
Gorgon           = {bn: "Gorgon",              bo: 25.00, so: 25.00, sos: 1.6,  os: 1.2,  ss: 1.13, mstc: 12,  p_mstc: 12,  risk: 100, dec_p: 4}
chimera          = {bn: "chimera",             bo: 14.00, so: 14.00, sos: 1.6,  os: 1.2,  ss: 1.11, mstc: 15,  p_mstc: 15,  risk: 100, dec_p: 4}
aqrabua          = {bn: "aqrabua",             bo: 10.00, so: 10.00, sos: 1.0,  os: 1.4,  ss: 1.26, mstc: 12,  p_mstc: 12,  risk: 100, dec_p: 4}
mars_bot         = {bn: "Mars",                bo: 10.00, so: 10.00, sos: 1.8,  os: 1.4,  ss: 1.3,  mstc: 10,  p_mstc: 10,   risk: 100, dec_p: 4}
oni_bot          = {bn: "Oni",                 bo: 10.00, so: 10.00, sos: 1,    os: 1.4,  ss: 1.45, mstc: 10,  p_mstc: 10,   risk: 100, dec_p: 4}


def set_test_coins():
    test_coins.append(ada_coin)
    test_coins.append(ftm_coin)
    test_coins.append(xrp_coin)
    test_coins.append(near_coin)
    test_coins.append(sol_coin)
    test_coins.append(dot_coin)
    test_coins.append(doge_coin)
    test_coins.append(enj_coin)
    test_coins.append(eth_coin)
    test_coins.append(btc_coin)
    #test_coins.append(bnb_coin)
    #test_coins.append(trx_coin)
    #test_coins.append(matic_coin)
    #test_coins.append(lite_coin)
    #test_coins.append(cro_coin)
    #test_coins.append(leo_coin)
    #test_coins.append(ftt_coin)
    #test_coins.append(uni_coin)
    #test_coins.append(link_coin)
    #test_coins.append(xlm_coin)
    #test_coins.append(atom_coin)
    #test_coins.append(algo_coin)
    #test_coins.append(flow_coin)
    #test_coins.append(xmr_coin)
    #test_coins.append(ape_coin)
    #test_coins.append(mana_coin)
    #test_coins.append(hbar_coin)
    #test_coins.append(vet_coin)
    #test_coins.append(icp_coin)
    #test_coins.append(egld_coin)
    #test_coins.append(fil_coin)
    #test_coins.append(xtz_coin)
    #test_coins.append(sand_coin)
    #test_coins.append(mkr_coin)
    #test_coins.append(zec_coin)
    #test_coins.append(theta_coin)
    #test_coins.append(grp_coin)
    #test_coins.append(eos_coin)
    #test_coins.append(kcs_coin)
    #test_coins.append(axs_coin)
    #test_coins.append(cake_coin)
    #test_coins.append(aave_coin)
    #test_coins.append(hnt_coin)
    #test_coins.append(rune_coin)
    #test_coins.append(klay_coin)
    #test_coins.append(ht_coin)
    #test_coins.append(btt_coin)
    #test_coins.append(miota_coin)
    #test_coins.append(gmt_coin)
    #test_coins.append(qnt_coin)
    ##test_coins.append(xec_coin)
    #test_coins.append(okb_coin)
    #test_coins.append(nexo_coin)
    #test_coins.append(neo_coin)
    #test_coins.append(stx_coin)
    #test_coins.append(waves_coin)
    #test_coins.append(chz_coin)
    #test_coins.append(cvx_coin)
    #test_coins.append(celo_coin)
    #test_coins.append(gala_coin)
    #test_coins.append(dash_coin)
    #test_coins.append(zil_coin)
    #test_coins.append(crv_coin)
    #test_coins.append(lrc_coin)
    #test_coins.append(ksm_coin)
    #test_coins.append(bat_coin)
    #test_coins.append(xdc_coin)
    #test_coins.append(one_coin)
    #test_coins.append(paxg_coin)
    #test_coins.append(gno_coin)
    #test_coins.append(amp_coin)
    #test_coins.append(kda_coin)
    #test_coins.append(mina_coin)
    #test_coins.append(ar_coin)
    #test_coins.append(comp_coin)
    #test_coins.append(xem_coin)
    #test_coins.append(dcr_coin)
    #test_coins.append(hot_coin)
    #test_coins.append(ldo_coin)
    #test_coins.append(kava_coin)
    #test_coins.append(gt_coin)
    #test_coins.append(qtum_coin)
    #test_coins.append(fei_coin)
    #test_coins.append(bnt_coin)
    #test_coins.append(oinch_coin)
    #test_coins.append(xym_coin)
    #test_coins.append(fet_coin)
    #test_coins.append(ankr_coin)
    ##test_coins.append(shib_coin)
    #test_coins.append(ctsi_coin)


def set_test_bots():
    test_bots.append(phillipe_dev)
    test_bots.append(phillipe_025_bot)
    test_bots.append(sixtynineer)
    test_bots.append(oni_aggressive)
    test_bots.append(phillipe_bot)
    test_bots.append(ta_bot)
    test_bots.append(banshee)
    test_bots.append(Gorgon)
    test_bots.append(chimera)
    test_bots.append(aqrabua)
    test_bots.append(mars_bot)


def run_test_bots(bot_ph):
    for coin in test_coins:
        print("getting data for coin... {}".format(coin[cn]))
        df = get_data_from_api(coin)
        for bot in test_bots:
            for take_profit in take_profits:
                bot_config = create_config(bot, coin, take_profit)
                run_dca_bot(config=bot_config, dfData=df, bot_profit_history=bot_ph)


def get_data_from_api(coin):
    sd = coin[start_date]
    ed = coin[end_date]
    if override_start_date != "":
        sd = override_start_date

    if override_end_date != "":
        ed = override_end_date
    if not coin[has_file]:
        print("NO FILE")
        return yf.download(coin[cn], start=sd, end=ed)

    pathfile = '../Historical_Data/test_coins/' + coin[file_path] + '.csv'
    print("Coin Path: ", pathfile)
    print("")

    # Wednesday, 9 March 2016 16:04:00
    # Sunday, 18 September 2016 19:37:00


    data = (bt.feeds.GenericCSVData(
        dataname=pathfile,
        headers=True,
        dtformat=lambda x: datetime.datetime.utcfromtimestamp(float(x) / 1000.0),
        timeframe=bt.TimeFrame.Minutes,
        compression=1,
        fromdate=datetime.datetime(2022, 1, 1),
        todate=datetime.datetime(2022, 12, 31),
        nullvalue=0.0,
        datetime=0,
        open=1,
        close=2,
        high=3,
        low=4,
        volume=5,
        openinterest=-1

    ))

    return data

def create_config(bot, coin, take_profit):
    return BotConfig(coin_name=coin[cn],
                     config_bot_name=bot[bn],
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
                     is_coin_token=coin[is_not_divisible],
                     is_multi_bot=True)


def run_dca_bot(config, coin=None, start_date=None, end_date=None, dfData=None, bot_profit_history=None):
    initial_BR = 200000
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(initial_BR)
    #feed = bt.feeds.PandasData(dataname=dfData)

    #print(dfData.keys())

    #feed = bt.feeds.PandasData(dataname=dfData)

    cerebro.broker.set_coc(False)
    cerebro.broker.set_coo(False)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.adddata(dfData)
    cerebro.addstrategy(DCAStrat, config=config, bot_history=bot_profit_history)
    cerebro.run()

    #ENABLE PLOT HERE
    # plt.rcParams['figure.dpi'] = 100
    # plt.rcParams['figure.figsize'] = [20, 12]
    # plt.rcParams['figure.figsize'] = [10, 8]
    # cerebro.plot(style='candlestick', height=3000, width=3000, dpi=10000)

if __name__ == "__main__":
    print("Starting application....", time.ctime(time.time()))
    bot_profit_history = BotProfitHistory()
    set_test_coins()
    set_test_bots()
    run_test_bots(bot_profit_history)
    bot_profit_history.print_profits()
