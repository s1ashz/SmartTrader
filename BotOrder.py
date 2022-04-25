from objprint import add_objprint


@add_objprint
class BotOrder():
    order_volume = None
    order_price = None
    order_size = None
    order_status = None

    def __init__(self, order_volume=None, order_price=None, order_size=None, order_status=None):
        self.order_volume = order_volume
        self.order_price = order_price
        self.order_size = order_size
        self.order_status = order_status
