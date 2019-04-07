# Modern-Tron-Mulligans

A *Magic the Gathering* Simulator and Decision Optimizer

The Modern Tron deck relies on assembling Urza's Mine, Urza's Tower, and Urza's Power Plant in play as 
early as possible. This combination, termed 'Tron', is ideally achieved by the third or fourth turn of the game.
<br><br>

![Urza's Mine](http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=83314&type=card)
![Urza's Tower](http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=83316&type=card)
![Urza's Power Plant](http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=83315&type=card)

Because assembling this combination of lands is so important to the deck's functionality, players are incentivized 
to mulligan hands that cannot assemble Tron within the first several turns. With the introduction of the [London mulligan](https://magic.wizards.com/en/articles/archive/competitive-gaming/mythic-championship-ii-format-and-london-test-2019-02-21), 
Tron players are faced with potentially new optimal mulligan decisions.

### Mulligan for achieving a turn 3 Tron

The mulligan_sim.py file starting hands using the London and [Paris mulligan](https://mtg.fandom.com/wiki/Paris_mulligan) rules.
This program only takes into account starting hands that can guarantee assembling Tron by turn 3.

### Optimal mulligan decisions when Tron is not guaranteed

Determining whether to mulligan hands that do not immediately achieve Tron requires simulated games involving those starting hands.

The vancouver.py script simulates playing until all three Tron lands are in play, and outputs the starting hand and turn when Tron was achieved. Methods for each card and the deck are found in the card_classes.py file.

A Random Forest model trained on 50,000 simulated games are used to predict optimal hand selection for the London Mulligan. The model_turns.py script contains code to train the model. The london.py script chooses the best hand when taking a London mulligan.

### Summary:
In progress.


<br><br>


*Magic: The Gathering* is property of Hasbro
