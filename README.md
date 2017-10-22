# deckbuilding

Best-deck list builder for Magic: the Gathering Decklists.

Can pull decklists from mtgtop8 or from folder. If creating own lists, decklists are of the format

```
4 CARDNAME
...
2 CARDNAME
SIDEBOARD
3 CARDNAME
```

which is the MTGO export format.

Works off of essentially a best will-of-the-crowd. Uses cards appearing with each other in different lists to determine synergies between cards, and then determines what cards out of the entire pool are most synergistic with each other, and determines best 60 cards. Also works for sideboards with the same way, but doesn't do legality checks between sideboard and maindeck nor does it check for synergy between sideboard and maindeck (yet).

Based roughly off of Frank Karsten's [A New Way to Determine an Aggregate Deck List](https://www.channelfireball.com/articles/magic-math-a-new-way-to-determine-an-aggregate-deck-list-rg-dragons/), but with more math, as the method used in this program iterates through and determines the cards with the best synergies that are still left in the pool, not just by raw number counts.

To use:
```
python processing.py -h
```

Requires python 2.7+. Requirements are listed in requirements.txt
