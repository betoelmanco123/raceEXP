import pygame

HEIGHT = 800
WIDTH = 600
screen = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.init()

running = True

while running:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
    