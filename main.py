import pygame as pg
import math
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


def is_collision(obj1_x, obj1_y, obj2_x, obj2_y):
    distance = math.sqrt(math.pow(obj1_x - obj2_x, 2) + (math.pow(obj1_y - obj2_y, 2)))
    if distance < 60:
        return True
    else:
        return False


def draw_track(track):
    for y in range(track.y_min, track.y_max):
        pg.draw.circle(game1.screen.screen, (0, 0, 220), (track.get_x(y), y), radius=1, width=1)


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

    # Collision
    collision_player1 = is_collision(target1.center_x, target1.center_y, player1.x, player1.y)
    collision_player2 = is_collision(target1.center_x, target1.center_y, player2.x, player2.y)

    if collision_player1 or collision_player2:
        explosionSound = pg.mixer.Sound("Media/Sounds/explosion.wav")
        explosionSound.play()
        game1.round_over()

    if collision_player1:
        game1.score1_value += 1
    if collision_player2:
        game1.score2_value += 1

    game1.update()  # Game update first
    target1.update()  # Second update target
    player1.update()
    player2.update()
    pg.draw.circle(game1.screen.screen, (0, 200, 0), (target1.center_x, target1.center_y), radius=60, width=2)
    pg.draw.circle(game1.screen.screen, (220, 0, 0), (player1.x, player1.y), radius=20, width=2)
    pg.draw.circle(game1.screen.screen, (220, 0, 0), (player2.x, player2.y), radius=20, width=2)
    draw_track(track1)
    draw_track(track2)
    pg.display.update()
    fpsClock.tick(FPS)
