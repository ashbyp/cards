from cards.base.card import Deck
from cards.holdem.score import eval_hand, winning_hand
import timeit
import functools


def winning_chance(deck, initial_board, hands, debug=1):
    if debug > 1:
        print(f' Init: {initial_board}')

    tally = dict.fromkeys({tuple(h) for h in hands}, 0)
    combinations = list(deck.combinations_remaining(5 - len(initial_board)))

    if debug > 0:
        print (f'Combinations = {len(combinations)}')

    count = 0
    for count, comb in enumerate(combinations):
        board = initial_board + list(comb)
        if debug > 1:
            print(f'    Board {board}')
        winners, _ = winning_hand(board, hands)
        for winner in winners:
            if debug > 1:
                print(f' winner { winner}')
            tally[tuple(winner)] += 1 / len(winners)

        count += 1
        if debug > 0 and count % 10000 == 0:
            print(count)
            #return [(tally[tuple(h)] / count) * 100 for h in hands]

    if debug > 0:
        print(f'Final tally: {tally}')

    return [(tally[tuple(h)] / count) * 100 for h in hands]


def run_sim(decks, num_cards_known):
    for s, deck in enumerate(decks):
        hands = deck.deal(2, num_cards_known)

        p1_win_or_draw = 0
        p2_win_or_draw = 0

        for revealed in deck.combinations_remaining(5-num_cards_known):
            revealed = list(revealed)
            p1 = eval_hand(hands[0] + revealed)
            p2 = eval_hand(hands[1] + revealed)

            if p1 >= p2:
                p1_win_or_draw += 1
            if p2 >= p1:
                p2_win_or_draw += 1

        p1_success = 100 * (p1_win_or_draw / (p1_win_or_draw + p2_win_or_draw))
        p2_success = 100 * (p2_win_or_draw / (p1_win_or_draw + p2_win_or_draw))

        if abs(100.0 - p1_success - p2_success) > 0.0000000000000000001:
            assert f'EVAL PROBLEM {abs(100.0 - p1_success - p2_success)}'

        print(f'Sim: {s} {hands[0]} {p1_success:.2f}% vs {hands[1]} {p2_success:.2f}%')


def run_sims(name, known, num_sims):
    print(f'{name} SIM')
    all_decks = [Deck(shuffle=True) for _ in range(num_sims)]
    start_time = timeit.default_timer()
    run_sim(all_decks, known)
    time_taken = timeit.default_timer() - start_time
    print(f'Average {name} sim time: {time_taken / num_sims:.4f}')


run_flop_sim = functools.partial(run_sims, 'Flop', 2)
run_turn_sim = functools.partial(run_sims, 'Turn', 3)
run_river_sim = functools.partial(run_sims, 'River', 4)


def test_stuff():
    deck = Deck(shuffle=True)
    hands = deck.deal(2, 2)
    board = deck.deal_one(4)
    print(f'HANDS:   {hands}')
    print(f'BOARD:   {board}')
    print(f'CHANCES: {winning_chance(deck, board, hands)}')

    deck = Deck(shuffle=True)
    hands = deck.deal(2, 2)
    board = deck.deal_one(3)
    print(f'HANDS:   {hands}')
    print(f'BOARD:   {board}')
    print(f'CHANCES: {winning_chance(deck, board, hands)}')

    deck = Deck(shuffle=True)
    hands = deck.deal(2, 2)
    board = []
    print(f'HANDS:   {hands}')
    print(f'BOARD:   {board}')
    print(f'CHANCES: {winning_chance(deck, board, hands)}')


if __name__ == '__main__':
    import cProfile
    cProfile.run('test_stuff()')
