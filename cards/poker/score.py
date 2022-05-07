import itertools
from urllib.request import urlopen
from cards.base.card import Card


def eval_desc(result, verbose=False):

    value_dict = {11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}

    res_code = {
        8: ('Straight Flush', lambda x: f'{value_dict.get(x[1], str(x[1]))} high'),
        7: ('Four of a Kind', lambda x: f'{value_dict.get(x[1], str(x[1]))}\'s'),
        6: ('Full House', lambda x: f'{value_dict.get(x[1][0], str(x[1][0]))}\'s over {value_dict.get(x[2][0], str(x[2][0]))}\'s'),
        5: ('Flush', lambda x: f'{value_dict.get(x[1][0], str(x[1][0]))} high'),
        4: ('Straight', lambda x: f'{value_dict.get(x[1], str(x[1]))} high'),
        3: ('Three of a Kind', lambda x: f'{value_dict.get(x[1][0], str(x[1][0]))}\'s'),
        2: ('Two pair', lambda x: f'{value_dict.get(x[1][0], str(x[1][0]))}\'s and {value_dict.get(x[1][1], str(x[1][1]))}\'s'),
        1: ('One pair', lambda x: f'{value_dict.get(x[1][0], str(x[1][0]))}\'s'),
        0: ('High card', lambda x: f'{value_dict.get(x[2][0], str(x[2][0]))}'),
    }
    return res_code[result[0]][0] if not verbose else f'{res_code[result[0]][0]} ({res_code[result[0]][1](result)})'


def eval_hand(hand):
    # Return ranking followed by tie-break information.
    # 8. Straight Flush
    # 7. Four of a Kind
    # 6. Full House
    # 5. Flush
    # 4. Straight
    # 3. Three of a Kind
    # 2. Two pair
    # 1. One pair
    # 0. High card
    #
    # Aces are transformed to 14 in the tie break info to allow hands to be ranked correctly
    if len(hand) != 5:
        raise ValueError("Can only evaluate 5 card hands")

    values = sorted([c.rank if c.rank != 1 else 14 for c in hand], reverse=True)
    suits = [c.suit for c in hand]
    straight = (values == list(range(values[0], values[0]-5, -1))
                or values == [14, 5, 4, 3, 2])
    flush = all(s == suits[0] for s in suits)

    if straight and flush:
        return 8, values[0] if values[0:2] != [14, 5] else 5
    if flush:
        return 5, values
    if straight:
        return 4, values[0] if values[0:2] != [14, 5] else values[1]

    trips = []
    pairs = []
    for v, group in itertools.groupby(values):
        count = sum(1 for _ in group)
        if count == 4: return 7, v, values
        elif count == 3: trips.append(v)
        elif count == 2: pairs.append(v)

    if trips:
        return (6 if pairs else 3), trips, pairs, values
    return len(pairs), pairs, values


def score_some_hands():
    data = urlopen('https://projecteuler.net/project/resources/p054_poker.txt')
    count = 0
    for line in data:
        try:
            cards = Card.from_str_list(line.decode('utf-8').strip(), sep=' ')
            hand1 = cards[0:5]
            hand2 = cards[5:]
            eval1 = eval_hand(hand1)
            eval2 = eval_hand(hand2)
            desc1 = eval_desc(eval1, True)
            desc2 = eval_desc(eval2, True)
            result = "draws with"

            if eval1 > eval2:
                result = 'beats'
                count += 1
            elif eval1 < eval2:
                result = 'loses to'

            print(f'{hand1} {desc1} {result} {hand2} {desc2}')
        except ValueError as e:
            print(e, f'input was {line}')
            raise e

    print(f'Player 1 won {count} games')


if __name__ == '__main__':
    score_some_hands()

