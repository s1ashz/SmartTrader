import backtrader as bt

from BotOrder import BotOrder
from BotStatus import BotStatus


class DCAStrat(bt.Strategy):
    my_orders = []
    map_bot_safety_orders = {}
    bot_base_order = None

    config_base_order_volume = 10.00
    config_safety_order_volume = 20.00
    config_order_tp = 1.0138
    #config_order_tp = 1.0213
    config_order_safety_sos = 0.02
    config_order_step_scale = 1
    config_order_volume_scale = 1.05
    config_mstc = 30
    total_bot_cost = 0
    total_bot_profit = 0

    is_bot_active = False

    current_avg_buy = None
    current_size = None
    current_tp = None
    current_ss = None
    current_last_SO_price = None
    current_bot_upnl = None
    current_bot_vol = None
    current_bot_close_price = None

    def __init__(self):
        self.total_bot_cost = self.calculate_bot_total_cost2()
        print("start... total bot cost will be: {}".format(self.total_bot_cost))

    def calculate_bot_total_profit(self, net_profit):
        profit_vals = []
        cost = self.config_base_order_volume
        profit = net_profit - cost
        possible_profit = profit
        profit_vals.append(profit)
        cost += self.config_safety_order_volume
        vol = self.config_safety_order_volume
        while possible_profit > 0:
            possible_profit = net_profit - cost
            vol *= self.config_order_volume_scale
            cost += vol
            profit_vals.append(possible_profit)

        return profit_vals[len(profit_vals) - 2]
        # return profit if len(profit_vals) == 1 else profit_vals[len(profit_vals) - 2]

    def calculate_bot_total_cost2(self):
        vol = self.config_safety_order_volume
        cost = self.config_base_order_volume + self.config_safety_order_volume
        for i in range(1, self.config_mstc):
            vol *= self.config_order_volume_scale
            cost += vol
            print(i, cost)
        return cost

    # TODO:
    # Bot por 1 run parece correcto. Testar para varias trades

    def reset_current_status(self):
        self.current_avg_buy = None
        self.current_size = None
        self.current_tp = None
        self.current_ss = None
        self.current_last_SO_price = None
        self.my_orders = []
        self.map_bot_safety_orders = {}
        self.bot_base_order = None
        self.current_bot_upnl = None
        self.current_bot_vol = None

    bar_count = 0

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def next(self):
        self.bar_count += 1

        if self.bar_count > 1111111:
            return

        try:
            next_bar = self.data.close[1]
            self.current_bot_close_price = self.data.close[1]
        except IndexError:
            return

        if self.bar_count == 1:
            print("\t>>>Next Bar {}:low {}, open: {}, close: {}, high {} ".format(self.bar_count, self.data.low[0],
                                                                                  self.data.open[0], self.data.close[0],
                                                                                  self.data.high[0]))
            self.start_bot(self.data.close[0])

        print("\t>>>Next Bar {}:low {}, open: {}, close: {}, high {} ".format(self.bar_count + 1, self.data.low[1],
                                                                              self.data.open[1], self.data.close[1],
                                                                              self.data.high[1]))

        # if not self.is_bot_active:
        #    self.start_bot(self.data.close[0])
        #    return

        self.peak_next_bar(self.data)

    def start_bot(self, start_price):
        print(">start bot...")
        self.update_bot_orders(start_price)
        self.is_bot_active = True
        self.bot_base_order = self.buy(exectype=bt.Order.StopLimit, size=self.current_size, price=start_price)
        # TODO: FILL BASE ORDER NOW
        # self.fill_bot_orders()
        # self.peak_next_bar(self.data)

    def update_bot_orders(self, start_price):
        print(">update_bot_orders: {}".format(start_price))
        base_order = self.create_base_bot_order(start_price)
        self.bot_base_order = base_order
        self.update_current_status(base_order)
        safety_order = self.create_safety_bot_order(self.config_safety_order_volume, start_price)
        self.map_bot_safety_orders["so1"] = safety_order

        for i in range(2, self.config_mstc + 1):
            safety_order = self.create_safety_bot_order(
                safety_order.order_volume,
                safety_order.order_price,
                ss=self.config_order_step_scale,
                os=self.config_order_volume_scale
            )
            self.map_bot_safety_orders["so{}".format(i)] = safety_order
        # for x in self.map_bot_orders.values():
        # print(str(x))

    def peak_next_bar(self, data):
        print(">peaking")
        if self.is_bot_active:
            if data.close[1] < data.open[1]:
                self.process_red_candle(data)
            else:
                self.process_green_candle(data)

            # self.check_bar_bottom(data)
            # self.check_bar_top(data)

    def process_red_candle(self, data):
        print(">red candle")
        self.check_bar_top(data)
        self.check_bar_bottom(data)

    def process_green_candle(self, data):
        print(">green candle")
        self.check_bar_bottom(data)
        self.check_bar_top(data)

    def check_bar_bottom(self, data):
        print(" check bottom: current_tp: {} price: {} low: {} close: {} high: {}".format(self.current_tp,
                                                                                          self.current_last_SO_price,
                                                                                          data.low[1], data.close[1],
                                                                                          data.high[1]))
        for order in self.map_bot_safety_orders.values():
            if (order.order_price >= data.low[1]) and (order.order_status == BotStatus.PENDING):
                self.fill_bot_safety_order(order)

    def fill_bot_safety_order(self, order):
        order.order_status = BotStatus.FILLED
        order_buy = self.buy(exectype=bt.Order.StopLimit, size=order.order_size, price=order.order_price)
        self.my_orders.append(order_buy)
        self.current_last_SO_price = order.order_price  # TODO: check there is no bug with this approach without < validation
        self.recalculate_current_status()

    def check_bar_top(self, data):
        print(">check_bar_top {} {}".format(self.current_tp <= data.high[1], self.is_bot_active))
        if self.current_tp <= data.high[1] and self.is_bot_active:
            closing_price = self.close_active_orders(data)
            closing_price = self.scalp_bar_top(data, closing_price)
            self.start_bot(closing_price)

    def scalp_bar_top(self, data, closing_price):
        current_tp = closing_price * self.config_order_tp
        while current_tp <= data.high[1]:
            size = self.calculate_size(self.config_base_order_volume, closing_price)
            self.buy(exectype=bt.Order.StopLimit, size=size, price=closing_price)
            self.sell(exectype=bt.Order.StopLimit, price=current_tp, size=size)
            closing_price = current_tp
            current_tp = closing_price * self.config_order_tp
        return closing_price

    def close_active_orders(self, data):
        closing_price = self.current_tp
        self.sell(exectype=bt.Order.StopLimit, price=self.current_tp, size=self.current_size)
        print("stopping bot.... current_p: {} high: {} size: {} ".format(self.current_tp, data.high[1],
                                                                         self.current_size))
        print("Size: {}".format(self.current_size))
        self.reset_current_status()
        return closing_price

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
        order_price = price * (1.00 - self.current_ss)
        order_size = self.calculate_size(order_volume, order_price)
        # print("----- Safety order ------")
        # print("volume: {}, price: {}, size: {} ss {}".format(order_volume, order_price, order_size, self.current_ss))
        self.current_ss = self.current_ss * self.config_order_step_scale
        return BotOrder(order_volume=order_volume,
                        order_price=order_price,
                        order_size=order_size,
                        order_status=BotStatus.PENDING)

    def update_current_status(self, order):
        self.current_tp = order.order_price * self.config_order_tp
        self.current_avg_buy = order.order_price
        self.current_size = order.order_size
        self.current_ss = self.config_order_safety_sos
        self.current_last_SO_price = order.order_price
        self.current_bot_vol = order.order_price * order.order_size
        print("Current TP: {}".format(self.current_tp))

    def recalculate_current_status(self):
        avg_price_numerator = self.bot_base_order.price * self.bot_base_order.size
        avg_price_denominator = self.bot_base_order.size
        self.current_bot_vol = self.config_base_order_volume
        for order in self.map_bot_safety_orders.values():
            if order.order_status == BotStatus.FILLED:
                avg_price_numerator += order.order_price * order.order_size
                avg_price_denominator += order.order_size
                self.current_bot_vol += order.order_price * order.order_size

        self.current_avg_buy = avg_price_numerator / avg_price_denominator
        self.current_tp = self.current_avg_buy * self.config_order_tp
        self.current_size = avg_price_denominator
        self.current_bot_upnl = self.current_bot_vol - (self.current_size * self.current_bot_close_price)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log("BUY EXECUTED ref:{}, price: {} size: {}".format(order.ref, order.executed.price,
                                                                          order.executed.size))
            elif order.issell():
                netProfit = -(order.executed.price * order.executed.size)
                profit = self.calculate_bot_total_profit(netProfit)
                self.total_bot_profit += profit
                self.log(
                    "SELL EXECUTED ref:{}, price: {} size: {} -----> Profit: {}".format(order.ref, order.executed.price,
                                                                                        order.executed.size,
                                                                                        profit))

        elif order.status in [order.Canceled]:
            self.log("ORDER CANCELLED")

    def _stop(self):
        print("------------ DONE ------------")
        print(self.position)
        print(self.position.price)
        print(self.position.size)
        print("avg: {}, TP: {}, size: {}".format(self.current_avg_buy, self.current_tp, self.current_size))
        print("=========")
        print("Current Bot Vol: {}".format(self.current_bot_vol))
        print("Current Bot UPNL: -{}".format(self.current_bot_upnl))
        print("Total Bot Profit: {}".format(self.total_bot_profit))
        # print(len(self.my_orders))
        # for x in self.my_orders:
        # print("{} - {} - {}".format(str(x.price), x.size, x.Status[x.status]))
        # print(str(x.Status[x.status]))
        # print(self.orders_executed[1])

    # def fill_bot_orders(self):
    # for order in self.map_bot_orders.values():
    # order_buy = self.buy(exectype=bt.Order.Limit, size=order.order_size, price=order.order_price)
    # self.my_orders.append(order_buy)
    #   order.order_status = BotStatus.ACCEPTED
