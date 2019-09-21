from base.card import three_of_a_kind, four_of_a_kind


def find_all_melds(hand):
    melds = []
    three = three_of_a_kind(hand)
    if three:
        melds = three
        four = four_of_a_kind(hand)
        if four:
            melds += four
    return melds


def score_hand(hand):
    if len(hand) not in (10, 11):
        raise ValueError('length of hand must be 10 or 11 cards')

    # return a list of melds with the lowest possible deadwood count
    return [], sum(x.value for x in hand)

