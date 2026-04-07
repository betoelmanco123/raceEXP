import pygame
from race import RaceCar, getwinners, mix_up
import math, time


pygame.init()

CARSIZE = [14, 36]

screen = pygame.display.set_mode((900, 900))

carsprite = pygame.transform.scale(pygame.image.load("sprites/car.png"), (72, 28))

mapsprite = pygame.transform.scale(pygame.image.load("sprites/map3.jpg"), (900, 900))

running = True


first = RaceCar()
first.image = carsprite


def updateCar(car, time):
    car.run(time)
    car.image = pygame.transform.rotate(carsprite, -car.direction)
    car.rect = car.image.get_rect(center=(car.x, car.y))
    screen.blit(car.image, car.rect)


def alldied(cars):
    for car in cars:
        if car.alive:
            return False
    return True


def reset_generation(cars):
    winners = getwinners(cars, 5)
    cars = list()
    for car in winners:

        car.goToStart()
        car.print_laps()
        for _ in range(10):
            child = car.haveChild()
            cars.append(child)
        cars.append(car)
    return cars


def new_generation(cars):
    winners = getwinners(cars, 3)

    for car in winners:
        car.goToStart()

    new_cars = mix_up(winners, 50)

    return new_cars + winners


def drawRays(car):
    for i in range(len(car.RayValues)):
        if not car.alive:
            return
        theta = math.radians(car.angles[i] + car.direction + 90)
        pygame.draw.line(
            screen,
            (120, 0, 0),
            (car.x, car.y),
            (
                car.RayValues[i] * math.sin(theta) + car.x,
                -car.RayValues[i] * math.cos(theta) + car.y,
            ),
        )


def run_simulation(cars, turn, generation, time):
    vivos = 0
    alive = False
    for car in cars:
        if car.alive:
            alive = True
            updateCar(car, time)
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
        drawRays(winner)
    turn += 1
    if turn >= 300 and set_mode:
        cars = new_generation(cars)
        turn = 0
        generation += 1

    return cars, turn, generation


cars = [RaceCar() for _ in range(20)]
for car in cars:
    car.image = carsprite

turn = 0
set_mode = True
generation = 0
clock = pygame.time.Clock()
last = pygame.time.get_ticks()
while running:
    screen.blit(mapsprite, (0, 0))  # negro (fondo)

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
