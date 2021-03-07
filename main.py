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


screen1 = Screen(resolution_id=3)
game1 = Game(screen1)
target1 = Target(screen1)


track1 = Track('left', x1=target1.center_x, y1=target1.center_y, x2=20, y2=screen1.height)
track2 = Track('right', x1=target1.center_x, y1=target1.center_y, x2=20, y2=screen1.height)


player1 = Player(pg.image.load('Media/Images/player.png'),
                 scr=screen1.screen,
                 track=track1,
                 x=20,
                 y=screen1.height,
                 gravity=game1.gravity,
                 speed=screen1.height/120
                 )
player2 = Player(pg.image.load('Media/Images/player.png'),
                 scr=screen1.screen,
                 track=track2,
                 x=screen1.width-20,
                 y=screen1.height,
                 gravity=game1.gravity,
                 speed=screen1.height/120
                 )


# Frames per second setting
FPS = 30
fpsClock = pg.time.Clock()


def is_collision(self, enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                player1.launch()
            if event.key == pg.K_UP:
                player2.launch()

        if event.type == pg.KEYUP:
            if event.key == pg.K_w:
                player1.stop()
            if event.key == pg.K_UP:
                player2.stop()

    # # Collision
    # collision = game1.is_collision(target1.center_x, target1.center_y, bulletX, bulletY)
    # if collision:
    #     explosionSound = pg.mixer.Sound("Media/Sounds/explosion.wav")
    #     explosionSound.play()
    #     bulletY = 480
    #     bullet_state = "ready"
    #     game1.score_value += 1

    game1.update()  # Game update first
    target1.update()  # Second update target
    player1.update()
    player2.update()
    pg.display.update()
    fpsClock.tick(FPS)
