# import random
import pygame as pg
# import numpy as np

from paraboloidTrack import Track
from player import Player
from screen import Screen
from game import Game

# Initialize the pygame
pg.mixer.pre_init(frequency=44100)
pg.init()
pg.mixer.init(frequency=44100)


screen1 = Screen(Screen.resolution_list[0])
game1 = Game(screen1)

FPS = 30  # frames per second setting
fpsClock = pg.time.Clock()

# Players speed
players_speed = 5 * screen1.height / 600

# Background
background = pg.image.load('Media/Images/background2.png')

# Sound
pg.mixer.music.load("Media/Sounds/background.wav")
pg.mixer.music.play(-1)
bulletSound = pg.mixer.Sound("Media/Sounds/laser.wav")

# Caption and Icon
pg.display.set_caption("Space Invader")
icon = pg.image.load('Media/Images/ufo.png')
pg.display.set_icon(icon)

# Target
targetImg = pg.image.load('Media/Images/target.png')
targetX = screen1.width // 2
targetY = targetImg.get_height() // 2 + 20


track1 = Track('left', x1=targetX, y1=targetY, x2=20, y2=screen1.height)
track2 = Track('right', x1=targetX, y1=targetY, x2=20, y2=screen1.height)


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


def target(x, y):
    x = x - targetImg.get_width() // 2
    y = y - targetImg.get_height() // 2
    screen1.screen.blit(targetImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen1.screen.blit(bulletImg, (x + 16, y + 10))


# Game Loop
running = True
while running:
    # Background Image
    screen1.screen.blit(background, (0, 0))
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
    collision = game1.is_collision(targetX, targetY, bulletX, bulletY)
    if collision:
        explosionSound = pg.mixer.Sound("Media/Sounds/explosion.wav")
        explosionSound.play()
        bulletY = 480
        bullet_state = "ready"
        game1.score_value += 1

    target(targetX, targetY)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player1.update()
    player2.update()
    game1.show_score()
    pg.display.update()
    fpsClock.tick(FPS)
