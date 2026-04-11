import random
from source.race import RaceCar
from source.utils import getwinners, calculate_fitness



def get_children_result(A, B):

    child = RaceCar(validMap=A.map)
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
    temp = (number // len(cars)) // 2 
    for i in cars:
        for k in range(temp ):
            child = i.haveChild(speed=.5)
            new.append(child)
        for k in range(temp):
            child = i.haveChild(speed=2)
            new.append(child)
    
    return new

def clone_elite(car):
    elite = RaceCar(validMap=car.map)

    elite.w_ih = [row[:] for row in car.w_ih]
    elite.w_ho = [row[:] for row in car.w_ho]
    elite.goToStart()
    return elite

def new_generation(cars, selected=5, diversity=5, Nnew_generation=None, every=False):
    current = 0
    indicator = False
    if every:
        winners = cars
        print(winners)
    else:
        winners = getwinners(cars, selected)
    elite_cars = []

    for car in winners:
        if car.laps > 0:
            indicator = True
        current = max(current, car.counterCheckpoint + car.laps * 6)
        elite = clone_elite(car)
        elite_cars.append(elite)
    valid_map = car.map
    if Nnew_generation is None:
        children_number = max(0, len(cars) - selected - diversity)
    else:
        children_number = Nnew_generation
    new_cars = get_childrens(winners, children_number)
    for i in range(diversity):
        car = RaceCar(validMap=valid_map)
        new_cars.append(car)

    return new_cars + elite_cars, indicator, current