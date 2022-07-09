from random import uniform

from bots.BaseBot import BaseBot
from staff.Bet import Bet


class SampleBot(BaseBot):
    #smrodobot testujacy stronke

    def __init__(self, bot_id, coal_market_valuation):
        super().__init__(bot_id, coal_market_valuation)

        self.my_bets = []
        self.previous_results = []
        self.name = 'MarstarsTestBot'

    def bet(self, quality_tests, previous_round_results, money):
        self.previous_results.append(previous_round_results)

        my_bet = self.calculate_bets(quality_tests)

        self.my_bets.append(my_bet)

        return my_bet

    def calculate_bets(self, quality_tests):
        prognoses = [(test.mine_id, self.coal_market_valuation(test)) for test in quality_tests]

        prognoses.sort(key=lambda x: x[1])

        my_bet = [
            Bet(
                prognosis[0],
                prognosis[1] / 2 + uniform(100.0, 1000.0),
                index
            ) for index, prognosis in enumerate(prognoses)
        ]

        return my_bet
