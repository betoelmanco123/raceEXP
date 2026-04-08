import math


def calculate_fitness(car):
    value = 0.0

    value += car.laps * 1000
    value += car.counterCheckpoint * 150

    value += car.distanceTraveled * 0.2
    
    if car.alive:
        value += 250
    else:
        value -= 250

    ideal_speed = 6
    speed_error = abs(car.speed - ideal_speed)
    value += max(0.0, 300 - speed_error * 120)

    if car.counterCheckpoint == 0 and car.laps == 0:
        value -= 500
    
    value += len(car.known) * 100

    return value


def getwinners(cars, number):
    values = {}

    for car in cars:
        values[car] = calculate_fitness(car)

    ordenado = sorted(values, key=values.get, reverse=True)
    return ordenado[:number]


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
