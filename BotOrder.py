from objprint import add_objprint


@add_objprint
class BotOrder():

    order_avg_price = None

    order_price = None
    order_incremented_ss = None
    order_total_ss = None
    order_size = None
    order_iteration_volume = None
    order_volume = None
    order_status = None
    order_cumulative_volume = None
    order_cumulative_size = None

    def __init__(self,order_avg_price=None, order_volume=None, order_iteration_volume=None, order_cumulative_volume=None, order_price=None, order_cumulative_size=None, order_size=None, order_status=None, order_incremented_ss=None, order_total_ss=None):
        self.order_avg_price = order_avg_price
        self.order_price = order_price
        self.order_incremented_ss = order_incremented_ss
        self.order_total_ss = order_total_ss
        self.order_cumulative_size = order_cumulative_size
        self.order_size = order_size
        self.order_iteration_volume = order_iteration_volume
        self.order_volume = order_volume
        self.order_cumulative_volume = order_cumulative_volume
        self.order_status = order_status
