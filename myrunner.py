from math import sin, cos, radians

from utils import getwinners
from race import RaceCar
from heredation import new_generation
from storage import get_stored_cars


import pygame

# constants
CARSIZE = [14, 36]


CAR_SPRITE_NAME = "sprites/car.png"
MAP_SPRITE_NAME = "sprites/map3.jpg"
WIDTH = 900
HEIGHT = 900
CHECKPOINT_BASE_RADIUS = 20
CHECKPOINT_EXTRA_RADIUS = 80
CHECKPOINT_DRAW_RADIUS = CHECKPOINT_BASE_RADIUS + CHECKPOINT_EXTRA_RADIUS

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


def draw_checkpoints(checkpoints) -> None:
    for checkpoint in checkpoints:
        pygame.draw.circle(
            screen,
            (30, 170, 255),
            checkpoint,
            CHECKPOINT_DRAW_RADIUS,
            2,
        )
        pygame.draw.circle(screen, (255, 210, 0), checkpoint, 4)


def run_simulation(cars, turn, generation, time,checkpoint, turn_limit=300):
    vivos = 0
    alive = False
    for car in cars:
        if car.alive:
            alive = True
            update_car(car, time)
            vivos += 1

    if not alive:
        cars, _, checkpoint = new_generation(cars)
        generation += 1
        turn = 0

    pygame.display.set_caption(
        f"Generation: {generation}   Vivos :{vivos}  Turn: {turn}"
    )

    winners = getwinners(cars, 5)
    for winner in winners:
        draw_raycast(winner)
    turn += 1
    if turn >= turn_limit and set_mode:
        cars, _, checkpoint = new_generation(cars)
        turn = 0
        generation += 1

    return cars, turn, generation, checkpoint



cars = get_stored_cars()
for car in cars:
    car.image = carsprite

# Checkpoints are shared by all cars; capture once and draw every frame.
checkpoint_positions = [tuple(point) for point in cars[0].checkpoints]


# variables
running = True
set_mode = True
turn = 0
generation = 0

# time control
clock = pygame.time.Clock()
last = pygame.time.get_ticks()

# main loop
checkpoint = 0
while running:
    value = min(300 + checkpoint * 45 , 600)
    screen.blit(mapsprite, (0, 0))
    draw_checkpoints(checkpoint_positions)

    # mouse and keyboard detection
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                cars, _, checkpoint = new_generation(cars)
                turn = 0
                generation += 1

            if event.key == pygame.K_r:
                set_mode = False

    current = pygame.time.get_ticks()
    dt = (current - last) / 1000.0
    last = current

    cars, turn, generation, checkpoint = run_simulation(cars, turn, generation, dt,checkpoint, value)

    start = pygame.time.get_ticks()

    clock.tick(60)
    pygame.display.update()
