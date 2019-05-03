# MTG Divination - Tron

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

Divination simulates starting hands using the London and [Paris mulligan](https://mtg.fandom.com/wiki/Paris_mulligan) rules.
This aspect of the program only takes into account starting hands that can guarantee assembling Tron by turn 3.

### Optimal mulligan decisions when Tron is not guaranteed

Determining whether to mulligan hands that do not immediately achieve Tron requires simulated games involving those starting hands.

Divination simulates gameplay until all three Tron lands are in play, and outputs the starting hand and turn when Tron was achieved. A Random Forest model trained on 50,000 simulated games is used to predict optimal hand selection for the London Mulligan. 

### Summary:

Under the Vancouver mulligan rule, taking mulligans until 3 card hands results in a guaranteed turn 3 Tron 36% of the time. In comparison, hands using the London mulligan rule guarantee turn 3 Tron 63% of the time, a. 

These results are consistent with deck selections for the inaugural event for the London mulligan. Players were aware that the Tron deck performs more consistently under these rules, as evidenced by the deck having the [largest share of the metagame](https://magic.wizards.com/en/events/coverage/2019MC2/mythic-championship-ii-day-1-metagame-breakdown-2019-04-26).

<br><br>


*Magic: The Gathering* is property of Hasbro
