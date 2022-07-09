from staff.AuctionWorld import AuctionWorld

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--turn_limit', '-t', help='How many time steps?', type=int)
parser.add_argument('--destination', '-d', help='Where to save the figure?', type=str)
parser.add_argument('--n_episodes', '-e', help='How many episodes?', type=int)
args = parser.parse_args()
d_args = vars(args)
turn_limit = 100 if d_args['turn_limit'] is None else d_args['turn_limit']
destination = d_args['destination']
n_episodes = 1 if d_args['n_episodes'] is None else d_args['n_episodes']

if __name__ == '__main__':
    winners = {}
    for i in range(n_episodes):
        auction = AuctionWorld(turn_limit=turn_limit)

        # There should be as many mines as players
        auction.create_mines()

        # Calculate how well they do
        auction.simulate()

        winner_id = list(sorted(auction.player_money.items(), key=lambda x: x[1]))[-1][0]
        winner_name = auction.players[winner_id].name
        winners[winner_name] = winners.get(winner_name, 0) + 1
    
    print(winners)
