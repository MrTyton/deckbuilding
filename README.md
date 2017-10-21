# deckbuilding

Best-deck list builder for Magic: the Gathering Decklists.

Can pull decklists from mtgtop8 or from folder. If creating own lists, decklists are of the format

```4 CARDNAME
...
2 CARDNAME
SIDEBOARD
3 CARDNAME
```

Works off of essentially a best will-of-the-crowd. Uses cards appearing with each other in different lists to determine synergies between cards, and then determines what cards out of the entire pool are most synergistic with each other, and determines best 60 cards.

Todo is to add capability to do sideboard.

Based roughly off of Frank Karsten's [A New Way to Determine an Aggregate Deck List, but with more math.](https://www.channelfireball.com/articles/magic-math-a-new-way-to-determine-an-aggregate-deck-list-rg-dragons/), as the method used in this program iterates through and determines the cards with the best synergies that are still left in the pool, not just by raw number counts.

To use:
```
python processing.py -h
```

Requires python 2.7+. Requirements are listed in requirements.txt
