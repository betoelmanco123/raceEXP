import math
import numpy as np
from PIL import Image

def calculate_fitness(car):
    value = 0.0

    value += car.laps * 5000
    value += car.counterCheckpoint * 1500

    value += car.distanceTraveled * 0.2
    
    if car.alive:
        value += 250
    else:
        value -= 250

    ideal_speed = 6
    speed_error = abs(car.speed - ideal_speed)
    value += max(0.0, 300 - speed_error * 500)
    

    if car.counterCheckpoint == 0 and car.laps == 0:
        value -= 500
    
    value += len(car.known) * 100

    car.reward += value
    car.reward += car.TotalSpeed * 5
    #if car.counterCheckpoint > current_checkpoint:
        #car.winner = True
    
    return car.reward


def getwinners(cars, number=5):

    values = {}
    winner = list()
    for car in cars:
        #if car.winner:
         #   winner.append(car)
        values[car] = calculate_fitness(car)

    ordenado = sorted(values, key=values.get, reverse=True)
    selected = ordenado[:number]
    
    #for i in winner:
     #   if i not in selected:
      #      selected.append(i)
    return selected


def getDistance(pointA, pointB):
    ax, ay = pointA
    bx, by = pointB
    return math.hypot((ax - bx), (ay - by))

def is_all_died(cars: list) -> bool:
    """Return `True` if every car in a list is not alive"""
    
    for car in cars:
        if car.alive:
            return False
    return True

def get_matrix(mapName):
    img = Image.open(mapName).convert("L")
    matriz = np.array(img)
    return matriz


def getColition(map1, position):
    x, y = position
    
    if map1[x][y] == 0:
        return True
    return False