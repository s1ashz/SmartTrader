from objprint import add_objprint


@add_objprint
class BotProfitHistory:

    def __init__(self):
        self.excel_print = True
        self.bot_profit_history = {}
        self.bot_coins = []
        self.coin_take_profits = []

    def add_profit(self, bot_profit):
        if not self.bot_profit_history.__contains__(bot_profit.coin):
            self.bot_profit_history[bot_profit.coin] = {}

        if not self.bot_profit_history[bot_profit.coin].__contains__(bot_profit.bot_config.config_order_tp):
            self.bot_profit_history[bot_profit.coin][bot_profit.bot_config.config_order_tp] = []

        self.bot_profit_history[bot_profit.coin][bot_profit.bot_config.config_order_tp].append(bot_profit)

    def print_profits(self):
        print(",".join(self.bot_profit_history.keys()))
        print("Bot, Coin, TP, Profit, Daily ROI, ROI, Bot Cost, Risk, Nº>risk, Nº>mstc, bot_numb")
        for coin, coin_bots in self.bot_profit_history.items():
            print("")
            print("'============ {} ============".format(coin))
            for take_profit, bot_all_take_profits in coin_bots.items():
                print("")
                for bot in bot_all_take_profits:
                    tp = (bot.bot_config.config_order_tp - 1) * 100
                    daily_roi = ((bot.total_bot_profit / bot.bar_count) / bot.total_bot_cost) * 100
                    total_roi = (bot.total_bot_profit / bot.total_bot_cost) * 100
                    str = "Bot: {:13}, Coin: {:8}, TP:{:6.2f}%, Profit:{:7.2f}, Daily ROI:{:4.2f}%, ROI:{:5.2f}%, Bot Cost:{:6.2f}, Risk:{}, Nº>risk:{}, Nº>mstc:{}, bot_numb:{:3}"
                    if self.excel_print:
                        excelStr = "{:13},{:8},{:6.2f}%,{:7.2f},{:4.2f}%,{:5.2f}%,{:6.2f},{},{},{},{:3}"
                        str = excelStr

                    risk_value = bot.config_risk_value * 100
                    print(str.format(bot.bot_name,
                                     coin,
                                     tp,
                                     bot.total_bot_profit,
                                     daily_roi,
                                     total_roi,
                                     bot.total_bot_cost,
                                     risk_value,
                                     bot.bot_risk_surpassed_times,
                                     bot.bot_extra_mstc_reached_times,
                                     bot.bot_number,
                                     ))
