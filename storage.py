import json, os
from race import RaceCar


def store_cars(cars, dirName):
    for i in range(len(cars)):
        path = dirName + f"car{i}.txt"
        save_car(cars[i], path)


def save_car(car, fileName) -> None:
    genes = car.get_genetics()

    with open(fileName, "w") as file:

        json.dump(genes, file, indent=4)


def get_stored_cars(dirName):
    cars = list()
    for archivo in os.listdir(dirName):
        car = read_car(dirName + "/" + archivo)
        cars.append(car)
    return cars


def read_car(fileName) -> RaceCar:

    car = RaceCar()
    with open(fileName, "r") as file:
        data = json.load(file)
        car.w_ih = data["inputs"]
        car.w_ho = data["outputs"]

    return car
