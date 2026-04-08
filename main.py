import sys
from game import Game
from train import run_simulation

arguments = len(sys.argv)


def main():
    if arguments > 1:
        if sys.argv[1] == "-t":
            run_simulation()
    game = Game()
    
    game.run_simulation()