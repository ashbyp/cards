import itertools

from cards.base.card import  Card, standard_deck
from cards.holdem.score import eval_hand

def main(cards):
    deck = standard_deck()
    for c in cards:
        deck.remove(c)
    print(cards)

    total = 0
    win = 0

    for comb in itertools.combinations(deck, 5):
        me = eval_hand(cards)
        you = eval_hand(comb)
        total += 1
        win += me > you

    print('total', total)
    print('win', win)
    print((float(win)/float(total)) * 100)

if __name__ == '__main__':
    main(Card.from_str_list("AD,AH,AS,KH,KS"))
    main(Card.from_str_list("AD,AH,AS,9H,9S"))

