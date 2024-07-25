import pygame

pygame.init()
if pygame.get_init():
    print("pygame initialized successfully!")
else:
    raise Exception("pygame could not be initialized")

keys = pygame.key.get_pressed()

background = [1, 1, 2, 2, 2, 1]
screen = pygame.display.set_mode((640, 480))
for i in range(6):
    screen.blit(background[i], (i*10,0))
playerpos = 3
screen.blit(8, (playerpos*10,0))