import sys
from source.game import Game
from source.train import run_simulation
from source.storage import get_stored_cars
from source.utils import get_matrix

arguments = len(sys.argv)
DEFAULT_MAP = "assets/map4.png"

def main():
    if arguments > 1:
        if sys.argv[1] == "-t":
            run_simulation()
        if sys.argv[1] == "-m":
            game = Game(mapName=sys.argv[2])
        if sys.argv[1] == "-c":
            cars = get_stored_cars(get_matrix(sys.argv[2]))
            game = Game(cars=cars)

    game = Game()
    
    game.run_simulation()
    
if __name__ == "__main__":
    main()