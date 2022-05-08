from objprint import add_objprint


@add_objprint
class BotConfig():
    config_name = None
    config_order_tp = None
    config_base_order_volume = None
    config_safety_order_volume = None
    config_order_safety_sos = None
    config_order_step_scale = None
    config_order_volume_scale = None
    config_mstc = None
    config_profit_mstc = None  # Must always be lower than config_mstc, otherwise it will just give 0

    config_risk_value = None
    config_round_decimal = None
    config_is_coin_token = None

    def __init__(self, config_name=None,
                 order_tp=None,
                 base_order_volume=None,
                 safety_order_volume=None,
                 order_safety_sos=None,
                 order_volume_scale=None,
                 order_step_scale=None,
                 mstc=None,
                 profit_mstc=None,
                 risk_value=1,
                 round_decimal=4,
                 is_coin_token=True):
        self.config_name = config_name
        self.config_order_tp = 1 + (order_tp / 100)
        self.config_base_order_volume = base_order_volume
        self.config_safety_order_volume = safety_order_volume
        self.config_order_safety_sos = order_safety_sos / 100
        self.config_order_step_scale = order_step_scale
        self.config_order_volume_scale = order_volume_scale
        self.config_mstc = mstc
        self.config_profit_mstc = profit_mstc
        self.config_risk_value = risk_value / 100
        self.config_round_decimal = round_decimal
        self.config_is_coin_token = is_coin_token
