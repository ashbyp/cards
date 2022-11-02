from itertools import chain, combinations
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
    # results = score_hand(hand)
    # results contains all scores, highest score to lowest
    #   [
    #       [ [[meld1], [meld2]], [deadwood], deadwood_count ],
    #       [ [[meld1]],          [deadwood], deadwood_count ],
    #       [ [[meld2]],          [deadwood], deadwood_count ],
    #   ]
    #
    # It is possible for the melds list to be empty and for all the hand to be deadwood

    if len(hand) not in (10, 11):
        raise ValueError('length of hand must be 10 or 11 cards')

    all_melds = find_all_melds(hand)
    if not all_melds:
        return [[], hand, sum(x.value for x in hand)]

    # brute force, look at every meld combination

    def all_subsets(ss):
        return chain(*map(lambda x: combinations(ss, x), range(0, len(ss) + 1)))

    valid_combinations = []
    for subset in all_subsets(all_melds):
        if subset:
            subset = list(subset)
            valid_combs = [subset[0]]
            for i in range(1, len(subset)):
                comb = subset[i]
                is_subset = False
                for valid in valid_combs:
                    if set(valid).intersection(comb):
                        is_subset = True
                        break
                if not is_subset:
                    valid_combs.append(comb)

            valid_combinations.append(valid_combs)

    results = []

    for comb in valid_combinations:
        results.append([comb, None, 10])

    return results

