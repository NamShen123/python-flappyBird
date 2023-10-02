import random
import pygame

# floor functions ----------
def draw_floor(screen, floor, floor_x_pos):
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos+ 432, 650))

# pipe function -------------
def create_pipe(pipe_surface, pipe_heights):
    pipe_space = 700
    random_pipe_pos = random.choice(pipe_heights)
    bottom_pipe = pipe_surface.get_rect(midtop= (500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop= (500, random_pipe_pos - pipe_space))

    return bottom_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes :
        pipe.centerx -= 5
    return pipes

def draw_pipe(screen, pipes, pipe_surface):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


# collision
def check_collision(bird_hitbox, pipes, hit_sound, die_sound):
    for pipe in pipes:
        if bird_hitbox.colliderect(pipe):
            hit_sound.play()
            return False
    
    if bird_hitbox.top <= -75 or bird_hitbox.bottom >= 650:
        hit_sound.play()
        die_sound.play()
        return False
    
    return True

# bird
def rotate_bird(bird, bird_movement):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
    return new_bird

def bird_animation(bird_list, bird_index, bird_hitbox):
    new_bird = bird_list[bird_index]
    new_bird_hitbox = new_bird.get_rect(center = (100, bird_hitbox.centery))
    return new_bird, new_bird_hitbox

# score
def score_display(screen, game_font, score, high_score, game_state):
    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center= (216, 20))
        screen.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center= (216, 20))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center= (216, 550))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score
