from random import uniform
from typing import List

from staff.Bet import Bet
from staff.QualityTest import QualityTest
from staff.RoundResults import RoundResults
from bots.BaseBot import BaseBot

class TwojStaryBot(BaseBot):
    def __init__(self, bot_id, coal_market_valuation):
        super().__init__(bot_id, coal_market_valuation)
        self.name = 'TwojStaryBot'

    def bet(self, quality_tests: List[QualityTest], previous_round_results: RoundResults, money: float) -> List[Bet]:
        prognoses = [(test.mine_id, self.coal_market_valuation(test)) for test in quality_tests]
        prognoses.sort(key=lambda x: x[1])

        amount = 10
        if previous_round_results:
            previous_bets = [result['bet'] for result in previous_round_results.winners.values()]
            amount = min(previous_bets) + 1

        return [
            Bet(
                prognosis[0],
                amount,
                index
            ) for index, prognosis in enumerate(prognoses)
        ]
