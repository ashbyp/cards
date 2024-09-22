import itertools

from cards.base.card import  Card, standard_deck
from cards.holdem.score import eval_hand, eval_desc


def main(cards):
    deck = standard_deck()
    for c in cards:
        deck.remove(c)
    print(cards)

    total = 0
    win = 0
    lose = 0
    draw = 0

    for comb in itertools.combinations(deck, 5):
        me = eval_hand(cards)
        you = eval_hand(comb)
        if me > you:
            win += 1
            total += 1
        elif you > me:
            total += 1
            lose += 1
            print(eval_desc(you, True), comb)
        else:
            draw += 1

    print('total', total)
    print('win', win)
    print('lose', lose)
    print('draw', draw)
    print((float(win)/float(total)) * 100)

if __name__ == '__main__':
    main(Card.from_str_list("9D,KD,QD,JD,10D"))
    # main(Card.from_str_list("AD,AH,AS,KH,KS"))
    # main(Card.from_str_list("AD,AH,AS,9H,9S"))

