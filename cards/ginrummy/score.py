from cards.base.card import three_of_a_kind, four_of_a_kind, same_suit_all_runs


def find_all_melds(hand):
    melds = []
    three = three_of_a_kind(hand)
    if three:
        melds += three
        four = four_of_a_kind(hand)
        if four:
            melds += four

    for run_len in range(3, len(hand) + 1):
        runs = same_suit_all_runs(hand, run_len)
        if runs:
            melds += runs
        else:
            break

    return melds


def score_hand(hand):
    if len(hand) not in (10, 11):
        raise ValueError('length of hand must be 10 or 11 cards')

    # return a list of melds with the lowest possible deadwood count
    return [], sum(x.value for x in hand)

