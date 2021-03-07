import pygame as pg
# import random
# import numpy as np

from paraboloidTrack import Track
from player import Player
from screen import Screen
from game import Game
from target import Target


# Initialize the pygame
pg.mixer.pre_init(frequency=44100)
pg.init()
pg.mixer.init(frequency=44100)


screen1 = Screen(Screen.resolution_list[0])
game1 = Game(screen1)
target1 = Target(screen1)

# Frames per second setting
FPS = 30
fpsClock = pg.time.Clock()

# Players speed
players_speed = 5 * screen1.height / 600

bulletSound = pg.mixer.Sound("Media/Sounds/laser.wav")


track1 = Track('left', x1=target1.center_x, y1=target1.center_y, x2=20, y2=screen1.height)
track2 = Track('right', x1=target1.center_x, y1=target1.center_y, x2=20, y2=screen1.height)


player1 = Player(pg.image.load('Media/Images/player.png'),
                 scr=screen1.screen,
                 track=track1,
                 x=20,
                 y=screen1.height,
                 gravity=game1.gravity
                 )
player2 = Player(pg.image.load('Media/Images/player.png'),
                 scr=screen1.screen,
                 track=track2,
                 x=screen1.width-20,
                 y=screen1.height,
                 gravity=game1.gravity
                 )


# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pg.image.load('Media/Images/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen1.screen.blit(bulletImg, (x + 16, y + 10))


# Game Loop
running = True
while running:
    # Background Image
    screen1.screen.blit(game1.background, (0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                # player1_y_change = -players_speed
                player1.launch()
                if bullet_state == "ready":
                    bulletSound.play()
                    # Get the current x coordinate of the spaceship
                    bulletX = player1.x
                    fire_bullet(bulletX, bulletY)
            if event.key == pg.K_UP:
                player2.launch()

        if event.type == pg.KEYUP:
            if event.key == pg.K_w:
                player1.stop()
            if event.key == pg.K_UP:
                player2.stop()

    # Collision
    collision = game1.is_collision(target1.center_x, target1.center_y, bulletX, bulletY)
    if collision:
        explosionSound = pg.mixer.Sound("Media/Sounds/explosion.wav")
        explosionSound.play()
        bulletY = 480
        bullet_state = "ready"
        game1.score_value += 1

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    target1.update()
    player1.update()
    player2.update()
    game1.show_score()
    pg.display.update()
    fpsClock.tick(FPS)
