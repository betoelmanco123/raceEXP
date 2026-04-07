import random
from race import RaceCar


def get_children_result(A, B):

    child = RaceCar()
    child.w_ih = [row[:] for row in A.w_ih[:6]] + [row[:] for row in B.w_ih[6:]]
    child.w_ho = [row[:] for row in A.w_ho[:1]] + [row[:] for row in B.w_ho[1:]]
    if random.random() < 0.50:
        child.mutate()
    return child


def mix_up(cars, number):

    new_ones = list()

    counter = 0
    while counter < number:

        A = random.choice(cars)
        B = random.choice(cars)
        child = get_children_result(A, B)
        new_ones.append(child)
        counter += 1
    return new_ones
