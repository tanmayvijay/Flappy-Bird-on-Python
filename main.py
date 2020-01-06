import random
import sys
import pygame
from pygame.locals import *

# print(pygame.__version__)

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = int(SCREENHEIGHT * 0.8)
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'



def welcome_screen():
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height() )/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width() )/2)
    messagey = int (SCREENHEIGHT * 0.13)
    basex = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0,0)),
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery)),
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey)),
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)






def main_game():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/2)
    basex = 0

    new_pipe_1 = get_random_pipe()
    new_pipe_2 = get_random_pipe()


    upper_pipes = [
        {'x': SCREENWIDTH + 200, 'y': new_pipe_1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': new_pipe_1[1]['y']},
    ]

    lower_pipes = [
        {'x': SCREENWIDTH + 200, 'y': new_pipe_2[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': new_pipe_2[1]['y']},
    ]


    pipe_vel_x = -4
    player_vel_y = -9
    player_max_vel_y = 10
    player_min_vel_y = -8
    player_acc_y = 1

    player_flap_acc_v = -8
    player_flapped = False


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    player_vel_y = player_flap_acc_v
                    player_flapped = True
                    GAME_SOUNDS['wing'].play()

    
    crash_test = is_collide(playerx, playery, upper_pipes, lower_pipes)

    if crash_test:
        return
    
    player_mid_pos = playerx + GAME_SPRITES['player'].get_width()/2
    for pipe in upper_pipes:
        pipe_mid_pos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
        if pipe_mid_pos <= player_mid_pos < pipe_mid_pos + 4:
            score += 1
            print(f"Your Score is {score}")
        GAME_SOUNDS['point'].play()


    
    if player_vel_y < player_max_vel_y and not player_flapped:
        player_vel_y += player_acc_y

    if player_flapped:
        player_flapped = False

    player_height = GAME_SPRITES['player'].get_height()
    playery = playery + min(player_vel_y, GROUNDY - playery - player_height)


    for upperPipe, lowerPipe in zip(upper_pipes, lower_pipes):
        upperPipe['x'] += pipe_vel_x
        lowerPipe['x'] += pipe_vel_x

    if 0 < upper_pipes[0]['x'] < 5:
        new_pipe = get_random_pipe()
        upper_pipes.append(new_pipe[0])
        lower_pipes.append(new_pipe[1])



    if upper_pipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
        upper_pipes.pop(0)
        lower_pipes.pop(0)

    
    SCREEN.blit(GAME_SPRITES['background'], (0, 0))
    for upperPipe, lowerPipe in zip(upper_pipes, lower_pipes):
        SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
        SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
    
    SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
    SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

    my_digits = [int(x) for x in list(str(score))]
    width = 0
    for digit in my_digits:
        width += GAME_SPRITES['numbers'][digit].get_width()
    x_offset = (SCREENWIDTH - width)/2

    for digit in my_digits:
        SCREEN.blit(GAME_SPRITES['numbers'][digit], (x_offset, SCREENHEIGHT*0.12))
        x_offset += GAME_SPRITES['numbers'][digit].get_width()

    pygame.display.update()
    FPSCLOCK.tick(FPS)









def get_random_pipe():
    pipe_height = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipex = SCREENWIDTH + 10
    y1 = pipe_height - y2 + offset
    pipe = [
        {'x': pipex, 'y': -y1},
        {'x': pipex, 'y': y2}
    ]

    return pipe







if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird")
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha()
    )

    GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )


    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()


    while True:
        welcome_screen()
        main_game()
















