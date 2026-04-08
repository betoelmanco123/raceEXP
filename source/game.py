import pygame
from source.race import RaceCar
from math import radians, sin, cos
from source.heredation import new_generation
from source.utils import getwinners

WIDTH = 900
HEIGHT = 700
CAR_SPRITE_NAME = "sprites/car.png"
MAP_SPRITE_NAME = "sprites/map3.jpg"
CHECKPOINT_DRAW_RADIUS = 80


class Game:
    def __init__(self, cars=None, Ncars=100):
        pygame.init()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        
        # import images
        self.carsprite = pygame.transform.scale(
        pygame.image.load(CAR_SPRITE_NAME), (72, 28)
        ).convert_alpha()
        
        self.mapsprite = pygame.transform.scale(
        pygame.image.load(MAP_SPRITE_NAME), (900, 900)
        ).convert()
        
        # cars
        if cars is None:
            self.cars = [RaceCar() for _ in range(Ncars)]
        else:
            self.cars = cars
        
        for car in self.cars:
            car.image = self.carsprite
        
        self.checkpoint_positions = [tuple(point) for point in self.cars[0].checkpoints]
        
        self.turn = 0
        self.generation = 0
            
    def draw_checkpoints(self, checkpoints) -> None:
        for checkpoint in checkpoints:
            pygame.draw.circle(
                self.screen,
                (30, 170, 255),
                checkpoint,
                CHECKPOINT_DRAW_RADIUS,
                2,
            )
            pygame.draw.circle(self.screen, (255, 210, 0), checkpoint, 4)
            
            
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
        car.image = pygame.transform.rotate(self.carsprite, -car.direction)
        car.rect = car.image.get_rect(center=(car.x, car.y))
        self.screen.blit(car.image, car.rect)
    
    def run_one_turn(self, cars, turn, generation, time,checkpoint, turn_limit=300):
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
            f"Generation: {generation}   Vivos :{vivos}  Turn: {turn}"
        )

        winners = getwinners(cars, 5)
        for winner in winners:
            self.draw_raycast(winner)
        turn += 1
        if turn >= turn_limit:
            cars, _, checkpoint = new_generation(cars)
            turn = 0
            generation += 1

        return cars, turn, generation, checkpoint
    
    def run_simulation(self):
        checkpoint = 0
        running = True
        clock = pygame.time.Clock()
        last = pygame.time.get_ticks()
        while running:
            value = min(300 + checkpoint * 45 , 600)
            self.screen.blit(self.mapsprite, (0, 0))
            self.draw_checkpoints(self.checkpoint_positions)

            # mouse and keyboard detection
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE:
                        cars, _, checkpoint = new_generation(cars)
                        turn = 0
                        generation += 1

                    if event.key == pygame.K_r:
                        set_mode = False

            current = pygame.time.get_ticks()
            dt = (current - last) / 1000.0
            last = current

            self.cars, self.turn, self.generation, checkpoint = self.run_one_turn(self.cars, self.turn, self.generation, dt,checkpoint, value)


            clock.tick(60)
            pygame.display.update()
    
    
    
juego = Game()

juego.run_simulation()