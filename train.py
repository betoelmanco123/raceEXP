from race import RaceCar
from utils import getwinners
from heredation import new_generation
import time
from storage import store_cars

START_CARS = 100
WINNERS = 5


def run_one_turn(cars, turn, generation, dt, turnlimit=500, current=0):
    indicator = False
    alive = False
    checkpoint = current
    for car in cars:
        if car.alive:
            alive = True
            car.run(dt)

    # Si todos murieron, crear nueva generación y terminar el turno aquí.
    if not alive:
        cars, indicator, checkpoint = new_generation(cars, selected=WINNERS)
        generation += 1
        return cars, 0, generation, indicator, checkpoint

    turn += 1
    if turn >= turnlimit:
        cars, indicator, checkpoint = new_generation(cars, selected=WINNERS)
        generation += 1
        print(f"generation {generation}")
        return cars, 0, generation, indicator, checkpoint

    return cars, turn, generation, indicator, checkpoint


def run_simulation():
    checkpoint = 0
    indicator = False
    saw_winner = False
    cars = [RaceCar() for _ in range(START_CARS)]
    turn = 0
    generation = 0
    counter = 0
    last = time.perf_counter()
    while True:
        current = time.perf_counter()
        dt = current - last
        last = current
        value = min(300 + checkpoint * 45, 600)
        prev_checkpoint = checkpoint
        cars, turn, generation, indicator, checkpoint = run_one_turn(
            cars, turn, generation, dt, turnlimit=value, current=checkpoint
        )
        if checkpoint > prev_checkpoint:
            print(checkpoint)
        if indicator:
            counter += 1
            saw_winner = True


        if counter >= 10 or generation >= 100:
            break

    beaters = getwinners(cars, 5)
    store_cars(beaters)
    return saw_winner


def main():
    start = time.time()
    print("Starting simulation")
    indicator = run_simulation()
    end = time.time()
    print(f"Simulation ended after {end - start} seconds")
    if indicator:
        print("Someone won the race")
    else:
        print("Nobody won the race")


if __name__ == "__main__":
    main()
