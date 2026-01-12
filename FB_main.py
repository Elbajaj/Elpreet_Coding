import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()              # [Variable] clock object to control FPS
fps = 60                                 # [Variable] frames per second

screen_width = 864                       # [Variable]
screen_height = 936                      # [Variable]

screen = pygame.display.set_mode((screen_width, screen_height))  # [Algorithm] create window
pygame.display.set_caption('Flappy Bird')

font = pygame.font.SysFont('Bauhaus 93', 60)    # [Variable] font object
white = (255, 255, 255)                         # [Variable] color tuple

ground_scroll = 0                       # [Variable] how far ground image has moved
scroll_speed = 4                        # [Variable] pipe/ground speed
flying = False                          # [Variable] game state flag
game_over = False                       # [Variable] game state flag
pipe_gap = 150                          # [Variable] gap between top/bottom pipes
pipe_frequency = 1500                   # [Variable] ms between pipe spawns
last_pipe = pygame.time.get_ticks() - pipe_frequency   # [Variable] time tracking
score = 0                               # [Variable]
pass_pipe = False                       # [Variable] scoring flag

bg = pygame.image.load('img/bg.png')            # [Variable] background image
ground_img = pygame.image.load('img/ground.png')# [Variable] ground image
button_img = pygame.image.load('img/restart.png')# [Variable] restart button image

def draw_text(text, font, text_col, x, y):
    # [Algorithm] draw score text onto the screen
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_game():
    # [Algorithm] reset everything needed for a fresh run
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0                       # [Variable] local reset score
    return score

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []            # [Variable] list of animation frames
        self.index = 0              # [Variable] current frame index
        self.counter = 0            # [Variable] animation timer counter

        for num in range(1, 4):     # [Loop] load bird frames
            img = pygame.image.load(f"img/bird{num}.png")
            self.images.append(img)

        self.image = self.images[self.index]     # [Variable]
        self.rect = self.image.get_rect()        # [Variable] hitbox rectangle
        self.rect.center = [x, y]                # [Variable] position
        self.vel = 0                              # [Variable] vertical velocity
        self.clicked = False                      # [Variable] click lock

    def update(self):
        #                           MOVEMENT PHYSICS 
        if flying:                                # [Conditional]
            self.vel += 0.5                       # [Algorithm] gravity
            if self.vel > 8:                      # [Conditional]
                self.vel = 8                      # [Algorithm] clamp fall speed
            if self.rect.bottom < 768:            # [Conditional] stay above ground line
                self.rect.y += int(self.vel)      # [Algorithm] move bird

        #                             INPUT + ANIMATION
        if not game_over:                         # [Conditional]
            # mouse flap
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:  # [Conditional]
                self.clicked = True               # [Variable]
                self.vel = -10                    # [Algorithm] flap upward
            if pygame.mouse.get_pressed()[0] == 0: # [Conditional]
                self.clicked = False              # [Algorithm] allow next click

            flap_cooldown = 5                     # [Variable] animation speed control
            self.counter += 1                     # [Algorithm] tick animation counter

            if self.counter > flap_cooldown:      # [Conditional]
                self.counter = 0
                self.index += 1                   # [Algorithm] next animation frame
                if self.index >= len(self.images):# [Conditional]
                    self.index = 0
                self.image = self.images[self.index]

            # [Algorithm] rotate based on velocity (tilt up/down)
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            # [Algorithm] if game over, point bird downward
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/pipe.png")  # [Variable]
        self.rect = self.image.get_rect()               # [Variable]

        if position == 1:                        # [Conditional] top pipe
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]  # [Algorithm] place top pipe
        elif position == -1:                     # [Conditional] bottom pipe
            self.rect.topleft = [x, y + int(pipe_gap / 2)]     # [Algorithm] place bottom pipe

    def update(self):
        self.rect.x -= scroll_speed              # [Algorithm] move pipe left
        if self.rect.right < 0:                  # [Conditional] off-screen cleanup
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image                       # [Variable]
        self.rect = self.image.get_rect()        # [Variable]
        self.rect.topleft = (x, y)

    def draw(self):
        action = False                           # [Variable]
        pos = pygame.mouse.get_pos()             # [Variable]
        if self.rect.collidepoint(pos):          # [Conditional] mouse over button
            if pygame.mouse.get_pressed()[0] == 1: # [Conditional] click
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

pipe_group = pygame.sprite.Group()              # [Variable] holds all pipes
bird_group = pygame.sprite.Group()              # [Variable] holds bird sprite(s)

flappy = Bird(100, int(screen_height / 2))      # [Variable] the player bird
bird_group.add(flappy)                          # [Algorithm] add bird into sprite group

button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)  # [Variable]

run = True                                      # [Variable] main loop flag
while run:                                      # [Loop] MAIN GAME LOOP
    clock.tick(fps)                             # [Algorithm] keep FPS steady

    # [Algorithm] draw background + objects
    screen.blit(bg, (0,0))
    pipe_group.draw(screen)
    bird_group.draw(screen)
    bird_group.update()
    screen.blit(ground_img, (ground_scroll, 768))

    #                           SCORING LOGIC
    if len(pipe_group) > 0:                     # [Conditional]
        # [Algorithm] detect bird inside pipe to allow scoring once
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and not pass_pipe:                  # [Conditional]
            pass_pipe = True                    # [Variable]

        # [Algorithm] once bird fully passes pipe, add score
        if pass_pipe:                           # [Conditional]
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:  # [Conditional]
                score += 1                      # [Variable] score increases
                pass_pipe = False               # [Algorithm] reset scoring flag

    draw_text(str(score), font, white, int(screen_width / 2), 20)  # [Algorithm] display score

    #                       COLLISION / GAME OVER RULES
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        # [Algorithm] hit a pipe OR flew above screen -> game over
        game_over = True                        # [Variable]

    if flappy.rect.bottom >= 768:               # [Conditional] hit ground
        game_over = True
        flying = False                          # [Algorithm] stop flight

    #                       PIPE SPAWNING + SCROLLING
    if flying and not game_over:                # [Conditional]
        time_now = pygame.time.get_ticks()      # [Variable]

        if time_now - last_pipe > pipe_frequency:  # [Conditional]
            # [Algorithm] spawn a new pair of pipes at a random height
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now                # [Algorithm] remember last spawn time

        pipe_group.update()                     # [Algorithm] move pipes

        ground_scroll -= scroll_speed           # [Algorithm] move ground
        if abs(ground_scroll) > 35:             # [Conditional] loop ground texture
            ground_scroll = 0

    #                       RESTART BUTTON
    if game_over:                               # [Conditional]
        if button.draw():                       # [Conditional]
            game_over = False
            score = reset_game()                # [Algorithm] reset and restart

    #                      EVENT HANDLING
    for event in pygame.event.get():            # [Loop] check all events
        if event.type == pygame.QUIT:           # [Event]
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
            # [Event] first click starts the game
            flying = True                       # [Algorithm]

    pygame.display.update()                     # [Algorithm] refresh screen

pygame.quit()