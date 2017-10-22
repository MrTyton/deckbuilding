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

What this program does:

1. Reads in all of the decklists provided
    1. For each combination of cards in the list, add that combination to a global pool of cards
        * For example, for a decklist of 1 Serum Visions, 1 Gitaxian Probe, and 1 Island, the combinations (for n = 2) added to the pool would be: (1 Serum Visions, 1 Gitaxian Probe), (1 Serum Visions, 1 Island), (1 Gitaxian Probe, 1 Island), (1 Serum Vision), (1 Gitaxian Probe), (1 Island)
    2. Cards that exist in multiples are each treated as their own card, with a positional order.
        * For example, 4 Serum Visions is treated like 4 separate cards: Serum Visions 1, Serum Visions 2, Serum Visions 3, and Serum Visions 4
    3. Each time that a combination repeats in a different decklist, the count for that combination is incremented by 1.
2. Start a loop until the number of cards left in the pool is the size of the deck (60 cards)
    1. Go through each combination in the pool
    2. For each card in the combination, increase the rank of that card by ``(number of times that the card appeared) * (1/2^(size of the combination))``
    3. Remove the card with the lowest rank
    4. Reset the rank of the card.
3. Repeat for sideboard

This ensures that the cards that are left are the ones that have the highest amount of synergy with the other cards in the pool, since the cards are upranked when they are found with other cards. The more often that the cards are found with the other cards in the combinatiosn, the higher the rank of the card. As this is recalculated each iteration of the loop, it ensures that it's only looking at cards that are still in the rest of the card pool.


To use:
```
python processing.py -h
```

Requires python 2.7+. Requirements are listed in requirements.txt
