class RoundResults:
    def __init__(self):
        self.winners = {}

    def add(self, winner, bet_amount, value, mine_id):
        self.winners[winner] = {
            'bet': bet_amount,
            'income': value,
            'mine_id': mine_id
        }
