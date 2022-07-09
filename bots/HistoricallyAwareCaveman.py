from random import uniform

from bots.BaseBot import BaseBot
from staff.Bet import Bet


class HistoricallyAwareCaveman(BaseBot):
    def __init__(self, bot_id, coal_market_valuation):
        super().__init__(bot_id, coal_market_valuation)

        self.my_bets = []
        self.previous_results = []
        self.name = 'HistoricallyAwareCaveman'
        self.incomes = {}

    def bet(self, quality_tests, previous_round_results, money):
        self.update_historical_income(previous_round_results)
        self.previous_results.append(previous_round_results)

        my_bet = self.calculate_bets(quality_tests)

        self.my_bets.append(my_bet)

        return my_bet

    def calculate_bets(self, quality_tests):
        prognoses = [(test.mine_id, self.coal_market_valuation(test), self.historical_income(test.mine_id)) for test in quality_tests]

        prognoses.sort(key=lambda x: x[2])

        my_bet = [
            Bet(
                prognosis[0],
                prognosis[1] / 2 + uniform(50.0, 500.0),
                index
            ) for index, prognosis in enumerate(prognoses)
        ]

        return my_bet
    
    def historical_income(self, mine_id):
        if mine_id in self.incomes.keys():
            return self.incomes[mine_id]
        
        return 0
    
    def update_historical_income(self, results):
        if results is None:
            return

        for _, result in results.winners.items():
            bet, income, mine_id = result['bet'], result['income'], result['mine_id']
            actual_income = income - bet
            historical_income = self.historical_income(mine_id)
            self.incomes[mine_id] = historical_income + actual_income

