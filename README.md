# Coal Auction KOTH

## Rules

### General KOTH rules

You can create any number of bots, but they can not collude.

Every bot has only one instance of itself.

If the total simulation time exceedes one minute per bot, the slowest bot will be excluded from the simulation.

### Information rules

Your bot can only use information provided to it in its parameters or in its internal state.

Do not use reflection or similar mechanisms.

Do not use external libraries. Exception: `scipy`.

## The Coal Auction game

Welcome to the coal market of P*land, a country where coal is king. The coal trade is highly regulated and subject 
to some arcane rules.

The time here is not divided into days, months and years, but into time steps, set up so every coal mine in the country 
can extract exactly one standard coal transport out of the earth. Every time step, coal companies, of which there is the
same amount as mines (additional ones do not get business licences), bid in P*lish auction to acquire coal from 
the mines to sell on the market.

The rules of the P*lish auction are as such: every company, based on the reports of government coal examiners, place
bet list to the auction house. They must bet on every coal transport, but shall acquire only one of them. To each bet
they attach a bet value, which specifies how much they will pay, and a reverse priority value, which specifies how
important a given transport is to them (bigger value means higher priority).

The government auctioneer then taken in the bet lists and arranges them by their priorities. He takes the highest 
priority bet from every company and groups them by the transport that was bet on. Then, the company that has placed the 
biggest bet on that transport is forced to pay its bet amount and given the transport. Ties are broken randomly. All of
that company's bets are removed from the running and the auctioneer moves on to the next bets in priority order. 
The process repeats until all the transports have found their owners.

There is an exception, however: if the winning bet is lower than `10`, then the transaction does not go through. 
That can lead to a transport being unsold. Such a transport is ceremonially burned as an offering to the Coal Gods.

## How to create a bot

### Short version

In short: create a bot inheriting from `BaseBot`. Implement 
`bet(quality_tests: List[QualityTest], previous_round_results: RoundResults, money: float)` in your bot. Put your bot
in `bots` package (you can create you own subpackage inside it, but keep the main bot file in `bots/`). 
Import the bot in `AuctionWorld.py` according to the template `from bots import <BotName>`. That's all!

### Long version

The key to victory lies in `bet(quality_tests: List[QualityTest], previous_round_results: RoundResults, money: float)`.

Each round, you'll be provided with `RoundResults` object, which contains a `winners` dictionary. Inside it there are 
`world_id`s of bots used as keys, with dictionary of closed bets. That dictionary consists of three keys: `bet`, which
hold how much given player paid for the `CoalTransport`, `income`, which tells you how much given player got on the 
`CoalMarket` for the `CoalTransport` and `mine_id`, which holds information about which `CoalMine` provided that 
`CoalTransport`. You would do well to keep that information in your bot in some way.

You will also be provided with `money` information, which tells you how much money your company currently hold. Don't
worry - if it  falls below `0`, you can still trade on a credit. Remember, however, that if you go into the red, your
company will be forced to pay `1%` of its debt amount each time step, for debt servicing.

Lastly, you are provided with a `list` of `QualityTest`s. This gives you information, although imperfect, about the
`CoalTransport`s on the market. Each `CoalMine` has a base percentage of pure coal in its ore veins: between 
`20%` and `95%`, distributed with a truncated normal distribution. Average coal percentage is `55%` 
with standard deviation of `20`.
Also, each mine has its `deviation`, which specifies the standard deviation between the veins in the mine.
It ranges from `2` to `15` with uniform distribution.
After a mine extracts a single `CoalTransport` it deviates with bounds of `10%` and `99%`, 
with truncated normal distribution centered on the base percentage of pure coal for the mine with provided `deviation`. 
Then the `CoalTransport` is inspected to know how much pure coal is inside it. 
The test takes a sample, thus the `QualityTest` deviates from the `CoalTransport` percentage 
with normal distribution centered on `0` with provided `deviation`. The tests are 'sanity-checked' by the testators: 
pure coal percentages over `99%` are set to `99%`, pure coal percentages below `1%` are set to `1%`.
The test has three self-explanatory fields: `mine_id`, `pure_coal_percentage`, `scum_coal_percentage`.

No `CoalTransport` can have more than `99%` of pure coal nor can it have less than `10%` of pure coal. No `QualityTest`
will report more than `99%` of pure coal nor will it report less than `1%` of pure coal.

The `bet()` needs to return a list of `Bet`s. Every bet needs `mine_id`, `bet_amount` and `reverse_priority`. `mine_id`
specifies on which `CoalTransport` the bot is betting, `bet_amount` specifies how much they will pay and 
`reverse_priority` specifies how important a given `CoalTransport` is to the bot.

You should have one `Bet` per `CoalTransport`. Your `reverse_priorities` should be injective (do not repeat values).
`bet_amount`s should be higher than `10`.

Your bot also has access to `CoalMarket` information about coal prices. They do not change in the current version. To
know how much a `CoalTransport` with qualities specified with a `QualityTest` would be worth, use 
`self.coal_market_valuation(QualityTest)`. That function accepts `QualityTest`s, `CoalTransport`s, `CoalInfo`s.

## Coal distribution quick reference

|                       	| lower bound 	| upper bound 	|   distribution   	|       mean       	|      std dev     	| additional info                                                                    	|
|-----------------------	|:-----------:	|:-----------:	|:----------------:	|:----------------:	|:----------------:	|------------------------------------------------------------------------------------	|
| `vein deviation`      	|     `2`     	|     `15`    	|      uniform     	|                  	|                  	|                                                                                    	|
| `base pure coal`      	|    `20%`    	|    `95%`    	| truncated normal 	|       `55%`      	|       `20`       	|                                                                                    	|
| `transport pure coal` 	|    `10%`    	|    `99%`    	| truncated normal 	| `base pure coal` 	| `vein deviation` 	|                                                                                    	|
| `testing error`       	|             	|             	|      normal      	|        `0`       	| `vein deviation` 	|                                                                                    	|
| `tested pure coal`    	|     `1%`    	|    `99%`    	|                  	|                  	|                  	| `transport pure coal` - `testing error`, values out of bounds set to closest bound 	|
