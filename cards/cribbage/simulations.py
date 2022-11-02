import timeit
import datetime
import numpy as np
import concurrent.futures
import multiprocessing

from cards.base import card
from cards.cribbage import score
from cards.cribbage.stats import Collector
from cards.cribbage.game import Game
from cards.cribbage.display import Display
from cards.cribbage.player import RandomComputerPlayer, ComputerPlayerV1, ComputerPlayerV2, ComputerPlayerV3, \
    ComputerPlayerV4, ComputerPlayerV5


class Simulator:
    def run(self, *args, **kwargs):
        raise NotImplementedError()

    @staticmethod
    def record_results(simulation_type, num_simulations, stats):
        with open(f'{simulation_type}.txt', 'a') as f:
            f.write(f'{datetime.datetime.now()} :: Simulations: {num_simulations} :: {stats}\n')


class TargetScoreSimulation(Simulator):

    @staticmethod
    def attempts_for_score_v1(deck, target_score, verbose=False):
        if verbose:
            print(f'Looking for score of {target_score}')
        attempts = 1
        while True:
            deck.shuffle()
            h = deck.deal_one(4)
            t = deck.next_card()
            hs = score.score_hand(h, t)
            deck.return_cards(h)
            deck.return_card(t)
            if hs == target_score:
                if verbose:
                    print(f'Found score of {target_score} after {attempts} attempts')
                break
            attempts += 1
        return attempts

    @staticmethod
    def attempts_for_score(deck, target_score, verbose=False):
        if verbose:
            print(f'Looking for score of {target_score}')
        attempts = 1
        while True:
            deck.shuffle()
            h = deck.deal_one(6)
            sh = score.choose_best_hand(h, 4)
            t = deck.next_card()
            hs = score.score_hand(sh[0][1], t)
            deck.return_cards(h)
            deck.return_card(t)
            if hs == target_score:
                if verbose:
                    print(f'Found score of {target_score} after {attempts} attempts')
                break
            attempts += 1
        return attempts

    def _single_thread(self, target_score, num_attempts):
        deck = card.Deck()
        return [self.attempts_for_score(deck, target_score) for _ in range(num_attempts)]

    def _multi_threaded(self, target_score, num_attempts):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            return list(executor.map(self.attempts_for_score, [card.Deck() for _ in range(num_attempts)], [target_score] * num_attempts))

    def _multi_process(self, target_score, num_attempts):
        with multiprocessing.Pool() as pool:
            return pool.starmap(self.attempts_for_score, [(card.Deck(), target_score)] * num_attempts)

    def run(self, target_score, num_attempts):
        if target_score > 19 or num_attempts > 50:
            fn = self._multi_process
        elif num_attempts > 10:
            fn = self._multi_threaded
        else:
            fn = self._single_thread

        print(f'Run sim: {fn}')

        start_time = timeit.default_timer()
        results = fn(target_score, num_attempts)
        time_taken = timeit.default_timer() - start_time
        print(f'Score {target_score}, Num attempts {num_attempts}, avg = {np.mean(results)}, Time={time_taken}')


class PlayerPerformanceSimulator(Simulator):

    def __init__(self, player1, player2=RandomComputerPlayer(), keep_alive=False):
        self._player1 = player1
        self._player2 = player2
        self._keep_alive = keep_alive

    def run(self, num_games):
        display = Display(False)
        collector = Collector(self._player1, self._player2)
        game = Game(self._player1, self._player2, stats=collector, display=display)

        for i in range(num_games):
            if self._keep_alive and not (i % 50):
                print('.', end='', flush=True)
            game.play()

        self.record_results(self.__class__.__name__, num_games, collector)
        return collector


class PlayerComparisonSimulator(Simulator):

    def __init__(self, keep_alive=False):
        self._keep_alive = keep_alive

    @staticmethod
    def _run_sim(simulator, games_per_sim):
        return simulator.run(games_per_sim)

    def _run_for_player(self, player, num_sims, games_per_sim):
        opp = RandomComputerPlayer()
        start_time = timeit.default_timer()
        with multiprocessing.Pool() as pool:
            results = pool.starmap(self._run_sim, [(PlayerPerformanceSimulator(player, opp, self._keep_alive),
                                                    games_per_sim)] * num_sims)
        time_taken = timeit.default_timer() - start_time
        results = Collector.combine(results, player, opp)
        print(f'Simulations: {num_sims*games_per_sim} :: {results} :: Time {time_taken}')
        self.record_results(self.__class__.__name__, num_sims*games_per_sim, results)

    def run(self, num_sims=5, games_per_sim=5):
        players = [ComputerPlayerV1(), ComputerPlayerV2(),  ComputerPlayerV3(), ComputerPlayerV4(), ComputerPlayerV5()]
        for player in players:
            self._run_for_player(player, num_sims, games_per_sim)


if __name__ == '__main__':
    sim = PlayerComparisonSimulator()
    sim.run()

























