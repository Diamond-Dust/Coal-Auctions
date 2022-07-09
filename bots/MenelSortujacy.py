from random import uniform
import random

from bots.BaseBot import BaseBot
from staff.Bet import Bet


class XXampleBot(BaseBot):

    def __init__(self, bot_id, coal_market_valuation):
        super().__init__(bot_id, coal_market_valuation)

        self.my_bets = []
        self.previous_results = []
        self.name = 'Menel'

    def bet(self, quality_tests, previous_round_results, money):
        prognoses = [(test.mine_id, self.coal_market_valuation(test)) for test in quality_tests]
        prognoses.sort(key=lambda x: x[1])
        lasteval = 0.0001
        puszki = []
        puszka = 10.1
        for index, prognosis in enumerate(prognoses):
                neweval = prognosis[1]
                diff = (neweval-lasteval)/(1000.0)
                lasteval = neweval
                puszka = puszka + diff
                puszki.append(puszka)
        return [
            Bet(
                prognosis[0],
                puszki[index],
                index
            ) for index, prognosis in enumerate(prognoses)
        ]
