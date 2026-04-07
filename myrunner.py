from math import sin, cos, radians

from utils import getwinners
from race import RaceCar
from heredation import mix_up


import pygame

# constants
CARSIZE = [14, 36]


CAR_SPRITE_NAME = "sprites/car.png"
MAP_SPRITE_NAME = "sprites/map3.jpg"
WIDTH = 900
HEIGHT = 900

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# images
carsprite = pygame.transform.scale(
    pygame.image.load(CAR_SPRITE_NAME), (72, 28)
).convert_alpha()
mapsprite = pygame.transform.scale(
    pygame.image.load(MAP_SPRITE_NAME), (900, 900)
).convert()


def update_car(car: list[RaceCar], time) -> None:
    """Update the visual component for a car"""
    car.run(time)
    car.image = pygame.transform.rotate(carsprite, -car.direction)
    car.rect = car.image.get_rect(center=(car.x, car.y))
    screen.blit(car.image, car.rect)


def is_all_died(cars: list[RaceCar]) -> bool:
    """Return `True` if every car in a list is not alive"""

    for car in cars:
        if car.alive:
            return False
    return True


# raycast
def draw_raycast(car: RaceCar) -> None:
    for i in range(len(car.RayValues)):
        if not car.alive:
            return
        theta = radians(car.angles[i] + car.direction + 90)
        pygame.draw.line(
            screen,
            (120, 0, 0),
            (car.x, car.y),
            (
                car.RayValues[i] * sin(theta) + car.x,
                -car.RayValues[i] * cos(theta) + car.y,
            ),
        )


def run_simulation(cars, turn, generation, time):
    vivos = 0
    alive = False
    for car in cars:
        if car.alive:
            alive = True
            update_car(car, time)
            vivos += 1

    if not alive:
        cars = new_generation(cars)
        generation += 1
        turn = 0

    pygame.display.set_caption(
        f"Generation: {generation}   Vivos :{vivos}  Turn: {turn}"
    )

    winners = getwinners(cars, 2)
    for winner in winners:
        draw_raycast(winner)
    turn += 1
    if turn >= 300 and set_mode:
        cars = new_generation(cars)
        turn = 0
        generation += 1

    return cars, turn, generation


# generation
def new_generation(cars):
    winners = getwinners(cars, 3)

    for car in winners:
        car.goToStart()

    new_cars = mix_up(winners, 50)

    return new_cars + winners


cars = [RaceCar() for _ in range(20)]
for car in cars:
    car.image = carsprite


# variables
running = True
set_mode = True
turn = 0
generation = 0

# time control
clock = pygame.time.Clock()
last = pygame.time.get_ticks()

# main loop
while running:

    screen.blit(mapsprite, (0, 0))

    # mouse and keyboard detection
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                cars = new_generation(cars)
                turn = 0
                generation += 1

            if event.key == pygame.K_r:
                set_mode = False

    current = pygame.time.get_ticks()
    dt = (current - last) / 1000.0
    last = current

    cars, turn, generation = run_simulation(cars, turn, generation, dt)

    start = pygame.time.get_ticks()

    clock.tick(60)
    pygame.display.update()
