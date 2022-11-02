

def score_hand(hand):
    if len(hand) not in (10, 11):
        raise ValueError('length of hand must be 10 or 11 cards')

    # return list of sequences and deadwood count
    return [], sum(x.value for x in hand)

