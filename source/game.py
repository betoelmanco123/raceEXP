import pygame
from source.race import RaceCar
from math import radians, sin, cos
from source.heredation import new_generation
from source.utils import getwinners
from source.utils import get_matrix
from source.storage import store_cars

WIDTH = 1280
HEIGHT = 720

CHECKPOINT_DRAW_RADIUS = 80


class Game:
    def __init__(
        self,
        cars=None,
        Ncars=100,
        mapName="sprites/maps/infinite.png",
        carName="sprites/car_blue.png",
    ):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # import images
        self.carsprite = pygame.transform.scale(
            pygame.image.load(carName), (72, 28)
        ).convert_alpha()

        # winners
        self.carsprite_winner = pygame.transform.scale(
            pygame.image.load("sprites/car_green.png"), (72, 28)
        ).convert_alpha()

        self.mapsprite = pygame.transform.scale(
            pygame.image.load(mapName), (1280, 720)
        ).convert()
        self.map_matrix = get_matrix(mapName)

        # normal car
        self.rotations = []
        for angle in range(0, 361):
            self.rotations.append(pygame.transform.rotate(self.carsprite, angle))

        # winner car
        self.rotations_winners = []
        for angle in range(0, 361):
            self.rotations_winners.append(
                pygame.transform.rotate(self.carsprite_winner, angle)
            )

        # cars
        if cars is None:
            self.cars = [RaceCar(validMap=self.map_matrix) for _ in range(Ncars)]
        else:
            self.cars, _, _ = new_generation(cars, Nnew_generation=Ncars, every=True)

        for car in self.cars:
            car.image = self.carsprite

        self.checkpoint_positions = [tuple(point) for point in self.cars[0].checkpoints]
        self.checkpoint_font = pygame.font.SysFont("arial", 24, bold=True)
        self.reached_checkpoint = 0
        self.turn = 0
        self.generation = 0
        self.winners = list()

    def draw_checkpoints(self, checkpoints) -> None:
        for index, checkpoint in enumerate(checkpoints, start=1):
            pygame.draw.circle(
                self.screen,
                (30, 170, 255),
                checkpoint,
                CHECKPOINT_DRAW_RADIUS,
                2,
            )


            number_surface = self.checkpoint_font.render(str(index), True, (0, 0, 0))
            number_rect = number_surface.get_rect(center=checkpoint)
            self.screen.blit(number_surface, number_rect)

    def draw_raycast(self, car: RaceCar) -> None:
        for i in range(len(car.RayValues)):

            theta = radians(car.angles[i] + car.direction + 90)
            pygame.draw.line(
                self.screen,
                (120, 0, 0),
                (car.x, car.y),
                (
                    car.RayValues[i] * sin(theta) + car.x,
                    -car.RayValues[i] * cos(theta) + car.y,
                ),
            )

    def update_car(self, car: list[RaceCar], time) -> None:
        """Update the visual component for a car"""
        car.run(time)

        value = int(car.direction)
        if value >= 0:
            direction = 360 - value
        else:
            direction = -value

        if car in self.winners:
            car.image = self.rotations_winners[direction]
            car.rect = car.image.get_rect(center=(car.x, car.y))
        else:
            car.image = self.rotations[direction]
            car.rect = car.image.get_rect(center=(car.x, car.y))

        self.screen.blit(car.image, car.rect)

    def run_one_turn(
        self,
        cars,
        turn,
        generation,
        time,
        checkpoint,
        turn_limit=300,
        show_raycast=False,
    ):
        vivos = 0
        alive = False
        for car in cars:
            if car.alive:
                alive = True
                self.update_car(car, time)
                vivos += 1

        if not alive:
            cars, _, checkpoint = new_generation(cars)
            generation += 1
            turn = 0

        pygame.display.set_caption(
            f"Generation: {generation}   Vivos :{vivos}  Turn: {turn} / {turn_limit}"
        )

        self.winners = getwinners(cars, 5)
        if show_raycast:
            for winner in self.winners:
                if winner.alive:
                    self.draw_raycast(winner)
        turn += 1
        if turn >= turn_limit:
            cars, _, checkpoint = new_generation(cars)
            turn = 0
            generation += 1

        return cars, turn, generation, checkpoint

    def run_simulation(self):
        show_raycast = True
        show_checkpoints = False
        turn_limit = 300
        value = 300
        checkpoint = 0
        running = True
        clock = pygame.time.Clock()
        last = pygame.time.get_ticks()
        while running:
            turn_limit = min(value + checkpoint * 45, 600 + value)
            self.screen.blit(self.mapsprite, (0, 0))
            if show_checkpoints:
                self.draw_checkpoints(self.checkpoint_positions)

            # mouse and keyboard detection
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE:
                        self.cars, _, checkpoint = new_generation(self.cars)
                        self.turn = 0
                        self.generation += 1

                    if event.key == pygame.K_UP:
                        value += 50
                    if event.key == pygame.K_DOWN:
                        value -= 50
                    if event.key == pygame.K_r:
                        show_raycast = not (show_raycast)
                    if event.key == pygame.K_c:
                        show_checkpoints = not (show_checkpoints)

                    if event.key == pygame.K_s:
                        store_cars(getwinners(self.cars, 5))

            current = pygame.time.get_ticks()
            dt = (current - last) / 1000.0
            last = current

            self.cars, self.turn, self.generation, checkpoint = self.run_one_turn(
                self.cars,
                self.turn,
                self.generation,
                dt,
                checkpoint,
                turn_limit,
                show_raycast=show_raycast,
            )

            clock.tick(60)
            pygame.display.update()


if __name__ == "__main__":
    print("Hello from game.py")
