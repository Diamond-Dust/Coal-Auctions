from random import uniform
from re import M
from scipy.stats import linregress

from bots.BaseBot import BaseBot
from staff.Bet import Bet


class GrandmaOnARollercoaster(BaseBot):
    def __init__(self, bot_id, coal_market_valuation):
        super().__init__(bot_id, coal_market_valuation)

        self.my_bets = []
        self.previous_results = []
        self.previous_tests = None
        self.name = 'GrandmaOnARollercoaster'
        self.incomes_data = {}

    def bet(self, quality_tests, previous_round_results, money):
        self.update_historical_income(previous_round_results, self.previous_tests)
        self.previous_tests = quality_tests
        self.previous_results.append(previous_round_results)

        my_bet = self.calculate_bets(quality_tests)

        self.my_bets.append(my_bet)

        return my_bet

    def calculate_bets(self, quality_tests):
        prognoses = [(test.mine_id, self.coal_market_valuation(test), self.historical_income(test.mine_id, test.pure_coal_percentage)) for test in quality_tests]

        prognoses.sort(key=lambda x: x[2])

        my_bet = [
            Bet(
                prognosis[0],
                prognosis[1] / 2 + uniform(50.0, 500.0),
                index
            ) for index, prognosis in enumerate(prognoses)
        ]

        return my_bet
    
    def historical_income(self, mine_id, prognosis):
        if mine_id not in self.incomes_data.keys() or len(self.incomes_data[mine_id]) < 3:
            return 0

        income_data = self.incomes_data[mine_id]
        x = [data[1] for data in income_data] # quality tests
        y = [data[0] for data in income_data] # acutal income
        result = linregress(x, y)
        return result.intercept + prognosis*result.slope
    
    def update_historical_income(self, results, tests):
        if results is None:
            return

        for _, result in results.winners.items():
            bet, income, mine_id = result['bet'], result['income'], result['mine_id']
            actual_income = income - bet
            self.incomes_data[mine_id] = self.incomes_data.get(mine_id, [])
            self.incomes_data[mine_id].append((actual_income, tests[mine_id].pure_coal_percentage))
