import backtrader as bt

from BotConfig import BotConfig
from BotOrder import BotOrder
from BotStatus import BotStatus
from utils import round_decimals_up, round_decimals_down


class DCAStrat(bt.Strategy):
    params = (
        ('config', None),
    )

    my_orders = []
    bot_last_active_order = {}
    map_bot_safety_orders = {}
    bot_base_order = None
    bot_number = 0
    bot_extra_mstc_reached_times = 0
    bot_risk_surpassed_times = 0

    # config_order_tp = 1.02
    # config_order_tp = 1.0038
    # config_order_tp = 1.0125
    # config_order_tp = 1.03
    # config_order_tp = 1.05
    # config_order_tp = 1.06
    # config_order_tp = 1.065
    # config_order_tp = 1.07
    # config_order_tp = 1.10
    # config_order_tp = 1.12
    # config_order_tp = 1.15
    # config_order_tp = 1.15
    # config_order_tp = 1.16
    # config_order_tp = 1.20
    # config_order_tp = 1.25

    config_order_tp = None
    config_base_order_volume = None
    config_safety_order_volume = None
    config_order_safety_sos = None
    config_order_step_scale = None
    config_order_volume_scale = None
    config_mstc = None
    config_profit_mstc = None
    config_risk_value = None
    config_round_decimal = None
    config_is_coin_token = None
    config_is_multi_bot = None

    total_bot_cost = 0
    total_bot_profit = 0

    is_bot_active = False
    stopped = False

    current_start_price = None
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
        self.clean_all_bot_status()
        self.config_order_tp = self.params.config.config_order_tp
        self.config_base_order_volume = self.params.config.config_base_order_volume
        self.config_safety_order_volume = self.params.config.config_safety_order_volume
        self.config_order_safety_sos = self.params.config.config_order_safety_sos
        self.config_order_step_scale = self.params.config.config_order_step_scale
        self.config_order_volume_scale = self.params.config.config_order_volume_scale
        self.config_mstc = self.params.config.config_mstc
        self.config_profit_mstc = self.params.config.config_profit_mstc
        self.config_risk_value = self.params.config.config_risk_value
        self.config_round_decimal = self.params.config.config_round_decimal
        self.config_is_coin_token = self.params.config.config_is_coin_token
        self.config_is_multi_bot = self.params.config.config_is_multi_bot

        self.total_bot_cost = self.calculate_bot_total_cost()
        # print("start... total bot cost will be: {}".format(self.total_bot_cost))

    def calculate_bot_total_profit(self, net_profit, avg_price, size):
        if self.stopped:
            return 0
        total_vol = avg_price * -size
        affordable_bot_cost = self.total_bot_cost
        if total_vol > affordable_bot_cost:
            self.bot_risk_surpassed_times += 1

        # print("NEW CALCULATE PROFIT MWAHAHA", total_vol,  net_profit, avg_price, size)
        return net_profit - total_vol

    def calculate_bot_total_cost(self):
        vol = self.config_safety_order_volume
        cost = self.config_base_order_volume + self.config_safety_order_volume
        for i in range(1, self.config_profit_mstc):
            vol *= self.config_order_volume_scale
            cost += vol

        real_risked_cost = cost / self.config_risk_value

        return real_risked_cost

    # TODO:
    # Bot por 1 run parece correcto. Testar para varias trades

    def clean_all_bot_status(self):
        self.my_orders = []
        self.bot_last_active_order = {}
        self.map_bot_safety_orders = {}
        self.bot_base_order = None
        self.bot_number = 0
        self.bot_extra_mstc_reached_times = 0
        self.bot_risk_surpassed_times = 0
        self.current_start_price = None
        self.current_avg_buy = None
        self.current_size = None
        self.current_tp = None
        self.current_ss = None
        self.current_last_SO_price = None
        self.current_bot_upnl = None
        self.current_bot_vol = None
        self.current_bot_close_price = None
        self.current_SO = 0
        self.total_bot_cost = 0
        self.total_bot_profit = 0
        self.is_bot_active = False
        self.stopped = False


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
        self.current_start_price = None

    current_bot_close_price = None

    bar_count = 0

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def print_first_bar(self):
        print("\t>>>Next Bar {}:low {}, open: {}, close: {}, high {} ".format(self.bar_count, self.data.low[0],
                                                                              self.data.open[0], self.data.close[0],
                                                                              self.data.high[0]))

    def print_next_bar(self):
        print("\t>>>Next Bar {}:low {}, open: {}, close: {}, high {} ".format(self.bar_count + 1, self.data.low[1],
                                                                              self.data.open[1], self.data.close[1],
                                                                              self.data.high[1]))

    def next(self):
        self.bar_count += 1

        if self.bar_count > 1111112:
            return

        try:
            next_bar = self.data.close[2]
            self.current_bot_close_price = self.data.close[2]
        except IndexError:
            if not self.stopped:
                self.graceful_stop_current_trade(self.data)
                self.stopped = True
            return

        if self.bar_count == 1:
            #self.print_first_bar()
            self.start_bot(self.data.close[0])

        #self.print_next_bar()

        # if not self.is_bot_active:
        #    self.start_bot(self.data.close[0])
        #    return

        self.peak_next_bar(self.data)

    def graceful_stop_current_trade(self, data):
        # print(">gracefully stopping last trade")
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
        self.bot_number += 1
        start_price = self.get_rounded_price(start_price)
        #print(">starting bot_num: {} with price {}".format(self.bot_number, start_price))
        self.update_bot_orders(start_price)
        self.is_bot_active = True
        self.buy(exectype=bt.Order.StopLimit, size=self.current_size, price=start_price)
        # TODO: FILL BASE ORDER NOW
        # self.fill_bot_orders()
        # self.peak_next_bar(self.data)

    def update_bot_orders(self, start_price):
        # print(">NEW update_bot_orders: {}".format(start_price))
        base_order = self.create_base_bot_order(start_price)
        self.bot_base_order = base_order
        self.update_current_status_with_base_order(base_order)
        safety_order = self.create_first_safety_bot_order(base_order)
        self.map_bot_safety_orders["so1"] = safety_order
        self.bot_last_active_order[self.bot_number] = base_order
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
        # print(">peaking")
        if self.is_bot_active:
            if data.close[1] < data.open[1]:
                self.process_red_candle(data)
            else:
                self.process_green_candle(data)

            # self.check_bar_bottom(data)
            # self.check_bar_top(data)

    def process_red_candle(self, data):
        # print(">red candle")
        self.check_bar_top(data)
        self.check_bar_bottom(data)
        self.fill_bar_from_bottom_to_close(data)

    def process_green_candle(self, data):
        # print(">green candle")
        self.check_bar_bottom(data)
        self.check_bar_top(data)
        self.fill_bar_from_top_to_close(data)

    def check_bar_bottom(self, data):
        # print(" check bottom: current_tp: {} price: {} low: {} close: {} high: {}".format(self.current_tp,
        #                                                                                  self.current_last_SO_price,
        #                                                                                  data.low[1], data.close[1],
        #                                                                                  data.high[1]))
        for order in self.map_bot_safety_orders.values():
            if (order.order_price > data.low[1]) and (order.order_status == BotStatus.PENDING):
                self.fill_bot_safety_order(order)

    def fill_bot_safety_order(self, order):
        order.order_status = BotStatus.FILLED
        order_buy = self.buy(exectype=bt.Order.StopLimit, size=order.order_size, price=order.order_price)
        # print("placing order_buy = self.buy(exectype=",bt.Order.StopLimit, " size=", order.order_size, " price=", order.order_price, ")")
        self.my_orders.append(order_buy)
        self.current_last_SO_price = order.order_price  # TODO: check there is no bug with this approach without < validation
        self.recalculate_current_status()

    def check_bar_top(self, data):
        # print(">check_bar_top {} {}".format(self.current_tp <= data.high[1], self.is_bot_active))
        if self.current_tp <= data.high[1] and self.is_bot_active:
            closing_price = self.close_active_orders(data.high[1])
            closing_price = self.scalp_bar(data, closing_price, "top")
            self.start_bot(closing_price)

    def fill_bar_from_bottom_to_close(self, data):
        if self.current_tp <= data.close[1] and self.is_bot_active:
            # print("Going Up on bar from Bottom to close: current_tp: {} price: {} low: {} close: {} high: {
            # }".format(self.current_tp, self.current_last_SO_price, data.low[1], data.close[1], data.high[1]))
            closing_price = self.close_active_orders(data.close[1])
            closing_price = self.scalp_bar(data, closing_price, "bottom_to_close")
            self.start_bot(closing_price)

    def fill_bar_from_top_to_close(self, data):
        for order in self.map_bot_safety_orders.values():
            if (order.order_price > data.close[1]) and (order.order_status == BotStatus.PENDING):
                # print("Going down on bar from top to close: current_tp: {} price: {} low: {} close: {} high: {
                # }".format(self.current_tp, self.current_last_SO_price, data.low[1], data.close[1], data.high[1]))
                self.fill_bot_safety_order(order)

    def scalp_bar(self, data, closing_price, event):
        current_tp = closing_price * self.config_order_tp
        while current_tp <= data.high[1]:
            self.bot_number += 1
            size = self.calculate_size(self.config_base_order_volume, closing_price)
            self.buy(exectype=bt.Order.StopLimit, size=size, price=closing_price)
            active_order = BotOrder(order_avg_price=closing_price)
            self.sell(exectype=bt.Order.StopLimit, price=current_tp, size=size)
            closing_price = current_tp
            current_tp = closing_price * self.config_order_tp
            self.bot_last_active_order[self.bot_number] = active_order
            # print(">Scalping {} bar bot_num: {}, price: {}, TP: {}, high: {}".format(event, self.bot_number,
            #                                                                         closing_price, current_tp,
            #                                                                         data.high[1]))
        return closing_price

    def close_active_orders(self, max_close_price):
        closing_price = self.current_tp
        self.sell(exectype=bt.Order.StopLimit, price=self.current_tp, size=self.current_size)
        # print("stopping bot_num: {}.... current_tp: {}, close Until: {}, size: {} ".format(self.bot_number,
        #                                                                                   self.current_tp,
        #                                                                                   max_close_price,
        #                                                                                   self.current_size))
        self.reset_current_status()
        return closing_price

    def calculate_size(self, order_volume, buy_price):
        size = order_volume / buy_price
        if self.config_is_coin_token:
            # print("order_vol: {}, buy_price: {}, size: {}".format(order_volume, buy_price, size))
            size1 = round_decimals_up(size, 0)
            # print("calc_size:", vol, vol1)
            size = size1
        return size

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
        order_volume_iter = self.config_base_order_volume
        order_price = price
        order_size = self.calculate_size(order_volume_iter, order_price)
        order_volume = self.get_rounded_volume(order_price * order_size)
        self.current_start_price = price
        order_cumulative_volume = order_volume
        order_cumulative_size = order_size
        # print("----- base order ------")
        # print("volume: {}, price: {}, size: {} ".format(order_volume, order_price, order_size))
        # print("Creating BO  -> ord_price: {}, ord_ss: {}, ord_siz:{}, order_vol:{}".format(order_price, 1, order_size,
        #                                                                                   order_volume))
        return BotOrder(order_price=order_price,
                        order_avg_price=order_price,
                        order_incremented_ss=0,
                        order_total_ss=0,
                        order_size=order_size,
                        order_volume=order_volume,
                        order_cumulative_volume=order_cumulative_volume,
                        order_cumulative_size=order_cumulative_size,
                        order_status=BotStatus.FILLED)

    def create_first_safety_bot_order(self, order):
        so1_base_ss = self.config_order_safety_sos  # 1.25%
        so1_incremental_ss = self.config_order_safety_sos
        so1_total_ss = self.config_order_safety_sos

        # so1_order_ss = self.config_order_safety_sos
        so1_order_price = self.get_rounded_price(self.current_start_price * (1 - so1_total_ss))
        so1_order_iter_vol = self.config_safety_order_volume
        so1_order_size = self.calculate_size(so1_order_iter_vol, so1_order_price)
        so1_order_vol = self.get_rounded_volume(so1_order_price * so1_order_size)
        so1_cumulative_volume = order.order_volume + so1_order_vol
        so1_cumulative_size = order.order_cumulative_size + so1_order_size
        # print( "Creating SO1 -> ord_price: {}, ord_inc_ss: {}, ord_total_ss: {}, ord_siz:{}, ord_cum_siz:{},
        # order_vol:{}".format( so1_order_price, so1_incremental_ss, so1_total_ss, so1_order_size,
        # so1_cumulative_size, so1_order_vol))
        return BotOrder(order_price=so1_order_price,
                        order_incremented_ss=so1_incremental_ss,
                        order_total_ss=so1_total_ss,
                        order_size=so1_order_size,
                        order_iteration_volume=so1_order_iter_vol,
                        order_cumulative_volume=so1_cumulative_volume,
                        order_cumulative_size=so1_cumulative_size,
                        order_volume=so1_order_vol,
                        order_status=BotStatus.PENDING)

    def create_safety_bot_order(self, order, orderNumber):
        isExtraOrder = self.check_if_extra_mstc_order(orderNumber)
        sox_base_ss = order.order_total_ss
        sox_incremental_ss = order.order_incremented_ss * self.config_order_step_scale  # 1,25 * 0,98 = 0,01225
        sox_total_ss = sox_base_ss + sox_incremental_ss

        sox_order_price = self.get_rounded_price(self.current_start_price * (1 - sox_total_ss))

        # sox_base_ss = order.order_total_ss
        # sox_order_ss = sox_base_ss

        # sox_order_ss = order.order_ss * self.config_order_step_scale
        sox_order_vol_iter = self.get_rounded_volume(order.order_iteration_volume * self.config_order_volume_scale)
        sox_order_size = self.calculate_size(sox_order_vol_iter, sox_order_price)
        sox_order_real_vol = self.get_rounded_volume(sox_order_price * sox_order_size)
        sox_cumulative_volume = order.order_volume + sox_order_real_vol
        sox_cumulative_size = order.order_cumulative_size + sox_order_size
        # print(
        #    "Creating SO{} -> ord_price: {}, ord_inc_ss: {}, ord_total_ss: {}, ord_siz:{}, ord_cum_siz:{}, order_vol_iter:{}, order_real_vol:{}, exra order? {}".format(
        #        orderNumber, sox_order_price, sox_incremental_ss, sox_total_ss,
        #        sox_order_size, sox_cumulative_size, sox_order_vol_iter, sox_order_real_vol, isExtraOrder))

        return BotOrder(order_price=sox_order_price,
                        order_incremented_ss=sox_incremental_ss,
                        order_total_ss=sox_total_ss,
                        order_size=sox_order_size,
                        order_iteration_volume=sox_order_vol_iter,
                        order_volume=sox_order_real_vol,
                        order_cumulative_volume=sox_cumulative_volume,
                        order_cumulative_size=sox_cumulative_size,
                        order_status=BotStatus.PENDING,
                        order_is_extra_mstc=isExtraOrder)
        # order_volume = volume * os
        # order_price = price * (1.00 - (self.current_ss))
        # order_size = self.calculate_size(order_volume, order_price)
        ## print("UPDATING: SO{} order_vol:{}, vol:{}, ord_price: {}, pric:{}, ord_siz:{},  cur_ss:{}, ss:{}, cu_bot_vol:{}, os:{}, ".format(i-1,order_volume, volume, order_price, price, order_size, self.current_ss, ss, self.current_bot_vol, os))
        # print("UPDATING: SO{} -> order_vol:{}, vol:{}, ord_price: {}, pric:{} ".format(i - 1, order_volume, volume,
        #                                                                               order_price, price))
        ## print("UPDATING: SO{} -> cur_ss:{}, ss:{}".format(i-1, self.current_ss, ss))
        ## print("----- Safety order ------")
        ## print("volume: {}, price: {}, size: {} ss {}".format(order_volume, order_price, order_size, self.current_ss))
        # self.current_ss = self.current_ss * ss
        # return BotOrder(order_volume=order_volume,
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
        order_number = 0
        # use my own BorOrder object, that has real total volume, which can be used to calculate
        # avg buy, which can be used to calculate TP

        avg_price_numerator = self.bot_base_order.order_price * self.bot_base_order.order_size
        avg_price_denominator = self.bot_base_order.order_size
        self.current_bot_vol = self.config_base_order_volume
        last_active_order = self.bot_base_order
        for order in self.map_bot_safety_orders.values():
            if order.order_status == BotStatus.FILLED:
                last_active_order = order
                avg_price_numerator += order.order_price * order.order_size
                avg_price_denominator += order.order_size
                self.current_bot_vol += order.order_price * order.order_size
                order_number += 1

        self.current_avg_buy = avg_price_numerator / avg_price_denominator
        self.current_tp = self.current_avg_buy * self.config_order_tp
        self.current_size = avg_price_denominator
        self.current_bot_upnl = self.current_bot_vol - (self.current_size * self.current_bot_close_price)
        last_active_order.order_avg_price = self.current_avg_buy
        self.bot_last_active_order[self.bot_number] = last_active_order
        #print( "Recalculate: SO: {}, BN: {}, Buy Price {} Avg Buy: {}, TP: {}, cu_size: {}, cu_ss: {},last_SO_price: {}"
        #       .format( order_number, self.bot_number, last_active_order.order_price,
        #            self.current_avg_buy, self.current_tp, self.current_size, self.current_ss, self.current_last_SO_price))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                #self.log("BUY EXECUTED ref:{}, price: {} size: {}".format(order.ref, order.executed.price,
                #                                                          order.executed.size))
                self.current_SO += 1
            elif order.issell():
                # print("SELLL -> last active orders ", self.bot_last_active_order)
                bot_numb = min(self.bot_last_active_order)
                # TODO: Careful, in scalp this "last_order" object only has only avg price
                last_order = self.bot_last_active_order[bot_numb]
                netProfit = -(order.executed.price * order.executed.size)
                profit = self.calculate_bot_total_profit(net_profit=netProfit, avg_price=last_order.order_avg_price,
                                                         size=order.executed.size)
                if last_order.order_is_extra_mstc:
                    self.bot_extra_mstc_reached_times += 1
                # profit = self.calculate_bot_total_profit(netProfit)
                self.total_bot_profit += profit
                self.current_SO = 0
                map_print = ""
                for k, v in self.bot_last_active_order.items():
                    map_print += "Inside obj: {} {} \t".format(k, v.order_avg_price)
                del self.bot_last_active_order[min(self.bot_last_active_order)]
                # print("Deleting bot order numb: {} -> last active orders ".format(bot_numb), self.bot_last_active_order)
                #self.log(
                #   "SELL EXECUTED bot_numb: {}, ref:{}, price: {} size: {} -----> Profit: {}\t Deleting bot order numb: {} -> last active orders {}".format(
                #       bot_numb, order.ref, order.executed.price,
                #       order.executed.size,
                #       profit, bot_numb, self.bot_last_active_order))

        elif order.status in [order.Canceled]:
            self.log("ORDER CANCELLED")

    def _stop(self):
        # print("------------ DONE ------------")
        # print(self.position)
        # print(self.position.price)
        # print(self.position.size)
        # print("avg: {}, TP: {}, size: {}".format(self.current_avg_buy, self.current_tp, self.current_size))
        # print("=========")
        # print("Current Bot Vol: {}".format(self.current_bot_vol))
        # print("Current Bot UPNL: -{}".format(self.current_bot_upnl))
        # print("Total bars: {}".format(self.bar_count))
        if self.config_is_multi_bot:
            self.print_dca_multi_bot()
        else:
            self.print_dca_bot()
        self.reset_current_status()
        # print("{:.2f}".format(self.total_bot_profit))
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

    def get_rounded_price(self, price):
        return round_decimals_down(price, self.config_round_decimal)

    def get_rounded_volume(self, vol):
        return round(vol, self.config_round_decimal)

    def check_if_extra_mstc_order(self, orderNumber):
        isExtraOrder = False
        if orderNumber > self.config_profit_mstc:
            isExtraOrder = True
        return isExtraOrder

    def print_dca_bot(self):
        print("Bot Risk: {}%".format(self.config_risk_value * 100))
        print("Number of times Bot volume surpassed risk volume: {}".format(self.bot_risk_surpassed_times))
        print("Number of times Bot reached extra mstc: {}".format(self.bot_extra_mstc_reached_times))
        print("Total Bot Cost: {:.2f}".format(self.total_bot_cost))
        print("Total Bot ROI: {:.2f}%".format((self.total_bot_profit / self.total_bot_cost) * 100))
        print("Daily Bot ROI: {:.2f}%".format(((self.total_bot_profit / self.bar_count) / self.total_bot_cost) * 100))
        print("Total Bot Profit: {:.2f}".format(self.total_bot_profit))
        print("")

    def print_dca_multi_bot(self):
        tp = (self.config_order_tp - 1) * 100
        daily_roi = ((self.total_bot_profit / self.bar_count) / self.total_bot_cost) * 100
        total_roi = (self.total_bot_profit / self.total_bot_cost) * 100
        str = "TP:{:6.2f}%, Profit:{:7.2f}, Daily ROI:{:4.2f}, ROI:{:5.2f}, Bot Cost:{:6.2f}, Risk:{}, Nº>risk:{}, Nº>mstc:{}, bot_numb:{:3}"
        print(str.format(tp,
                         self.total_bot_profit,
                         daily_roi,
                         total_roi,
                         self.total_bot_cost,
                         self.config_risk_value * 100,
                         self.bot_risk_surpassed_times,
                         self.bot_extra_mstc_reached_times,
                         self.bot_number,
                         ))
        # print("Bot Risk: {}%".format(self.config_risk_value * 100))
        # print("Number of times Bot volume surpassed risk volume: {}".format(self.bot_risk_surpassed_times))
        # print("Number of times Bot reached extra mstc: {}".format(self.bot_extra_mstc_reached_times))
        # print("Total Bot Cost: {:.2f}".format(self.total_bot_cost))
        # print("Total Bot ROI: {:.2f}%".format((self.total_bot_profit / self.total_bot_cost) * 100))
        # print("Daily Bot ROI: {:.2f}%".format(((self.total_bot_profit / self.bar_count) / self.total_bot_cost) * 100))
        # print("Total Bot Profit: {:.2f}".format(self.total_bot_profit))
        # print("")
