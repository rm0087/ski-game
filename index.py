import pygame
from sys import exit
import cv2 

cap = cv2.VideoCapture('background/SKI_BACKGROUND.mov')

pygame.init()
keys = pygame.key.get_pressed()
background = [1, 1, 2, 2, 2, 1]
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Upheaval.ttf', 30)


for i in range(6):
    screen.blit(background[i], (i*10,0))
playerpos = 3
screen.blit(8, (playerpos*10,0))

 

text_surface = test_font.render('X Ski Games', False, 'Blue')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            exit()


    ret, frame = cap.read()
    if not ret:
        break

    pygame.display.update()
    clock.tick(60)