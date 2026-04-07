import math


def getwinners(cars, number):
    values = dict()
    for car in cars:

        value = 1000 * (car.laps * 4 + car.counterCheckpoint) + car.distanceTraveled / 2
        if not car.alive:
            value -= 100
        if car.speed <= 0.2:
            value -= 500
        if car.speed <= 0.15:
            value -= 100
        value += car.reward * 100 * car.speed

        values[car] = value

    ordenado = sorted(values, key=values.get)

    return ordenado[-number:]


def getDistance(pointA, pointB):
    ax, ay = pointA
    bx, by = pointB
    return math.hypot((ax - bx), (ay - by))
