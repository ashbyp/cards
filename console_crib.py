from cards.cribbage import player
from cards.cribbage.game import Game

game = Game(player.HumanPlayer(), player.ComputerPlayerV4())
game.play()

