from cards.base.card import Deck
from cards.cribbage.player import DumbComputerPlayer
from cards.cribbage.board import Board, GameWonException
from cards.cribbage import score
from cards.cribbage.display import Display
from cards.cribbage.stats import Collector


class Game:

    def __init__(self, player1, player2, target_score=121, stats=None, display=None, trace_enabled=False):
        self._trace_enabled = trace_enabled
        self._player1 = player1
        self._player2 = player2
        self._target_score = target_score
        self._display = display or Display(True)
        self._stats = stats or Collector(self._player1, self._player2)
        self._display.welcome(self._player1, self._player2)

    def _trace(self, msg):
        if self._trace_enabled:
            print(f'trace: {msg}')

    def decide_dealer(self, deck):
        while True:
            try:
                player1_card = deck.random_card()
                player2_card = deck.random_card()

                self._trace(f'{self._player1.name} cut {player1_card}, {self._player2.name} cut {player2_card}')

                if player1_card.rank < player2_card.rank:
                    return self._player1, self._player2, player1_card, player2_card
                elif player2_card.rank < player1_card.rank:
                    return self._player2, self._player1, player2_card, player1_card
            finally:
                deck.return_cards([player1_card, player2_card])

    def discard(self, dealer, non_dealer, start_dealer_cards, start_non_dealer_cards):
        dealer_discards = dealer.choose_discards(start_dealer_cards, True)
        self._trace(f'{dealer.name} has discarded {dealer_discards}')
        assert len(dealer_discards) == 2, f'discards should be length of 2 {dealer_discards}'

        non_dealer_discards = non_dealer.choose_discards(start_non_dealer_cards, False)
        self._trace(f'{non_dealer.name} has discarded {non_dealer_discards}')
        assert len(non_dealer_discards) == 2, f'discards should be length of 2 {non_dealer_discards}'

        dealer_cards = [x for x in start_dealer_cards if x not in dealer_discards]
        non_dealer_cards = [x for x in start_non_dealer_cards if x not in non_dealer_discards]
        box = dealer_discards + non_dealer_discards

        return dealer_cards, non_dealer_cards, box

    def turn(self, deck, dealer, board):
        turn_card = deck.next_card()
        self._trace(f'Turn card is {turn_card}  ({board})')

        if turn_card.rank == 11:
            board.add_points(dealer, 2)

        self._display.turn_card(turn_card, dealer, board, turn_card.rank == 11)
        return turn_card

    @staticmethod
    def stack_count(stack):
        total = sum([x.value for x in stack])
        if total > 31:
            raise ValueError('A player pegged for more that 31, debug your player')
        return total

    @staticmethod
    def score_pegging_stack(stack):
        return score.score_pegging_stack(stack)

    def play_pegging_card(self, player, stack, hand, turn_card, board):
        peg_card = player.next_pegging_card(stack, hand, turn_card)
        if peg_card:
            hand.remove(peg_card)
            stack.append(peg_card)
            stack_value = self.stack_count(stack)
            player_score, score_desc = self.score_pegging_stack(stack)

            if stack_value in (15, 31):
                board.add_points(player, 2)
            if player_score:
                board.add_points(player, player_score)

            self._display.player_pegged(player, peg_card, stack, stack_value, player_score, score_desc)
            return False
        else:
            self._display.player_said_go(player)
            return True

    def pegging(self, dealer, non_dealer, dealer_hand, non_dealer_hand, turn_card, board):
        stack = []

        dealer_start_points = board.player_score(dealer)
        non_dealer_start_points = board.player_score(non_dealer)
        p1, p2 = non_dealer, dealer
        p1_hand, p2_hand = non_dealer_hand.copy(), dealer_hand.copy()
        p2_go = True

        def reset_stack():
            self._trace(f'Clear stack {stack}, score={self.stack_count(stack)}')
            stack.clear()

        while True:
            p1_go = self.play_pegging_card(p1, stack, p1_hand, turn_card, board)
            if p1_go:
                if p2_go:
                    self._display.no_player_can_go(p1)
                    board.add_points(p1, 1)
                    p1, p2 = p2, p1
                    p1_hand, p2_hand = p2_hand, p1_hand
                    reset_stack()
                    continue

            else:
                if self.stack_count(stack) == 31:
                    self._display.stack_at_31(p1)
                    if not (p1_hand or p2_hand):
                        break
                    p1, p2 = p2, p1
                    p1_hand, p2_hand = p2_hand, p1_hand
                    reset_stack()
                    continue
                elif not (p1_hand or p2_hand):
                    self._display.no_pegging_cards_left(p1)
                    board.add_points(p1, 1)
                    break

            p2_go = self.play_pegging_card(p2, stack, p2_hand, turn_card, board)
            if p2_go:
                if p1_go:
                    self._display.no_player_can_go(p2)
                    board.add_points(p2, 1)
                    reset_stack()
                    continue

            else:
                if self.stack_count(stack) == 31:
                    self._display.stack_at_31(p2)
                    if not (p1_hand or p2_hand):
                        break
                    reset_stack()
                    continue
                elif not (p1_hand or p2_hand):
                    self._display.no_pegging_cards_left(p2)
                    board.add_points(p2, 1)
                    break

        self._display.end_of_pegging(board)
        self._stats.add_pegging_score(dealer, board.player_score(dealer) - dealer_start_points)
        self._stats.add_pegging_score(non_dealer, board.player_score(non_dealer) - non_dealer_start_points)

    def score_hand(self, player, hand, turn_card, board, is_box):
        sc, breakdown = score.score_hand_with_breakdown(hand, turn_card, is_box)
        board.add_points(player, sc)
        self._display.score_hand(player, hand, turn_card, sc, score.breakdown_tostring(breakdown), is_box)
        if is_box:
            self._stats.add_box_score(player, sc)
        else:
            self._stats.add_hand_score(player, sc)

    def play(self,  board=None):
        board = board or Board(self._player1, self._player2, 121)
        deck = Deck()
        deck.shuffle()
        dealer, non_dealer, dealer_card, non_dealer_card = self.decide_dealer(deck)

        self._display.cut(dealer, dealer_card, non_dealer, non_dealer_card )

        while True:
            try:
                dealer_hand, non_dealer_hand = map(sorted, deck.deal(2, 6))

                self._trace(f'{dealer.name} has been dealt {dealer_hand}')
                self._trace(f'{non_dealer.name} has been dealt {non_dealer_hand}')

                dealer_hand, non_dealer_hand, box = self.discard(dealer, non_dealer, dealer_hand, non_dealer_hand)

                self._trace(f'After discard {dealer.name} has  {dealer_hand}')
                self._trace(f'After discard {non_dealer.name} has {non_dealer_hand}')
                self._trace(f'Box is {box}')

                turn_card = self.turn(deck, dealer, board)

                self.pegging(dealer, non_dealer, dealer_hand, non_dealer_hand, turn_card, board)

                self.score_hand(non_dealer, non_dealer_hand, turn_card, board, False)
                self.score_hand(dealer, dealer_hand, turn_card, board, False)
                self.score_hand(dealer, box, turn_card, board, True)

                deck.return_cards(dealer_hand + non_dealer_hand + box + [turn_card])
                self._trace(f' ---- End of round, cards in the deck = {deck.cards_remaining()}')

                dealer, non_dealer = non_dealer, dealer

                self._display.new_dealer(dealer, board)
            except GameWonException as gwe:
                self._trace(gwe)
                self._display.announce_win(board)
                break


if __name__ == '__main__':
    game = Game(DumbComputerPlayer(), DumbComputerPlayer(), 121, trace_enabled=True)
    game.play()
