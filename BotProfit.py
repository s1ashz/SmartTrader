from objprint import add_objprint


@add_objprint
class BotProfit:
    # coin = None
    # total_bot_profit = None
    # daily_roi = None
    # total_roi = None
    # total_bot_cost = None
    # config_risk_value = None
    # bot_risk_surpassed_times = None
    # bot_extra_mstc_reached_times = None
    # bot_number = None

    def __init__(self,
                 coin=None,
                 bot_name=None,
                 total_bot_profit=None,
                 daily_roi=None,
                 total_roi=None,
                 total_bot_cost=None,
                 config_risk_value=None,
                 bot_risk_surpassed_times=None,
                 bot_extra_mstc_reached_times=None,
                 profit_if_bot_money_invested=None,
                 bar_count=None,
                 bot_number=None,
                 bot_config=None,
                 ):
        self.coin = coin
        self.bot_name = bot_name
        self.total_bot_profit = total_bot_profit
        self.daily_roi = daily_roi
        self.total_roi = total_roi
        self.total_bot_cost = total_bot_cost
        self.config_risk_value = config_risk_value
        self.bot_risk_surpassed_times = bot_risk_surpassed_times
        self.bot_extra_mstc_reached_times = bot_extra_mstc_reached_times
        self.bar_count = bar_count
        self.bot_number = bot_number
        self.profit_if_bot_money_invested = profit_if_bot_money_invested
        self.bot_config = bot_config
