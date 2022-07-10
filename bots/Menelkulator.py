from random import uniform
import random
from decimal import Decimal

from bots.BaseBot import BaseBot
from staff.Bet import Bet


class XXXampleBot(BaseBot):

    def __init__(self, bot_id, coal_market_valuation):
        super().__init__(bot_id, coal_market_valuation)

        self.my_bets = []
        self.previous_results = []
        self.name = 'Menelkulator'
        self.sumowanskoraz = []
        self.sumowanskodwa = []
        self.sumowanskotrzy = []
        self.sumowanskocztery = []
        for x in range(1, 32):
            self.sumowanskoraz.append(0.000000001)
            self.sumowanskodwa.append(0.0)
            self.sumowanskotrzy.append(0)
            self.sumowanskocztery.append(0.0)
        self.zima = 0

    def bet(self, quality_tests, previous_round_results, money):
        self.zima = self.zima + 1
        if previous_round_results is not None:
            for (k,result) in previous_round_results.winners.items():
                self.sumowanskoraz[result['mine_id']] = self.sumowanskoraz[result['mine_id']] + result['income']
                self.sumowanskodwa[result['mine_id']] = self.sumowanskodwa[result['mine_id']] + result['bet']
                self.sumowanskotrzy[result['mine_id']] = self.sumowanskotrzy[result['mine_id']] + 1
        if self.zima < 10:
            prognoses = [(test.mine_id, self.coal_market_valuation(test)) for test in quality_tests]
        else:
            prognoses = []
            for test in quality_tests:
                if(self.sumowanskotrzy[test.mine_id] > 0):
                    prognoses.append((test.mine_id, self.sumowanskoraz[test.mine_id]/self.sumowanskotrzy[test.mine_id]))
                else:
                    prognoses.append((test.mine_id, self.coal_market_valuation(test) / 100.0))

        for test in quality_tests:
            self.sumowanskocztery[test.mine_id] = self.coal_market_valuation(test) * 0.01



        prognoses.sort(key=lambda x: x[1])
        betsy = []
        for index, prognosis in enumerate(prognoses):
            zlocisze = 10.1
            if self.sumowanskotrzy[prognosis[0]] > 0:
                zlocisze = max(10.1, ((Decimal(self.sumowanskoraz[prognosis[0]]) / Decimal(self.sumowanskotrzy[prognosis[0]])) + Decimal(10241.01)*(Decimal(self.sumowanskodwa[prognosis[0]]) / Decimal(self.sumowanskotrzy[prognosis[0]])))/Decimal(10252.01))
                zlocisze = min(zlocisze, self.sumowanskocztery[prognosis[0]])
            betsy.append(Bet(prognosis[0], float(zlocisze), index))

        return betsy
