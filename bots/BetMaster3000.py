from random import uniform
import random

from bots.BaseBot import BaseBot
from staff.Bet import Bet


class XampleBot(BaseBot):

    def __init__(self, bot_id, coal_market_valuation):
        super().__init__(bot_id, coal_market_valuation)

        self.my_bets = []
        self.previous_results = []
        self.name = 'yyy'

    def bet(self, quality_tests, previous_round_results, money):
        self.previous_results.append(previous_round_results)
        n = len(quality_tests)
        abc = list(range(1,n+1))
        bcd = list(range(1,n+1))
        ind = list(range(1,n+1))
        random.shuffle(abc)
        random.shuffle(bcd)

        bets = []
        for x in ind:
                bets.append(Bet(abc[x-1]-1, 12, bcd[x-1]-1))

        return bets
