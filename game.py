import pygame, sys
from function.common import *

pygame.mixer.pre_init()
pygame.init()


screen= pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 40)

gravity = 0.2
bird_movement = 0
game_active = True
score = 0
high_score = 0
 
# Draw back ground
bg = pygame.image.load('./assests/background-night.png').convert()
bg = pygame.transform.scale2x(bg)

# Draw floor
floor = pygame.image.load('./assests/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

# Draw bird
bird_down = pygame.image.load('./assests/yellowbird-downflap.png').convert_alpha()
bird_mid = pygame.image.load('./assests/yellowbird-midflap.png').convert_alpha()
bird_up = pygame.image.load('./assests/yellowbird-upflap.png').convert_alpha()
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]

# bird = pygame.image.load('./assests/yellowbird-midflap.png').convert_alpha()
bird = pygame.transform.scale2x(bird)
bird_hitbox = bird.get_rect(center= (100, 300))

#bird timmer
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)

# Draw pipe
pipe_surface = pygame.image.load('./assests/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

# Make timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_heights = [300, 400, 500]

# Game over screen
game_over_surface = pygame.image.load('./assests/message.png').convert_alpha()
game_over_surface = pygame.transform.scale2x(game_over_surface)
game_over_rect = game_over_surface.get_rect(center=(216, 284))

# Sound effect
flap_sound = pygame.mixer.Sound('./sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('./sound/sfx_hit.wav')
die_sound = pygame.mixer.Sound('./sound/sfx_die.wav')
score_sound = pygame.mixer.Sound('./sound/sfx_point.wav')
score_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0 
                bird_movement = -7
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active==False:
                game_active = True
                pipe_list.clear()
                bird_hitbox.center = (100, 300)
                bird_movement = 0
                score = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe(pipe_surface, pipe_heights))
        
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
        
            ird, bird_hitbox = bird_animation(bird_list, bird_index, bird_hitbox)

    screen.blit(bg,(0,0))
    if game_active:
        # bird
        bird_movement += gravity
        rotated_bird =  rotate_bird(bird, bird_movement)
        bird_hitbox.centery += bird_movement
        screen.blit(rotated_bird,bird_hitbox)
        game_active= check_collision(bird_hitbox ,pipe_list, hit_sound, die_sound)

        # pipe
        pipe_list = move_pipe(pipe_list)
        draw_pipe(screen, pipe_list, pipe_surface)

        #score 
        score += 0.01
        score_display(screen, game_font, score, high_score, 'main_game')
        score_countdown -= 1
        if score_countdown <= 0:
            score_sound.play()
            score_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display(screen, game_font, score, high_score, 'game_over')

    # floor
    floor_x_pos -= 1
    draw_floor(screen, floor, floor_x_pos) 
    if floor_x_pos <= -243:
        floor_x_pos = 0

    screen.blit(floor,(floor_x_pos,600))
    pygame.display.update()
    clock.tick(120)