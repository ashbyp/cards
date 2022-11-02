from cards.base.card import three_of_a_kind, four_of_a_kind, same_suit_all_runs


def find_all_melds(hand):
    melds = []
    three = three_of_a_kind(hand)
    if three:
        melds.extend(three)
        four = four_of_a_kind(hand)
        if four:
            melds.extend(four)

    for run_len in range(3, len(hand) + 1):
        runs = same_suit_all_runs(hand, run_len)
        if runs:
            melds.extend(runs)
        else:
            break

    return melds


def score_hand(hand):
    if len(hand) not in (10, 11):
        raise ValueError('length of hand must be 10 or 11 cards')

    all_melds = find_all_melds(hand)
    if not all_melds:
        return [], sum(x.value for x in hand)

    return all_melds, 0 # TODO what algo here


