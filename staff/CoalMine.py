from random import uniform, gauss
from scipy.stats import truncnorm

from staff.CoalTransport import CoalTransport
from staff.QualityTest import QualityTest


class CoalMine:
    def __init__(self, mine_id, coal_distribution):
        self.mine_id = mine_id
        self.pure_coal_percentage = coal_distribution.rvs(size=1)[0]  # uniform(20.0, 95.0)
        self.deviation = uniform(2.5, 15.0)
        self.coal_distribution = truncnorm(
            (10.0 - self.pure_coal_percentage) / self.deviation,
            (99.0 - self.pure_coal_percentage) / self.deviation,
            loc=self.pure_coal_percentage,
            scale=self.deviation
        )

        self.next_ore = self._dig()

    def _dig(self):
        pure_coal_percentage_in_ore = self.coal_distribution.rvs(size=1)[0]

        return CoalTransport(self.mine_id, pure_coal_percentage_in_ore, 100.0 - pure_coal_percentage_in_ore)

    def test_ore(self):
        pure_coal_percentage_in_ore = min(
            99.0,
            max(
                1.0,
                self.next_ore.pure_coal_percentage - gauss(0.0, self.deviation)
            )
        )
        return QualityTest(self.mine_id, pure_coal_percentage_in_ore, 100.0 - pure_coal_percentage_in_ore)

    def get_ore(self):
        ore = self.next_ore

        self.next_ore = self._dig()

        return ore
