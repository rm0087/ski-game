import pygame
import random
from sys import exit

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen setup
width = int(600)
height = int(600)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Alpine Adventures')
clock = pygame.time.Clock()

# Fonts
main_font = pygame.font.Font('Font/upheavtt.ttf', 50)
ui_font = pygame.font.Font('Font/upheavtt.ttf', 30)

# Load images
background_surf = pygame.image.load('assets/images/SKISLOPE1.png').convert()
start_background = pygame.image.load('assets/images/SKISTART.png').convert()
start_background = pygame.transform.scale(start_background, (width, height))
score_background = pygame.image.load('assets/images/score_background.png').convert()
score_background = pygame.transform.scale(score_background, (width, height))
win_background = pygame.image.load('assets/images/You_Win.png').convert()
win_background = pygame.transform.scale(win_background, (width, height))
game_over_background = pygame.image.load('assets/images/game_over_background.png').convert()
game_over_background = pygame.transform.scale(game_over_background, (width, height))
player_surf = pygame.image.load('assets/images/SKICHARACTER2.png').convert_alpha()
player_surf = pygame.transform.scale(player_surf, (100, 100))
tree_surf = pygame.image.load('assets/images/snow_108.png').convert_alpha()
rock_surf = pygame.image.load('assets/images/rock.png').convert_alpha()
coin_surf = pygame.image.load('assets/images/COIN_small.png').convert_alpha()
finish_line_surf = pygame.image.load('assets/images/finish_line.png').convert_alpha()

# Load sounds
coin_sound = pygame.mixer.Sound('assets/music/coins.mp3')
game_over_sound = pygame.mixer.Sound('assets/music/game-over.wav')
jump_sound = pygame.mixer.Sound('assets/music/jump.wav')
win_sound = pygame.mixer.Sound('assets/music/win.wav')
start_page_sound = pygame.mixer.Sound('assets/music/start_page.mp3')

# Game variables
player_x_pos = 0
player_y_pos = 500  # Change to initial y position (ground level)
player_rect = player_surf.get_rect(bottomleft=(player_x_pos, player_y_pos))
player_speed = 10

is_jumping = False
jump_velocity = -15  
gravity = 1
player_velocity_y = 0

obstacles = []
coins = []
score = 0
coins_collected = 0
lives = 3
distance = 0
FINISH_DISTANCE = 2000

game_state = "start"
game_over = False
game_won = False
high_scores = []
player_name = ""
start_music_playing = False

def spawn_obstacle():
    obstacle_type = random.choice(['tree', 'rock'])
    if obstacle_type == 'tree':
        obstacle_surf = tree_surf
        obstacle_x = random.randint(0,600)
        obstacle_y = random.randint(350, height - tree_surf.get_height())
    else:  
        obstacle_surf = rock_surf
        snow_ground_top = 500  
        snow_ground_bottom = 600
        obstacle_x = random.randint(0,600)
        obstacle_y = random.randint(snow_ground_top, snow_ground_bottom - rock_surf.get_height())
    
    obstacle_rect = obstacle_surf.get_rect(topleft=(obstacle_x, obstacle_y))
    obstacles.append((obstacle_type, obstacle_rect))

def spawn_coin():
    min_y = 400
    max_y = 500
  
    min_x = width
    max_x = width + 50  

    coin_rect = coin_surf.get_rect(topleft=(random.randint(min_x, max_x), random.randint(min_y, max_y)))
    coins.append(coin_rect)

def draw_start_screen():
    screen.blit(start_background, (0, 0))
    title_text = main_font.render("Ski Game", True, (255, 255, 255)) 
    start_text = ui_font.render("Press SPACE to start", True, (255, 255, 255))  
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 3))
    screen.blit(start_text, (width // 2 - start_text.get_width() // 2, height // 2))

def draw_score_board():
    screen.blit(score_background, (0, 0))
    title_text = main_font.render("High Scores", True, (0, 0, 0))  
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 50))

    for i, (name, score) in enumerate(high_scores[:5]):
        score_text = ui_font.render(f"{i+1}. {name}: {score}", True, (0, 0, 0))  
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 150 + i * 50))

    restart_text = ui_font.render("Press R to restart", True, (0, 0, 0)) 
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height - 100))

