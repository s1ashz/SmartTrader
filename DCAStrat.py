import backtrader as bt

from BotOrder import BotOrder
from BotStatus import BotStatus


class DCAStrat(bt.Strategy):
    my_orders = []
    map_bot_orders = {}

    config_base_order_volume = 10.00
    config_safety_order_volume = 10.00
    config_order_tp = 1.02
    config_order_safety_sos = 0.01
    config_order_volume_scale = 1.4
    config_order_step_scale = 1.45
    config_mstc = 8

    is_bot_active = False

    current_avg_buy = None
    current_size = None
    current_tp = None

    def reset_current_status(self):
        self.current_avg_buy = None
        self.current_size = None
        self.current_tp = None
        self.my_orders = []
        self.map_bot_orders = {}

    bar_count = 0

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        print("start...")

    def next(self):
        try:
            next_bar = self.data.close[1]
        except IndexError:
            return
        self.bar_count += 1
        # for x in self.map_bot_orders.values():
        # print(str(x))
        if self.bar_count > 1161:
            return
        print(">Next Bar {}:low {}, open: {}, close: {}, high {} ".format(self.bar_count, self.data.low[0],
                                                                          self.data.open[0], self.data.close[0],
                                                                          self.data.high[0]))
        if self.bar_count == 1:
            self.start_bot()
            return

        if not self.is_bot_active:
            self.start_bot()
            return

        self.peak_next_bar(self.data)
        self.bar_count += 1

    def start_bot(self):
        print(">start bot...")
        self.update_bot_orders(self.data)
        self.fill_bot_orders()
        self.is_bot_active = True
        self.peak_next_bar(self.data)

    def update_bot_orders(self, data):
        print(">update_bot_orders:")
        base_order = self.create_base_bot_order(data.close[0])
        safety_order = self.create_safety_bot_order(self.config_safety_order_volume, data.close[0])
        self.map_bot_orders["bo"] = base_order
        self.map_bot_orders["so1"] = safety_order
        self.update_current_status(base_order)

        for i in range(2, self.config_mstc + 1):
            safety_order = self.create_safety_bot_order(
                safety_order.order_volume,
                safety_order.order_price,
                ss=self.config_order_step_scale,
                os=self.config_order_volume_scale
            )
            self.map_bot_orders["so{}".format(i)] = safety_order
        # for x in self.map_bot_orders.values():
        # print(str(x))

    def fill_bot_orders(self):
        for order in self.map_bot_orders.values():
            #order_buy = self.buy(exectype=bt.Order.Limit, size=order.order_size, price=order.order_price)
            #self.my_orders.append(order_buy)
            order.order_status = BotStatus.ACCEPTED

    def peak_next_bar(self, data):
        print(">peaking")
        if self.is_bot_active:
            self.check_bar_bottom(data)
            self.check_bar_top(data)

    def check_bar_bottom(self, data):
        changed = False
        for order in self.map_bot_orders.values():
            #print(" check bottom: {} {}".format(order.order_price >= data.low[1], order.order_status == BotStatus.ACCEPTED))
            if (order.order_price >= data.low[1]) and (order.order_status == BotStatus.ACCEPTED):
                order.order_status = BotStatus.FILLED
                order_buy = self.buy(exectype=bt.Order.Limit, size=order.order_size, price=order.order_price)
                self.my_orders.append(order_buy)
                changed = True
        if changed:
            self.calculate_current_status()

    def check_bar_top(self, data):
        print(">check_bar_top {} {}".format(self.is_bot_active, self.current_tp <= data.high[1]))
        if self.current_tp <= data.high[1] and self.is_bot_active:
            self.close_active_orders(data)

    def close_active_orders(self, data):
        self.sell(exectype=bt.Order.Stop, price=self.current_tp, size=self.current_size)
        print("stopping bot.... current_p:{} size: {} ".format(self.current_tp, self.current_size))
        self.is_bot_active = False
        self.reset_current_status()

    def calculate_size(self, order_volume, buy_price):
        shares = (order_volume / buy_price)
        return self.round_down(shares, 5)

    def round_down(self, value, decimals):
        factor = 1 / (10 ** decimals)
        return (value // factor) * factor

    def calculate_safety_order_price(self, price):
        return price * (1 - (self.config_order_safety_order_scale * self.config_order_step_scale))

    def calculate_safety_order_volume(self, volume):
        return volume * self.config_order_volume_scale

    def create_base_bot_order(self, price):
        order_volume = self.config_base_order_volume
        order_price = price
        order_size = self.calculate_size(order_volume, order_price)
        # print("----- base order ------")
        # print("volume: {}, price: {}, size: {} ".format(order_volume, order_price, order_size))
        return BotOrder(order_volume=order_volume,
                        order_price=order_price,
                        order_size=order_size,
                        order_status=BotStatus.PENDING)

    def create_safety_bot_order(self, volume, price, ss=1.00, os=1.00):
        order_volume = volume * os
        order_price = price * (1.00 - (self.config_order_safety_sos * ss))
        order_size = self.calculate_size(order_volume, order_price)
        # print("----- Safety order ------")
        # print("volume: {}, price: {}, size: {} ".format(order_volume, order_price, order_size))
        return BotOrder(order_volume=order_volume,
                        order_price=order_price,
                        order_size=order_size,
                        order_status=BotStatus.PENDING)

    def update_current_status(self, order):
        self.current_tp = order.order_price * self.config_order_tp
        self.current_avg_buy = order.order_price
        self.current_size = order.order_size

    def calculate_current_status(self):
        avg_price_numerator = 0
        avg_price_denominator = 0
        for order in self.map_bot_orders.values():
            if order.order_status == BotStatus.FILLED:
                avg_price_numerator += order.order_price * order.order_size
                avg_price_denominator += order.order_size

        self.current_avg_buy = avg_price_numerator / avg_price_denominator
        self.current_tp = self.current_avg_buy * self.config_order_tp
        self.current_size = avg_price_denominator

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log("BUY EXECUTED ref:{}, price: {} size: {}".format(order.ref, order.executed.price,
                                                                          order.executed.size))
            elif order.issell():
                self.log("SELL EXECUTED ref:{}, price: {} size: {}".format(order.ref, order.executed.price,
                                                                          order.executed.size))

        elif order.status in [order.Canceled]:
            self.log("ORDER CANCELLED")

    def _stop(self):
        print("------------ DONE ------------")
        print(self.position)
        print(self.position.price)
        print(self.position.size)
        print("=========")
        print("avg: {}, TP: {}, size: {}".format(self.current_avg_buy, self.current_tp, self.current_size))
        # print(len(self.my_orders))
        for x in self.my_orders:
            # print("{} - {} - {}".format(str(x.price), x.size, x.Status[x.status]))
            print(str(x.Status[x.status]))
        # print(self.orders_executed[1])
