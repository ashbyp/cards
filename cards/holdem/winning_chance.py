from cards.base.card import Deck
from cards.holdem.score import eval_hand
import timeit
import functools


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


if __name__ == '__main__':
    sims = 5
    run_flop_sim(sims)
    run_turn_sim(sims)
    run_river_sim(sims)