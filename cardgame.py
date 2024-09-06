#Coulton Manning
import random
suit = [ "D", "H", "C", "S" ]
value = [x for x in range(1,14)]

fullDeck = []
for s in suit:
    for card in [[x,s] for x in value]:
        fullDeck += [card]

def cardGen(fullDeck):
    card = random.choice(fullDeck)
    fullDeck.remove(card)
    return [card]

def printCards(deck):
    for card in deck:
        print(card[0], " of ", card[1])

def shuffleDeck(fullDeck):
    deck = []
    i=0
    while i < 52:
        card = cardGen(fullDeck)
        if card not in deck:
            i+=1
            deck+=[card]
    return deck