import pygame
from sys import exit

width = int(1366)
height = int(768)
pygame.init()
screen = pygame.display.set_mode((width, height), pygame.WINDOWMAXIMIZED)
pygame.display.set_caption('ski-game')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)

## static surfaces
## y-coordinate for the top of the ground surface = 325
background_surf = pygame.image.load('assets/images/background.png').convert()
ground_surf = pygame.image.load('assets/images/ground.png').convert()
text_surf = test_font.render('ski-game', False, 'Blue')

## player attributes:
player_surf = pygame.image.load('assets/images/snow_113.png').convert_alpha()
player_x_pos = 100
player_y_pox = 325
player_rect = player_surf.get_rect(midbottom = (player_x_pos, player_y_pox))

## tree attributes:
tree_surf = pygame.image.load('assets/images/snow_108.png').convert_alpha()
tree_x_pos = width
tree_y_pos = height
tree_rect = tree_surf.get_rect(topleft = (tree_x_pos, tree_y_pos))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    ## static elements
    screen.blit(background_surf, (0,0))
    # screen.blit(ground_surf,(0,325))
    screen.blit(text_surf,(400, 50))
   
    ## moving elements
    ## tree element
    tree_rect.x -= 10
    tree_rect.y -= 5
    if tree_rect.right <= -0: 
        tree_rect.left = width
        tree_rect.top = height
    screen.blit(tree_surf, tree_rect)
    
    
    
    ## player element
    screen.blit(player_surf, player_rect)

    ## collision handler
    # if player_rect.colliderect(tree_rect):
    #     print



    pygame.display.update()
    clock.tick(60)