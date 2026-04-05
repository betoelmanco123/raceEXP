import pygame
from race import RaceCar, getwinners
import math



        
        
pygame.init()

CARSIZE = [14, 36]

screen  = pygame.display.set_mode((900, 900))

carsprite = pygame.transform.scale(pygame.image.load("sprites/car.png"), (72, 28))

mapsprite = pygame.transform.scale(pygame.image.load("sprites/map3.jpg"), (900, 900))

running = True


first = RaceCar()
first.image = carsprite



def updateCar(car):
    car.run()
    car.image = pygame.transform.rotate(carsprite, car.direction)
    car.rect = car.image.get_rect(center=(car.x, car.y))

def alldied(cars):
    for car in cars:
        if car.alive:
            return False
    return True

def reset_generation(cars):
    winners = getwinners(cars, 10)
    cars = list()
    for car in winners:
        car.goToStart()
        car.print_laps()
        for _ in range(5):
            child = car.haveChild()
            cars.append(child)
        cars.append(car)
    return cars
    

cars = [RaceCar() for _ in range(10)]
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
    alive = True
    for car in cars:
        if car.alive:
            alive = True
            updateCar(car)
            screen.blit(car.image, car.rect)
            
    if not alive:
        cars = reset_generation(cars)
        turn = 0
    turn += 1
    if turn >= 500 and set_mode:
        cars= reset_generation(cars)
        turn = 0

        
        
    pygame.display.update()