def reset_game():
    global player_rect, obstacles, coins, score, coins_collected, lives, distance, is_jumping, player_velocity_y, game_over, game_won, start_music_playing
    player_rect.bottomleft = (player_x_pos, player_y_pos)
    obstacles = []
    coins = []
    score = 0
    coins_collected = 0
    lives = 3
    distance = 0
    is_jumping = False
    player_velocity_y = 0
    game_over = False
    game_won = False
    start_music_playing = False

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if game_state == "start" and event.key == pygame.K_SPACE:
                game_state = "playing"
                start_page_sound.stop()
                start_music_playing = False
                reset_game()
            elif game_state == "playing" and not is_jumping and event.key == pygame.K_SPACE:
                is_jumping = True
                player_velocity_y = jump_velocity
                jump_sound.play()
            elif game_state == "game_over":
                if event.key == pygame.K_RETURN:
                    high_scores.append((player_name, score))
                    high_scores.sort(key=lambda x: x[1], reverse=True)
                    game_state = "score_board"
                elif event.key == pygame.K_r:
                    game_state = "start"
                    reset_game()
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode
            elif game_state == "score_board" and event.key == pygame.K_r:
                game_state = "start"

    if game_state == "start":
        if not start_music_playing:
            start_page_sound.play(-1)
            start_music_playing = True
        draw_start_screen()
    elif game_state == "playing":
        if start_music_playing:
            start_page_sound.stop()
            start_music_playing = False
        if not game_over and not game_won:
            # Player movement
            player_collision = pygame.Rect(player_rect.x, player_rect.bottom - 3, player_rect.width, 3)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_rect.x -= player_speed
                player_rect.y += 5
                if player_rect.left < 0:
                    player_rect.left = 0
                if player_rect.bottom > 600:
                    player_rect.bottom = 600
            if keys[pygame.K_RIGHT]:
                player_rect.x += player_speed
                player_rect.y -= 5 
                if player_rect.right > 400:
                    player_rect.right = 400
                if player_rect.top < 350:
                    player_rect.top = 350

            # Jumping
            if is_jumping:
                player_velocity_y += gravity
                player_rect.y += player_velocity_y
                if player_rect.bottom >= player_y_pos:
                    player_rect.bottom = player_y_pos
                    is_jumping = False
                    player_velocity_y = 0

            # Spawn obstacles and coins
            if random.randint(1, 120) == 1: 
                spawn_obstacle()
            if random.randint(1, 120) == 1:
                spawn_coin()

            # Move and draw obstacles and coins
            screen.blit(background_surf, (0, 0))
            for obstacle_type, obstacle_rect in obstacles:
                obstacle_rect.x -= 10
                obstacle_rect.y -= 5
                obstacle_collision = pygame.Rect(obstacle_rect.x, obstacle_rect.bottom - 10, 35, 10)
                if obstacle_type == 'tree':
                    screen.blit(tree_surf, obstacle_rect)
                else:
                    screen.blit(rock_surf, obstacle_rect)
                if obstacle_rect.right <= 0:
                    obstacles.remove((obstacle_type, obstacle_rect))
                if player_collision.colliderect(obstacle_collision):
                    lives -= 1
                    obstacles.remove((obstacle_type, obstacle_rect))
                    if lives <= 0:
                        game_over = True
                        game_over_sound.play()

            for coin_rect in coins[:]:
                coin_rect.x -= 10
                coin_rect.y -= 5
                screen.blit(coin_surf, coin_rect)
                if coin_rect.right <= 0:
                    coins.remove(coin_rect)
                if player_rect.colliderect(coin_rect):
                    coins.remove(coin_rect)
                    score += 10
                    coins_collected += 1
                    coin_sound.play()
                    if coins_collected % 10 == 0:
                        lives += 1

            # Draw player
            screen.blit(player_surf, player_rect)

            # Update and draw UI
            score_text = ui_font.render(f'Score: {score}  Coins: {coins_collected}', False, 'Black')
            lives_text = ui_font.render(f'Lives: {lives}', False, 'Red')
            screen.blit(score_text, (10, height - 40))
            screen.blit(lives_text, (10, 10))

            # Check for win condition
            distance += 1
            if distance >= FINISH_DISTANCE:
                finish_line_rect = finish_line_surf.get_rect(midbottom=(width // 2, height))
                screen.blit(finish_line_surf, finish_line_rect)
                if player_rect.colliderect(finish_line_rect):
                    game_won = True
                    win_sound.play()
                    game_state = "game_over"

        if game_over or game_won:
            game_state = "game_over"

    elif game_state == "game_over":
        if start_music_playing:
            start_page_sound.stop()
            start_music_playing = False
        if game_over:
            screen.blit(game_over_background, (0, 0))
            end_text = main_font.render("Game Over!", True, (255, 0, 0))
            screen.blit(end_text, (width // 2 - end_text.get_width() // 2, height // 3))
        else:  # Win the game
            screen.blit(win_background, (0, 0))

        name_text = ui_font.render(f"Enter your name: {player_name}", True, (0, 119, 204))
        screen.blit(name_text, (width // 2 - name_text.get_width() // 2, height - 120))

        submit_text = ui_font.render("Press ENTER to submit", True, (0, 119, 204))
        screen.blit(submit_text, (width // 2 - submit_text.get_width() // 2, height - 80))

        restart_text = ui_font.render("Press R to restart", True, (0, 119, 204))
        screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height - 40))

    elif game_state == "score_board":
        if start_music_playing:
            start_page_sound.stop()
            start_music_playing = False
        draw_score_board()

    pygame.display.update()
    clock.tick(60)

