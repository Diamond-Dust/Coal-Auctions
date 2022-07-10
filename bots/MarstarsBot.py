import math
from random import uniform

from bots.BaseBot import BaseBot
from staff.Bet import Bet
from staff.CoalInfo import CoalInfo


class MarstarsBot(BaseBot):
    # TODO: clear licensing issues
    def __init__(self, bot_id, coal_market_valuation):
        super().__init__(bot_id, coal_market_valuation)

        # self.my_bets = []
        # self.previous_results = []
        self.name = '/api/v1/MarstarsBot'

        self.mines = {}

    # it's not stolen I promise
    def update_internal_information(self, quality_tests):
        # self.previous_results.append(previous_round_results)

        for test in quality_tests:
            if test.mine_id not in self.mines:
                self.mines[test.mine_id] = {}
            if 'pure_list' not in self.mines:
                self.mines[test.mine_id]['pure_list'] = []
            self.mines[test.mine_id]['pure_list'].append(test.pure_coal_percentage)

            self.mines[test.mine_id]['average_purity'] = sum(
                self.mines[test.mine_id]['pure_list']
            ) / len(self.mines[test.mine_id]['pure_list'])

            # self.mines[test.mine_id]['deviation'] = max(2.5, min(15.0, math.sqrt(
            #     ((
            #         sum(
            #             [p ** 2 for p in self.mines[test.mine_id]['pure_list']]
            #         ) - (
            #             (sum(self.mines[test.mine_id]['pure_list']) ** 2) / (len(self.mines[test.mine_id]['pure_list']))
            #         )
            #     ) / (max(1, len(self.mines[test.mine_id]['pure_list']) - 1))) / 2
            # )))

    def bet(self, quality_tests, previous_round_results, money):
        self.update_internal_information(quality_tests)

        my_bet = self.calculate_bets(previous_round_results, quality_tests)

        # self.my_bets.append(my_bet)

        return my_bet

    def calculate_bets(self, prevres, quality_tests):
        stuff_to_bet = []
        if prevres is not None:
            for winner, winner_val in prevres.winners.items():
                my_value_for_mine = self.coal_market_valuation(CoalInfo(
                    "mine deez nuts",
                    self.mines[winner_val['mine_id']]['average_purity'],
                    1e+04))
                betvalue = winner_val['bet'] + 300
                getmoney = my_value_for_mine - betvalue
                if (getmoney < 0):
                    betvalue = 25
                stuff_to_bet.append([winner_val['mine_id'], betvalue, getmoney])
                
            stuff_to_bet.sort(key=lambda x: x[2])
            my_bet = [
                Bet(
                    stuff[0],
                    stuff[1],
                    index
                ) for index, stuff in enumerate(stuff_to_bet)
            ]
        else:
            my_bet = [
                Bet(
                    stuff.mine_id,
                    25,
                    index
                ) for index, stuff in enumerate(quality_tests)
            ]
        
        # wrzuć procenty do waluacji
        # policz roznice miedzy waluacja a bet i income poprzednich graczy
        # gdzie jest ewidentny zysk takie bety i priorytety nadaj
        
        # 1. self.coal_market_valuation(self.mines[test.mine_id]['average_purity']) // typy ew.
        # potencjalny zysk = moja waluacja - ostatni bet - leeway zeby przebic aukcje
        # sort po potencjalnych zyskach i priority adekwatnie

        return my_bet