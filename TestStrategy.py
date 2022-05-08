import backtrader as bt

from BotConfig import BotConfig
from BotOrder import BotOrder
from BotStatus import BotStatus
from utils import round_decimals_up, round_decimals_down

class Omg():
    name="xico"
    Age=32

    def __init__(self, name:str=None):
        self.name = name

class TestStrat(bt.Strategy):
    params = (
        ('config', None),
    )


    def __init__(self):
        print(self.params.config.name)
        print("heyyy")

