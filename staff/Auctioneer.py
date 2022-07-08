from random import choice

from staff.CoalMarket import CoalMarket
from staff.RoundResults import RoundResults


class Auctioneer:
    @staticmethod
    def auction(ores, bets, money):
        minimal_bet = 10.0
        result = RoundResults()

        for player_id in bets.keys():
            bets[player_id].sort(key=lambda x: x.reverse_priority, reverse=True)

        for priority_index in range(len(ores)):
            current_auction = {}
            for player_id, player_bets in bets.items():
                if player_bets[priority_index].mine_id in current_auction:
                    current_auction[player_bets[priority_index].mine_id].append(
                        (
                            player_id,
                            player_bets[priority_index]
                        )
                    )
                else:
                    current_auction[player_bets[priority_index].mine_id] = [
                        (
                            (
                                player_id,
                                player_bets[priority_index]
                            )
                        )
                    ]

            for mine_id in current_auction.keys():
                ore = [o for o in ores if o.mine_id == mine_id][0]

                auction_players = current_auction[mine_id]

                auction_winnning_candidate = max(auction_players, key=lambda x: x[1].bet_amount)

                auction_winner_candidates = [
                    p for p in auction_players if p[1].bet_amount == auction_winnning_candidate[1].bet_amount
                ]

                if auction_winner_candidates:
                    auction_winner = choice(auction_winner_candidates)

                    if auction_winner[1].bet_amount >= minimal_bet:

                        result.add(
                            auction_winner[0],
                            auction_winner[1].bet_amount,
                            CoalMarket.calculate_value(ore),
                            mine_id
                        )

                        money[auction_winner[0]] -= auction_winner[1].bet_amount
                        money[auction_winner[0]] += CoalMarket.calculate_value(ore)

                        if money[auction_winner[0]] < 0.0:
                            money[auction_winner[0]] *= 1.01

                        del bets[auction_winner[0]]

        return result, money

    @staticmethod
    def auction_old(ores, bets, money):
        minimal_bet = 10.0
        result = RoundResults()

        for player_id in bets.keys():
            bets[player_id].sort(key=lambda x: x.reverse_priority)

        for priority_index in range(len(ores)):
            current_auction = {}
            for player_id, player_bets in bets.items():
                if player_bets[priority_index].mine_id in current_auction:
                    current_auction[player_bets[priority_index].mine_id].append(
                        (
                            player_id,
                            player_bets[priority_index]
                        )
                    )
                else:
                    current_auction[player_bets[priority_index].mine_id] = [
                        (
                            (
                                player_id,
                                player_bets[priority_index]
                            )
                        )
                    ]

            for mine_id in current_auction.keys():
                ore = [o for o in ores if o.mine_id == mine_id][0]

                auction_players = current_auction[mine_id]

                auction_winnning_candidate = max(auction_players, key=lambda x: x[1].bet_amount)

                auction_winner_candidates = [
                    p for p in auction_players if p[1].bet_amount == auction_winnning_candidate[1].bet_amount
                ]

                if auction_winner_candidates:
                    auction_winner = choice(auction_winner_candidates)

                    if auction_winner[1].bet_amount >= minimal_bet:

                        result.add(
                            auction_winner[0],
                            auction_winner[1].bet_amount,
                            CoalMarket.calculate_value(ore),
                            mine_id
                        )

                        money[auction_winner[0]] -= auction_winner[1].bet_amount
                        money[auction_winner[0]] += CoalMarket.calculate_value(ore)

                        if money[auction_winner[0]] < 0.0:
                            money[auction_winner[0]] *= 1.01

                        del bets[auction_winner[0]]

        return result, money
