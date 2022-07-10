import math
from random import uniform, gauss, choice

import matplotlib.pyplot as plt
from scipy.stats import truncnorm

from bots.BaseBot import BaseBot
from staff.Bet import Bet
from staff.CoalInfo import CoalInfo


class SampleBot3(BaseBot):
    ε = 0.00001
    fl = 10.0
    mem_cap = 100

    def __init__(self, bot_id, coal_market_valuation):
        super().__init__(bot_id, coal_market_valuation)

        self.my_bets = []
        self.previous_results = []
        self.name = 'SampleBot3'

        self.time = 0
        self.mines = {}
        self.players = {}

    def _update_internal_information(self, quality_tests, previous_round_results, money):
        if previous_round_results is not None:
            self.previous_results.append(previous_round_results)
            for player_id in previous_round_results.winners.keys():
                if 'bet_wins' not in self.mines[previous_round_results.winners[player_id]['mine_id']]:
                    self.mines[previous_round_results.winners[player_id]['mine_id']]['bet_wins'] = []
                self.mines[previous_round_results.winners[player_id]['mine_id']]['bet_wins'].append(
                    (
                        self.mines[previous_round_results.winners[player_id]['mine_id']]['pure_list'][-1],
                        previous_round_results.winners[player_id]['bet'],
                        self.time
                    )
                )
                self.mines[previous_round_results.winners[player_id]['mine_id']]['bet_wins'].sort(
                    key=lambda x: x[2],
                    reverse=True
                )
                self.mines[previous_round_results.winners[player_id]['mine_id']]['bet_wins'] = \
                    self.mines[previous_round_results.winners[player_id]['mine_id']]['bet_wins'][:SampleBot3.mem_cap]
                self.mines[previous_round_results.winners[player_id]['mine_id']]['bet_wins'].sort(key=lambda x: x[0])

                if player_id not in self.players:
                    self.players[player_id] = {}
                if 'bet_wins' not in self.players[player_id]:
                    self.players[player_id]['bet_wins'] = []

                self.players[player_id]['bet_wins'].append(
                    (
                        self.mines[previous_round_results.winners[player_id]['mine_id']]['pure_list'][-1],
                        previous_round_results.winners[player_id]['bet'],
                        self.time
                    )
                )
                self.players[player_id]['bet_wins'].sort(key=lambda x: x[2], reverse=True)
                self.players[player_id]['bet_wins'] = self.players[player_id]['bet_wins'][:SampleBot3.mem_cap]
                self.players[player_id]['bet_wins'].sort(key=lambda x: x[0])

        for test in quality_tests:
            if test.mine_id not in self.mines:
                self.mines[test.mine_id] = {}
            if 'pure_list' not in self.mines[test.mine_id]:
                self.mines[test.mine_id]['pure_list'] = []
            if 'average_purity_list' not in self.mines[test.mine_id]:
                self.mines[test.mine_id]['average_purity_list'] = []
            if 'deviation_list' not in self.mines[test.mine_id]:
                self.mines[test.mine_id]['deviation_list'] = []
            self.mines[test.mine_id]['pure_list'].append(test.pure_coal_percentage)

            self.mines[test.mine_id]['average_purity'] = sum(
                self.mines[test.mine_id]['pure_list']
            ) / len(self.mines[test.mine_id]['pure_list'])

            self.mines[test.mine_id]['average_purity_list'].append(self.mines[test.mine_id]['average_purity'])

            self.mines[test.mine_id]['deviation'] = max(2.5, min(15.0, math.sqrt(
                ((
                         sum(
                             [p ** 2 for p in self.mines[test.mine_id]['pure_list']]
                         ) - (
                                 (sum(self.mines[test.mine_id]['pure_list']) ** 2) /
                                 (len(self.mines[test.mine_id]['pure_list']))
                         )
                 ) / (max(1, len(self.mines[test.mine_id]['pure_list']) - 1))) / 2
            )))

            self.mines[test.mine_id]['deviation_list'].append(self.mines[test.mine_id]['deviation'])

        self.time += 1

    def bet(self, quality_tests, previous_round_results, money):
        self._update_internal_information(quality_tests, previous_round_results, money)

        my_bet = self._calculate_bets(quality_tests)

        self.my_bets.append(my_bet)

        return my_bet

    def _return_to_mean(self, percentage_value, mine_id):
        p = truncnorm(
            (10.0 - self.mines[mine_id]['average_purity']) / self.mines[mine_id]['deviation'],
            (99.0 - self.mines[mine_id]['average_purity']) / self.mines[mine_id]['deviation'],
            loc=self.mines[mine_id]['average_purity'],
            scale=self.mines[mine_id]['deviation']
        )

        if p.pdf(percentage_value) < 0.005:
            return self.mines[mine_id]['average_purity']

        rnd = gauss(0, self.mines[mine_id]['deviation'])
        if percentage_value > self.mines[mine_id]['average_purity']:
            return percentage_value - math.fabs(rnd)
        elif percentage_value < self.mines[mine_id]['average_purity']:
            return percentage_value + math.fabs(rnd)
        else:
            return percentage_value - rnd

    def _get_prognoses(self, quality_tests):
        return [
            (
                test.mine_id,
                self.coal_market_valuation(
                    CoalInfo(
                        test.mine_id,
                        self._return_to_mean(test.pure_coal_percentage, test.mine_id),
                        100.0
                    )
                ),
                test.pure_coal_percentage
            ) for test in quality_tests
        ]

    def _get_bet_value(self, prognosis):
        return prognosis[3]

    def __presume_minimal_bet_naive_linear(self, bet_list, test_pure_percentage):
        if len(bet_list) < 1:
            return SampleBot3.fl + SampleBot3.ε
        else:
            x_min = 1.0
            y_min = SampleBot3.fl
            if test_pure_percentage >= bet_list[-1][0]:
                return bet_list[-1][1] + SampleBot3.ε
            else:
                for test_purity, bet, _ in bet_list:
                    if test_pure_percentage < test_purity:
                        return y_min \
                               + (
                                       (bet - y_min) * ((test_pure_percentage - x_min) / (test_purity - x_min))
                               ) \
                               + SampleBot3.ε
                    y_min = bet
                    x_min = test_purity

    def _presume_nominal_bets(self, quality_tests):
        all_nominal_bets = {}
        all_bets = {}
        for player_id in self.players.keys():
            if player_id != self.bot_id:
                all_bets[player_id] = []
                for mine_id in self.mines.keys():
                    mine_test = [t for t in quality_tests if t.mine_id == mine_id][0]
                    all_bets[player_id].append(
                        {
                            'player_id': player_id,
                            'mine_id': mine_id,
                            'bet': self.__presume_minimal_bet_naive_linear(
                                self.players[player_id]['bet_wins'],
                                mine_test.pure_coal_percentage
                            )
                        }
                    )
                all_bets[player_id].sort(key=lambda x: x['bet'], reverse=True)

        bets_grouped_by_priority = list(zip(*all_bets.values()))
        already_won = []

        for bets in bets_grouped_by_priority:
            current_auction = {}
            for bet in bets:
                if bet['mine_id'] in current_auction:
                    current_auction[bet['mine_id']].append(
                        (
                            bet['player_id'],
                            bet['bet']
                        )
                    )
                else:
                    current_auction[bet['mine_id']] = [
                        (
                            (
                                bet['player_id'],
                                bet['bet']
                            )
                        )
                    ]

            for mine_id in current_auction.keys():
                if mine_id in all_nominal_bets:
                    continue

                auction_players = [bet for bet in current_auction[mine_id] if bet[0] not in already_won]

                if not auction_players:
                    continue

                auction_winnning_candidate = max(auction_players, key=lambda x: x[1])

                auction_winner_candidates = [
                    p for p in auction_players if p[1] == auction_winnning_candidate[1]
                ]

                if auction_winner_candidates:
                    auction_winner = choice(auction_winner_candidates)

                    if auction_winner[1] >= 10.0:

                        all_nominal_bets[mine_id] = auction_winner[1] + SampleBot3.ε

                        already_won.append(auction_winner[0])

        return all_nominal_bets

    def _arrange_prognoses(self, prognoses, quality_tests):
        nominals = self._presume_nominal_bets(quality_tests)

        prognoses = [
            (
                mine_id,
                self.coal_market_valuation(
                    CoalInfo(
                        mine_id,
                        self.mines[mine_id]['average_purity'],
                        100.0)
                ) if 0 < len(self.previous_results) < 5 else true_valuation,
                test_pure_percentage,
                nominals[mine_id] if mine_id in nominals else self.__presume_minimal_bet_naive_linear(
                    self.mines[mine_id]['bets_value'] if (
                            mine_id in self.mines and 'bets_value' in self.mines[mine_id]
                    ) else [],
                    test_pure_percentage
                )
            ) for mine_id, true_valuation, test_pure_percentage in prognoses
        ]

        prognoses.sort(
            key=lambda x: x[1] - x[3]
        )

        return prognoses

    def _calculate_bets(self, quality_tests):
        prognoses = self._get_prognoses(quality_tests)

        prognoses = self._arrange_prognoses(prognoses, quality_tests)

        my_bet = [
            Bet(
                prognosis[0],
                self._get_bet_value(prognosis),
                index
            ) for index, prognosis in enumerate(prognoses)
        ]

        return my_bet
