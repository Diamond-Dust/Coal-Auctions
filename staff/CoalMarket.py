from staff.CoalInfo import CoalInfo


class CoalMarket:
    @staticmethod
    def calculate_value(transport: CoalInfo):
        # anthracite (40000-55000)
        if transport.pure_coal_percentage >= 86.0:
            return 40_000 + 15_000 * (transport.pure_coal_percentage - 86.0) / 14.0
        # bituminous (17500-30000)
        if transport.pure_coal_percentage >= 45.0:
            return 17_500 + 12_500 * (transport.pure_coal_percentage - 45.0) / 41.0
        # subbituminous (8000-15000)
        if transport.pure_coal_percentage >= 35.0:
            return 8_000 + 7_000 * (transport.pure_coal_percentage - 35.0) / 10.0
        # lignite (2500-6000)
        if transport.pure_coal_percentage >= 25.0:
            return 2_500 + 3_500 * (transport.pure_coal_percentage - 25.0) / 10.0
        # trash
        return 100
