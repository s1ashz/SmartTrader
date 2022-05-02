from objprint import add_objprint


@add_objprint
class BotOrder():
    order_price = None
    order_ss = None
    order_size = None
    order_volume = None
    order_status = None

    def __init__(self, order_volume=None, order_price=None, order_size=None, order_status=None, order_ss=None):
        self.order_price = order_price
        self.order_ss = order_ss
        self.order_size = order_size
        self.order_volume = order_volume
        self.order_status = order_status
