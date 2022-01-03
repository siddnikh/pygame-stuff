from os import pipe
import pygame
from pygame import time
from pygame.locals import *
from Bird import Bird
from Pipe import Pipe
import random

#Fundamentals/Initialization
pygame.init()

clock = pygame.time.Clock()
fps = 60

SCREEN_WIDTH = 864
SCREEN_HEIGHT = 936

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

#Assets
bg = pygame.image.load('assets/bg.png')
ground = pygame.image.load('assets/ground.png')
btn_img = pygame.image.load('assets/restart.png')

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        #position of mouse
        pos = pygame.mouse.get_pos()

        #check mouse collision
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

#Variables
ground_scroll = 0
scroll_speed = 4 #Please change scroll speed in Pipe.py as well if you're changing this
pipe_gap = 150
pipe_frequency = 1500 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
global score
score = 0
pass_pipe = False

font = pygame.font.SysFont('Bauhaus 93', 100)
white = (255, 255, 255)

#Sprites
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(SCREEN_HEIGHT / 2))
bird_group.add(flappy)

restart_btn = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 100, btn_img)

#Main loop
run = True
while run:

    clock.tick(fps)

    #loading assets on screen
    screen.blit(bg, (0, 0))
    bird_group.draw(screen)
    pipe_group.draw(screen)
    screen.blit(ground, (ground_scroll, 768))

    #check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
            
    draw_text(str(score), font, white, int(SCREEN_WIDTH / 2), 20)

    #Collisions between bird and pipe
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        flappy.game_over = True

    #Checking if bird hit the ground
    if flappy.rect.bottom >= 768:
        flappy.game_over = True
        flappy.flying = False
    
    bird_group.update()

    if flappy.game_over == False:

        #generating new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency and flappy.flying == True:
            pipe_height = random.randint(- 150, 150)
            btm_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + int(pipe_gap / 2) + pipe_height, -1)
            top_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) - int(pipe_gap / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        #scrolling the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
        
        pipe_group.update()

    if flappy.game_over == True:
        if restart_btn.draw() == True:
            pipe_group.empty()
            score = flappy.reset(100, int(SCREEN_HEIGHT / 2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flappy.flying == False and flappy.game_over == False:
            flappy.flying = True

    pygame.display.update()

pygame.quit()