import backtrader as bt

from BotOrder import BotOrder
from BotStatus import BotStatus


class DCAStrat(bt.Strategy):
    my_orders = []
    map_bot_safety_orders = {}
    bot_base_order = None

    # config_order_tp = 1.0213
    # config_order_tp = 1.0038
    # config_order_tp = 1.0138
    config_order_tp = 1.0313
    # config_order_tp = 1.0513
    # config_order_tp = 1.0613
    # config_order_tp = 1.0643
    # config_order_tp = 1.0713
    # config_order_tp = 1.1013
    # config_order_tp = 1.1213
    # config_order_tp = 1.1513
    # config_order_tp = 1.15613
    # config_order_tp = 1.1513
    # config_order_tp = 1.1513
    # config_order_tp = 1.1513

    config_base_order_volume = 300.00
    config_safety_order_volume = 30.00
    config_order_safety_sos = 0.0125
    config_order_volume_scale = 1.01
    config_order_step_scale = 0.98
    config_mstc = 100
    total_bot_cost = 0
    total_bot_profit = 0

    is_bot_active = False
    stopped = False

    current_avg_buy = None
    current_size = None
    current_tp = None
    current_ss = None
    current_last_SO_price = None
    current_bot_upnl = None
    current_bot_vol = None
    current_bot_close_price = None
    current_SO = 0

    def __init__(self):
        self.total_bot_cost = self.calculate_bot_total_cost()
        print("start... total bot cost will be: {}".format(self.total_bot_cost))

    def calculate_bot_total_profit(self, net_profit):
        print(net_profit)
        if self.stopped:
            return 0
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

    def calculate_bot_total_cost(self):
        vol = self.config_safety_order_volume
        cost = self.config_base_order_volume + self.config_safety_order_volume
        for i in range(1, self.config_mstc):
            vol *= self.config_order_volume_scale
            cost += vol
        return cost

    # TODO:
    # Bot por 1 run parece correcto. Testar para varias trades

    def reset_current_status(self):
        self.current_avg_buy = 0
        self.current_size = 0
        self.current_tp = 0
        self.current_ss = 0
        self.current_last_SO_price = 0
        self.my_orders = []
        self.map_bot_safety_orders = {}
        self.bot_base_order = 0
        self.current_bot_upnl = 0
        self.current_bot_vol = 0

    bar_count = 0

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def next(self):
        self.bar_count += 1

        if self.bar_count > 11111110:
            return

        print("NEW BARR")
        try:
            next_bar = self.data.close[2]
            self.current_bot_close_price = self.data.close[2]
        except IndexError:
            if not self.stopped:
                self.graceful_stop_current_trade(self.data)
                self.stopped = True
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

    def graceful_stop_current_trade(self, data):
        print(">gracefully stopping last trade")
        buy_size = ((self.current_avg_buy * self.current_size) - (self.current_size * data.high[1])) / (
                data.high[1] - data.low[1])
        order_buy = self.buy(exectype=bt.Order.StopLimit, size=buy_size, price=data.low[1])
        self.map_bot_safety_orders["last"] = BotOrder(order_volume=buy_size * data.low[1],
                                                      order_price=data.low[1],
                                                      order_size=buy_size,
                                                      order_status=BotStatus.FILLED)

        self.my_orders.append(order_buy)
        self.recalculate_current_status()

        sell_size = self.getposition(data).size + buy_size
        self.sell(exectype=bt.Order.Sell, size=sell_size, price=data.high[1])
        self.reset_current_status()

    def start_bot(self, start_price):
        print(">start bot...")
        self.update_bot_orders(start_price)
        self.is_bot_active = True
        self.bot_base_order = self.buy(exectype=bt.Order.StopLimit, size=self.current_size, price=start_price)
        # TODO: FILL BASE ORDER NOW
        # self.fill_bot_orders()
        # self.peak_next_bar(self.data)

    def create_first_safety_bot_order(self, order):
        so1_order_ss = self.config_order_safety_sos
        so1_order_price = order.order_price * (1 - self.config_order_safety_sos)
        so1_order_vol = self.config_safety_order_volume
        so1_order_size = self.calculate_size2(so1_order_vol, so1_order_price)
        print("Creating SO1 -> ord_price: {}, ord_ss: {}, ord_siz:{}, order_vol:{}".format(so1_order_price, so1_order_ss, so1_order_size, so1_order_vol, so1_order_ss))
        #self.current_ss = self.current_ss * ss
        return BotOrder(order_price=so1_order_price,
                        order_ss=so1_order_ss,
                        order_size=so1_order_size,
                        order_volume=so1_order_vol,
                        order_status=BotStatus.PENDING)

    def update_bot_orders(self, start_price):
        print(">NEW update_bot_orders: {}".format(start_price))
        base_order = self.create_base_bot_order(start_price)
        self.update_current_status_with_base_order(base_order)
        safety_order = self.create_first_safety_bot_order(base_order)
        self.map_bot_safety_orders["so1"] = safety_order
        for i in range(2, self.config_mstc + 1):
            safety_order = self.create_safety_bot_order(order=safety_order, orderNumber=i)
            self.map_bot_safety_orders["so{}".format(i)] = safety_order

    #    def update_bot_orders(self, start_price):
    #        print(">update_bot_orders: {}".format(start_price))
    #        base_order = self.create_base_bot_order(start_price)
    #        self.bot_base_order = base_order
    #        self.update_current_status(base_order)
    #        safety_order = self.create_safety_bot_order(volume=self.config_safety_order_volume, price=start_price)
    #        self.map_bot_safety_orders["so1"] = safety_order

    #        for i in range(2, self.config_mstc + 1):
    #            safety_order = self.create_safety_bot_order(
    #                safety_order.order_volume,
    #                safety_order.order_price,
    #                i=i,
    #                ss=self.config_order_step_scale,
    #                os=self.config_order_volume_scale
    #            )
    #            self.map_bot_safety_orders["so{}".format(i)] = safety_order
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
        self.reset_current_status()
        return closing_price

    def calculate_size(self, order_volume, buy_price):
        return order_volume / buy_price

    def calculate_size2(self, order_volume, buy_price):
        shares = (order_volume / buy_price)
        return self.round_down(shares, 15)

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
        print("Creating BO  -> ord_price: {}, ord_ss: {}, ord_siz:{}, order_vol:{}".format(order_price, 1, order_size, order_volume))
        return BotOrder(order_price=order_price,
                        order_ss=1,
                        order_size=order_size,
                        order_volume=order_volume,
                        order_status=BotStatus.FILLED)

    def create_safety_bot_order(self, order, orderNumber):
        sox_order_ss = order.order_ss * self.config_order_step_scale
        sox_order_price = order.order_price * (1 - sox_order_ss)
        sox_order_vol = order.order_volume * self.config_order_volume_scale
        sox_order_size = self.calculate_size(sox_order_vol, sox_order_price)
        print("Creating SO{} -> ord_price: {}, ord_ss: {}, ord_siz:{}, order_vol:{}".format(orderNumber, sox_order_price, sox_order_ss, sox_order_size, sox_order_vol))
        return BotOrder(order_price=sox_order_price,
                        order_ss=sox_order_ss,
                        order_size=sox_order_size,
                        order_volume=sox_order_vol,
                        order_status=BotStatus.PENDING)
        #order_volume = volume * os
        #order_price = price * (1.00 - (self.current_ss))
        #order_size = self.calculate_size(order_volume, order_price)
        ## print("UPDATING: SO{} order_vol:{}, vol:{}, ord_price: {}, pric:{}, ord_siz:{},  cur_ss:{}, ss:{}, cu_bot_vol:{}, os:{}, ".format(i-1,order_volume, volume, order_price, price, order_size, self.current_ss, ss, self.current_bot_vol, os))
        #print("UPDATING: SO{} -> order_vol:{}, vol:{}, ord_price: {}, pric:{} ".format(i - 1, order_volume, volume,
        #                                                                               order_price, price))
        ## print("UPDATING: SO{} -> cur_ss:{}, ss:{}".format(i-1, self.current_ss, ss))
        ## print("----- Safety order ------")
        ## print("volume: {}, price: {}, size: {} ss {}".format(order_volume, order_price, order_size, self.current_ss))
        #self.current_ss = self.current_ss * ss
        #return BotOrder(order_volume=order_volume,
        #                order_price=order_price,
        #                order_size=order_size,
        #                order_status=BotStatus.PENDING)

    def update_current_status_with_base_order(self, order):
        self.current_tp = order.order_price * self.config_order_tp
        self.current_avg_buy = order.order_price
        self.current_size = order.order_size
        self.current_ss = self.config_order_safety_sos
        self.current_last_SO_price = order.order_price
        self.current_bot_vol = order.order_price * order.order_size
 #       print("Current cu_price: {}, TP: {}, cu_size: {}, cu_ss: {}, last_SO_price: {}".format(order.order_price,
 #                                                                                              self.current_tp,
 #                                                                                              self.current_size,
 #                                                                                              self.current_ss,
 #                                                                                              self.current_last_SO_price))

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
        print(
            "Recalculate: TP: {}, cu_size: {}, cu_ss: {}, last_SO_price: {}".format(self.current_tp, self.current_size,
                                                                                    self.current_ss,
                                                                                    self.current_last_SO_price))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log("BUY EXECUTED ref:{}, SO: {} price: {} size: {}".format(order.ref, self.current_SO,
                                                                                 order.executed.price,
                                                                                 order.executed.size))
                self.current_SO += 1
            elif order.issell():
                netProfit = -(order.executed.price * order.executed.size)
                profit = self.calculate_bot_total_profit(netProfit)
                self.total_bot_profit += profit
                self.current_SO = 0
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
        print("Total bars: {}".format(self.bar_count))
        print("Total Bot Cost: {:.2f}".format(self.total_bot_cost))
        print("Total Bot Profit: {:.2f}".format(self.total_bot_profit))
        print("Total Bot ROI: {:.2f}%".format((self.total_bot_profit / self.total_bot_cost) * 100))
        print("Daily Bot ROI: {:.2f}%".format(((self.total_bot_profit / self.bar_count) / self.total_bot_cost) * 100))
        print("{:.2f}".format(self.total_bot_profit))
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
