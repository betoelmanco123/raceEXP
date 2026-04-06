import pygame
from race import RaceCar, getwinners
import math, time


pygame.init()

CARSIZE = [14, 36]

screen = pygame.display.set_mode((900, 900))

carsprite = pygame.transform.scale(pygame.image.load("sprites/car.png"), (72, 28))

mapsprite = pygame.transform.scale(pygame.image.load("sprites/map3.jpg"), (900, 900))

running = True


first = RaceCar()
first.image = carsprite


def updateCar(car):
    car.run()
    car.image = pygame.transform.rotate(carsprite, car.direction)
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


def run_simulation(cars, turn):
    alive = False
    for car in cars:
        if car.alive:
            alive = True
            updateCar(car)


    if not alive:
        cars = reset_generation(cars)
        turn = 0
        
        
    winners = getwinners(cars, 2)
    for winner in winners:
        drawRays(winner)
    turn += 1
    if turn >= 500 and set_mode:
        cars = reset_generation(cars)
        turn = 0

    return cars, turn
cars = [RaceCar() for _ in range(20)]
for car in cars:
    car.image = carsprite

turn = 0
set_mode = True

while running:
    

    screen.blit(mapsprite, (0, 0))  # negro (fondo)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                cars = reset_generation(cars)
                turn = 0
            if event.key == pygame.K_r:
                set_mode = False

    cars, turn = run_simulation(cars, turn)

    pygame.display.update()
