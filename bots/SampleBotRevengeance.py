import math
from random import uniform, gauss

from bots.BaseBot import BaseBot
from staff.Bet import Bet
from staff.CoalInfo import CoalInfo


class SampleBotRevengeance(BaseBot):
    def __init__(self, bot_id, coal_market_valuation):
        super().__init__(bot_id, coal_market_valuation)

        self.my_bets = []
        self.previous_results = []
        self.name = 'SampleBotRevengeance'

        self.mines = {}

    def update_internal_information(self, quality_tests, previous_round_results, money):
        self.previous_results.append(previous_round_results)

        for test in quality_tests:
            if test.mine_id not in self.mines:
                self.mines[test.mine_id] = {}
            if 'pure_list' not in self.mines:
                self.mines[test.mine_id]['pure_list'] = []
            self.mines[test.mine_id]['pure_list'].append(test.pure_coal_percentage)

            self.mines[test.mine_id]['average_purity'] = sum(
                self.mines[test.mine_id]['pure_list']
            ) / len(self.mines[test.mine_id]['pure_list'])

            self.mines[test.mine_id]['deviation'] = max(2.5, min(15.0, math.sqrt(
                ((
                    sum(
                        [p ** 2 for p in self.mines[test.mine_id]['pure_list']]
                    ) - (
                        (sum(self.mines[test.mine_id]['pure_list']) ** 2) / (len(self.mines[test.mine_id]['pure_list']))
                    )
                ) / (max(1, len(self.mines[test.mine_id]['pure_list']) - 1))) / 2
            )))

    def bet(self, quality_tests, previous_round_results, money):
        self.update_internal_information(quality_tests, previous_round_results, money)

        my_bet = self.calculate_bets(quality_tests)

        self.my_bets.append(my_bet)

        return my_bet

    def get_prognoses(self, quality_tests):
        return [
            (
                test.mine_id,
                self.coal_market_valuation(
                    CoalInfo(
                        test.mine_id,
                        test.pure_coal_percentage - gauss(0, self.mines[test.mine_id]['deviation']),
                        100.0
                    )
                )
            ) for test in quality_tests
        ]

    def get_bet_value(self, prognosis):
        return prognosis[1] / (self.mines[prognosis[0]]['deviation'] * 100)  # 2 - uniform(tenth, tenth + tenth * self.mines[prognosis[0]]['deviation'])

    def calculate_bets(self, quality_tests):
        prognoses = self.get_prognoses(quality_tests)

        prognoses.sort(key=lambda x: x[1])

        my_bet = [
            Bet(
                prognosis[0],
                self.get_bet_value(prognosis),
                index
            ) for index, prognosis in enumerate(prognoses)
        ]

        return my_bet
