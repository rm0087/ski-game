import pygame
import random
from sys import exit




width = int(600)
height = int(600)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('ski-game')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/upheavtt.ttf', 50)

# static surfaces
background_surf = pygame.image.load('assets/images/SKISLOPE1.png').convert()
text_surf = test_font.render('', False, 'Blue')

# player attributes:
original_player_surf = pygame.image.load('assets/images/SKI_CHARACTER.png').convert_alpha()
desired_width, desired_height = 100, 100
player_surf = pygame.transform.scale(original_player_surf, (desired_width, desired_height))
player_x_pos = 100
player_y_pos = 400
player_rect = player_surf.get_rect(midbottom = (player_x_pos, player_y_pos))

# jump variables
is_jumping = False
jump_velocity = -20
gravity = 1
player_velocity_y = 0 

# tree attributes:
tree_surf = pygame.image.load('assets/images/snow_108.png').convert_alpha()
tree_x_pos = width
tree_y_pos = height
tree_rect = tree_surf.get_rect(topleft = (tree_x_pos, tree_y_pos))


coin_surf = pygame.image.load('assets/images/COIN.png').convert_alpha()
coin_x_pos = width
coin_y_pos = height
coin_rect = coin_surf.get_rect(topleft = (coin_x_pos, tree_y_pos))

score = 0
score_surf = test_font.render('Score: 0', False, 'Black')
score_rect = player_surf.get_rect(bottomright= (width-10, height-10))


player_speed = 10
# lives = 3
# game_over = False 


# def reset_game():
#     global player_rect, tree_rect, coin_rect, is_jumping, player_velocity_y
#     player_rect.midbottom = (player_x_pos, player_y_pos)
#     is_jumping = False
#     player_velocity_y = 0



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True
                player_velocity_y = jump_velocity


    # move player left and right, ensure player does not move off screen 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
        if player_rect.left < 0:
            player_rect.left = 0
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed 
        if player_rect.right > 400:
            player_rect.right = 400

        
    # static elements
    screen.blit(background_surf, (0,0))
    # screen.blit(ground_surf,(0,325))
    screen.blit(text_surf,(400, 50))

    # tree element
    tree_rect.x -= 10
    tree_rect.y -= 5
    if tree_rect.right <= 0: 
        tree_rect.left = width
        tree_rect.top = height
    screen.blit(tree_surf, tree_rect)
   
    #coin element
    coin_rect.x -= 10
    if coin_rect.right <= 0:
        coin_rect.left = width
        coin_rect.top = height
    screen.blit(coin_surf, coin_rect)

    # player element
    screen.blit(player_surf, player_rect)



    # collision handler for tree lives
    # if player_rect.colliderect(tree_rect):
    #     lives -= 1
    #     if lives > 0:
    #         reset_game()
    #     else:
    #         game_over = True 
    

    score_surf = test_font.render(f'Score: {score}', False, 'Black')
    score_rect = score_surf.get_rect(bottomright = (width - 20, height - 20))
    screen.blit(score_surf, score_rect)

    if is_jumping:
        player_velocity_y += gravity
        player_rect.y += player_velocity_y
        if player_rect.bottom >= player_y_pos:
            player_rect.bottom = player_y_pos
            is_jumping = False
            player_velocity_y = 0
    
    screen.blit(player_surf, player_rect)



    pygame.display.update()
    clock.tick(60)