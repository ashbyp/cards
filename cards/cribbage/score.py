import itertools

from cards.base import card


def runs(hand, turn_card):
    return card.any_suit_runs(hand + [turn_card] if turn_card else hand, 3)


def flushes(hand, turn_card, is_box):
    if is_box:
        if turn_card:
            return card.flushes(hand + [turn_card], 5)
    else:
        if turn_card:
            if card.flushes(hand, 4):
                return card.flushes(hand + [turn_card], 4)
        else:
            return card.flushes(hand, 4)
    return []


def fifteens(hand, turn_card):
    hand = hand + [turn_card] if turn_card else hand
    results = []

    for i in range(2, len(hand) + 1):
        for comb in itertools.combinations(hand, i):
            if sum(c.value for c in comb) == 15:
                results.append(list(comb))
    return results


def pairs(hand, turn_card):
    return card.pairs(hand + [turn_card] if turn_card else hand)


def nob(hand, turn_card):
    if not turn_card:
        return []

    for c in hand:
        if c.rank == 11 and c.suit == turn_card.suit:
            return [True]
    return []


def break_down(hand, turn_card, is_box):
    return {
        'runs': runs(hand, turn_card),
        'flushes': flushes(hand, turn_card, is_box),
        'fifteens': fifteens(hand, turn_card),
        'pairs': pairs(hand, turn_card),
        'nob': nob(hand, turn_card)
    }


def breakdown_tostring(bd):
    s = ''
    for score_type, scores in bd.items():
        if scores:
            if s:
                s += '\n'
            s += '%-9s: %s' % (score_type.capitalize(),
                               ', '.join(map(str, map(lambda x: sorted(x)
                               if isinstance(x, list) else x, (bd[score_type])))))
    return s


def score_breakdown(bd):
    score = sum(len(r) for r in bd['runs'])
    score += sum(len(f) for f in bd['flushes'])
    score += len(bd['fifteens']) * 2
    score += len(bd['pairs']) * 2
    if bd['nob']:
        score += 1
    return score


def score_hand(hand, turn_card, is_box=False):
    return score_breakdown(break_down(hand, turn_card, is_box))


def score_hand_with_breakdown(hand, turn_card, is_box=False):
    bd = break_down(hand, turn_card, is_box)
    return score_breakdown(bd), bd


def score_pegging_stack(stack):
    stack_len = len(stack)
    if stack_len >= 2:
        stack = list(reversed(stack))
        of_a_kind = 1
        for i in range(1, stack_len):
            if stack[i].rank == stack[0].rank:
                of_a_kind += 1
            else:
                break
        if of_a_kind > 1:
            return {2: 2, 3: 6, 4: 12}[of_a_kind], f'{of_a_kind} of a kind'

        for run_length in range(stack_len, 2, -1):
            if card.is_run(stack[0:run_length]):
                return run_length, f'run of {run_length}'

    return 0, None
