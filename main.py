import sys

from staff.AuctionWorld import AuctionWorld

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--turn_limit', '-t', help='How many time steps?', type=int)
parser.add_argument('--destination', '-d', help='Where to save the figure?', type=str)
args = parser.parse_args()
d_args = vars(args)
turn_limit = 100 if d_args['turn_limit'] is None else d_args['turn_limit']
destination = d_args['destination']

if __name__ == '__main__':
    auction = AuctionWorld(turn_limit=turn_limit)

    # There should be as many mines as players
    auction.create_mines()

    # Calculate how well they do
    auction.simulate()

    # Show the resulting plot
    auction.display(destination=destination)
