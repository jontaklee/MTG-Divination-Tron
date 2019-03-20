# Modern-Tron-Mulligans

The Modern Tron deck relies on assembling Urza's Mine, Urza's Tower, and Urza's Power Plant in play as 
early as possible. This combination, termed 'Tron', is ideally achieved by the third or fourth turn of the game.

Because assembling this combination of lands is so important to the deck's functionality, players are incentivized 
to mulligan hands that cannot assemble Tron within the first several turns. With the introduction of the [London mulligan](https://magic.wizards.com/en/articles/archive/competitive-gaming/mythic-championship-ii-format-and-london-test-2019-02-21), 
Tron players are faced with potentially new optimal mulligan decisions.

### Mulligan for achieving a turn 3 Tron

The mulligan_sim.py file simulates mulliganing with the Tron deck using the London and [Paris mulligan](https://mtg.fandom.com/wiki/Paris_mulligan) rules.
This program only takes into account starting hands that can guarantee assembling Tron by turn 3.

### Optimal mulligan decisions when Tron is not guaranteed (WIP)

Determining whether to mulligan hands that do not immediately achieve Tron requires simulated games involving those starting hands.

The vancouver.py script simulates playing until all three Tron lands are in play, and outputs the starting hand and turn when Tron was achieved. Methods for each card and the deck are found in the card_classes.py file.

#### Work in Progress:
Future work will involve training a machine learning model to predict the turn at which a hand achieves Tron, to make optimal mulligan decisions. This will also be used to compare the success rate between the Vancouver and London mulligans for all hands, rather than just those that start with Tron in the starting hand.





Magic: The Gathering is property of Hasbro
