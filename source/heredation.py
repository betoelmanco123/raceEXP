import random
from source.race import RaceCar
from source.utils import getwinners, calculate_fitness



def get_children_result(A, B):

    child = RaceCar()
    child.w_ih = [row[:] for row in A.w_ih[:6]] + [row[:] for row in B.w_ih[6:]]
    child.w_ho = [row[:] for row in A.w_ho[:1]] + [row[:] for row in B.w_ho[1:]]
    if random.random() < 0.50:
        child.mutate()
    return child

# cross generation
def mix_up(cars, number):

    new_ones = list()

    counter = 0
    while counter < number:

        A = random.choice(cars)
        B = random.choice(cars)
        child = get_children_result(A, B)
        new_ones.append(child)
        counter += 1
        if random.random() < .6:
            child.mutate()
    return new_ones


# simple mutation
def get_childrens(cars, number):
    new = list()
    temp = number // len(cars)
    for i in cars:
        for k in range(temp):
            child = i.haveChild()
            new.append(child)
    
    return new

def clone_elite(car):
    elite = RaceCar()
    elite.w_ih = [row[:] for row in car.w_ih]
    elite.w_ho = [row[:] for row in car.w_ho]
    elite.goToStart()
    return elite

def new_generation(cars, selected=3, diversity=10):
    current = 0
    indicator = False
    winners = getwinners(cars, selected)
    elite_cars = []

    for car in winners:
        if car.laps > 0:
            indicator = True
        current = max(current, car.counterCheckpoint + car.laps * 6)
        elite = clone_elite(car)
        elite_cars.append(elite)

    children_number = max(0, len(cars) - selected - diversity)
    new_cars = get_childrens(winners, children_number)
    for i in range(diversity):
        car = RaceCar()
        new_cars.append(car)

    return new_cars + elite_cars, indicator, current