from staff.CoalInfo import CoalInfo


class CoalTransport(CoalInfo):
    def __init__(self, mine_id, pure_coal, scum_coal):
        super().__init__(mine_id, pure_coal, scum_coal)
