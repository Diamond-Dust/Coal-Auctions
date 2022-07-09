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
        return [Bet(quality_test.mine_id, money / len(quality_tests), 1) for quality_test in quality_tests]
