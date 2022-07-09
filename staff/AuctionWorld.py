from copy import copy

import matplotlib.pyplot as plt
from scipy.stats import truncnorm

from bots import *

from bots.SampleBot import SampleBot
from bots.BaseBot import BaseBot
from bots.MarstarsTestBot import MarstarsTestBot
from bots.Twojstarybot import TwojStaryBot
from staff.Auctioneer import Auctioneer
from staff.CoalMarket import CoalMarket
from staff.CoalMine import CoalMine


class AuctionWorld:
    def _initialise_bots(self):
        # Initialise the bots
        for cls in BaseBot.__subclasses__():
            self.players.append(cls(self.id_counter_players, CoalMarket.calculate_value))
            self.player_money[self.id_counter_players] = 100_000
            self.id_counter_players += 1

    def __init__(self, turn_limit=100):
        self.mines = []
        self.players = []
        self.player_money = {}
        self.money_history = []
        self.ore_history = []
        self.test_history = []
        self.id_counter_players = 0
        self.turn_limit = turn_limit
        self.coal_distribution = truncnorm(
            (20.0 - 55.0) / 20.0,
            (95.0 - 55.0) / 20.0,
            loc=55.0,
            scale=20.0
        )

        self._initialise_bots()

    def create_mines(self):
        for i in range(len(self.players)):
            self.mines.append(CoalMine(i, self.coal_distribution))

    def simulate(self):
        previous_round_results = None
        for turn_counter in range(self.turn_limit):
            quality_tests = [mine.test_ore() for mine in self.mines]

            bets = {
                player.bot_id: player.bet(
                    copy(quality_tests),
                    copy(previous_round_results),
                    self.player_money[player.bot_id]
                ) for player in self.players
            }

            ores = [mine.get_ore() for mine in self.mines]

            previous_round_results, new_money = Auctioneer.auction(ores, bets, self.player_money)

            self.money_history.append(copy(self.player_money))
            self.ore_history.append(copy(ores))
            self.test_history.append(copy(quality_tests))

            self.player_money = new_money

    def display(self, destination=None):
        def _formatter(x_val, pos):
            if -1_000 < x_val < 1_000:
                return str(round(x_val, 1))
            elif x_val >= 1_000_000_000_000 or x_val <= -1_000_000_000_000:
                return str(round(x_val / 1e12, 1)) + " bln"
            elif x_val >= 1_000_000_000 or x_val <= -1_000_000_000:
                return str(round(x_val / 1e9, 1)) + " mld"
            elif x_val >= 1_000_000 or x_val <= -1_000_000:
                return str(round(x_val / 1e6, 1)) + " mln"
            elif x_val >= 1_000 or x_val <= -1_000:
                return str(round(x_val / 1e3, 1)) + " thd"

        fig, axs = plt.subplots(2, 1, figsize=(22, 11))
        plt.tight_layout()
        plt.subplots_adjust(left=0.05, bottom=0.05)

        x = [index for index in range(self.turn_limit)]

        for player in self.players:
            y = [step[player.bot_id] for step in self.money_history]

            axs[0].plot(x, y, label=player.name)

        axs[0].yaxis.set_major_formatter(_formatter)
        axs[0].set_title('Company valuations')
        axs[0].set_xlabel('Time steps', y=0.15)
        axs[0].set_ylabel('Company value')
        axs[0].grid(True)

        axs[0].legend()
        axs[0].set_xlim(left=0, right=self.turn_limit-1)

        for mine in self.mines:
            y = [
                step[i].pure_coal_percentage for step in self.ore_history \
                for i in range(len(step)) if step[i].mine_id == mine.mine_id
            ]

            y_test = [
                step[i].pure_coal_percentage for step in self.test_history \
                for i in range(len(step)) if step[i].mine_id == mine.mine_id
            ]

            yerr = [
                [y[i] - y_test[i] if y_test[i] - y[i] < 0 else 0 for i in range(self.turn_limit)],
                [y_test[i] - y[i] if y_test[i] - y[i] > 0 else 0 for i in range(self.turn_limit)]
            ]

            (_, caps, _) = axs[1].errorbar(
                x,
                y,
                yerr=yerr,
                fmt='p',
                markersize=8,
                capsize=4,
                elinewidth=1
            )

            for cap in caps:
                cap.set_markeredgewidth(1)

        axs[1].set_title('Mine ore qualities', y=-0.1)
        axs[1].set_ylabel('Pure coal %')
        axs[1].xaxis.tick_top()
        axs[1].grid(True)

        axs[1].set_xlim(left=0, right=self.turn_limit-1)
        axs[1].set_ylim(top=100.0, bottom=0.0)
        axs[1].get_xaxis().set_ticklabels([])

        if destination is None:
            plt.show()
        else:
            plt.savefig(destination)
            plt.close()

