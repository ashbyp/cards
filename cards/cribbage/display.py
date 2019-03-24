class Display:

    def __init__(self, enabled):
        self._enabled = enabled

    def welcome(self, player1, player2):
        if self._enabled:
            print()
            print('*' * 70)
            print(f'  Welcome to Cribbage v0.1')
            print(f'      {player1.name}')
            print(f'      {player2.name}')
            print('*' * 70)
            print()

    def announce_win(self, board):
        if self._enabled:
            print()
            print('*' * 70)
            print(f'  Winner')
            print(f'      {board}')
            print('*' * 70)
            print()

    def cut(self, dealer, dealer_card, non_dealer, non_dealer_card):
        if self._enabled:
            print(f'{dealer.name} cut {dealer_card} and will deal, {non_dealer.name} cut {non_dealer_card}')

    def new_dealer(self, dealer, board):
        if self._enabled:
            print(f'New dealer: {dealer.name},\n Current score {board}')

    def turn_card(self, card, dealer, board, nibs):
        if self._enabled:
            if nibs:
                print(f'Turn card was {card} nibs to {dealer.name} ({board})')
            else:
                print(f'Turn card was {card}')

    def player_pegged(self, player, card, stack, stack_value, player_score, score_desc):
        if self._enabled:
            msg = f'{player.name} pegged {card}\n\n'
            if stack_value in (15, 31):
                msg += f'Stack Value: {stack_value}, 2 points for {player.name}\n'
            else:
                msg += f'Stack Value: {stack_value}\n'
            if player_score:
                msg += f'Score :      {stack_value} for {score_desc}\n'
            msg += f'Stack:       {stack}\n'
            print(msg)

    def player_said_go(self, player):
        if self._enabled:
            print(f'Player {player.name} said GO\n')

    def no_player_can_go(self, last_player):
        if self._enabled:
            print(f'Last player was {last_player.name}, 1 point (both could not go)')

    def stack_at_31(self, last_player):
        if self._enabled:
            print(f'Last player was {last_player.name}, (stack at 31)')

    def no_pegging_cards_left(self, last_player):
        if self._enabled:
            print(f'Last player was {last_player.name}, 1 point (no cards left)')

    def end_of_pegging(self, board):
        if self._enabled:
            print(f'\nEnd of pegging score: {board}\n')

    def score_hand(self, player, hand, turn_card, score, score_desc, is_box):
        if self._enabled:
            msg = f'{"Hand" if not is_box else "Box"} score for {player.name}\n'
            msg += f' Cards : {hand}\n'
            msg += f' Turn  : {turn_card}\n\n\n'
            msg += f'{score_desc}\n'
            msg += f'Score    : {score}\n'
            print(msg)
