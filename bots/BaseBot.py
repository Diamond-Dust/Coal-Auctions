from abc import abstractmethod
from typing import List

from staff.Bet import Bet
from staff.QualityTest import QualityTest
from staff.RoundResults import RoundResults


class BaseBot:
    def __init__(self, bot_id, coal_market_valuation):
        self.name = 'BaseBot'
        self.bot_id = bot_id
        self.coal_market_valuation = coal_market_valuation

    @abstractmethod
    def bet(self, quality_tests: List[QualityTest], previous_round_results: RoundResults, money: float) -> List[Bet]:
        pass
