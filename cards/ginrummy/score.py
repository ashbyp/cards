from cards.base.card import three_of_a_kind, four_of_a_kind, same_suit_all_runs
from cards.base.utils import all_subsets, remove_intersecting_sets


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
    # results contains all scores, lowest score to highest
    #   [
    #       [ [[meld1], [meld2]], [deadwood], deadwood_count ],
    #       [ [[meld1]],          [deadwood], deadwood_count ],
    #       [ [[meld2]],          [deadwood], deadwood_count ],
    #   ]
    #
    # It is possible for the melds list to be empty and for all the hand to be deadwood

    if len(hand) not in (10, 11):
        raise ValueError('length of hand must be 10 or 11 cards')

    all_melds = [set(m) for m in find_all_melds(hand)]
    if not all_melds:
        return [[], hand, sum(x.value for x in hand)]

    # brute force, look at every meld combination
    potential_scores = list(all_subsets(all_melds))
    scores = []
    for p in potential_scores:
        score = remove_intersecting_sets(p)
        if score and score not in scores:
            scores.append(score)

    results = []
    for score in scores:
        flat_score = [card for meld in score for card in meld]
        deadwood = [card for card in hand if card not in flat_score]
        results.append([score, deadwood, sum(x.value for x in deadwood)])

    return sorted(results, key=lambda x: x[2])
