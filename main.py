import pygame as pg
import math
from pygame_textinput import TextInput
# import random
# import numpy as np

from paraboloidTrack import Track
from player import Player
from screen import Screen
from game import Game
from target import Target
from button import Button

# Initialize the pygame
pg.mixer.pre_init(frequency=44100)
pg.init()
pg.mixer.init(frequency=44100)

screen1 = Screen(resolution_id=3)
screen2 = Screen(resolution_id=3)

game1 = Game(screen1, screen2)
game1.init_screen1()
target1 = Target(screen1)

track1 = Track('left', x1=target1.center_x, y1=target1.center_y, x2=20, y2=screen1.height)
track2 = Track('right', x1=target1.center_x, y1=target1.center_y, x2=20, y2=screen1.height)

player1 = Player(pg.image.load('Media/Images/player.png'),
                 name='Игрок 1',
                 scr=screen1.screen,
                 track=track1,
                 x=20,
                 y=screen1.height,
                 gravity=game1.gravity,
                 speed=screen1.height / 120
                 )
player2 = Player(pg.image.load('Media/Images/player.png'),
                 name='Игрок 2',
                 scr=screen1.screen,
                 track=track2,
                 x=screen1.width - 20,
                 y=screen1.height,
                 gravity=game1.gravity,
                 speed=screen1.height / 120
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
        pg.draw.circle(game1.screen2.screen, (0, 0, 220), (track.get_x(y), y), radius=1, width=1)


def game1_screen2_loop():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False

        if not game1.is_round_over:
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

    if not game1.is_round_over:
        # Collision
        collision_player1 = is_collision(target1.center_x, target1.center_y, player1.x, player1.y)
        collision_player2 = is_collision(target1.center_x, target1.center_y, player2.x, player2.y)

        if collision_player1 or collision_player2:
            if collision_player1:
                player2.stop()
                game1.score1_value += 1
                game1.win_round_player = player1
            if collision_player2:
                player1.stop()
                game1.score2_value += 1
                game1.win_round_player = player2

            explosion_sound = pg.mixer.Sound("Media/Sounds/explosion.wav")
            explosion_sound.play()
            game1.round_over()
    # else:
    #     game1.round_over()

    return True


def text1_update(_events):
    x, y, w, h = 20, 20, 300, 40
    rect = draw_rect(x, y, w, h, game1.screen1.screen)

    text_input1.update(_events)
    text1_position = (x + 5, y + 5)
    game1.screen1.screen.blit(text_input1.get_surface(), text1_position)

    return rect


def text2_update(_events):
    w, h = 300, 40
    x, y = game1.screen1.width - w - 20, 20
    rect = draw_rect(x, y, w, h, game1.screen1.screen)

    text_input2.update(_events)
    text2_position = (x + 5, y + 5)
    game1.screen1.screen.blit(text_input2.get_surface(), text2_position)

    return rect


def draw_rect(x, y, w, h, screen):
    pg.draw.rect(screen, (140, 140, 140), pg.Rect(x, y, w, h), width=3, border_radius=5)
    return pg.draw.rect(screen, (240, 240, 240), pg.Rect(x+1, y+1, w-2, h-2), width=0, border_radius=5)


left = game1.screen1.width // 2
top = game1.screen1.height

button_run = Button(game1.screen1.screen, 'Media/Images/button_run.png', (left, top - 160), 'Играть')
button_quit = Button(game1.screen1.screen, 'Media/Images/button_quit.png', (left, top - 80), 'Выход')


def game1_screen1_loop():
    game1.screen1.screen.blit(game1.background1, (0, 0))

    button_run.update()
    button_quit.update()

    events = pg.event.get()

    text_player1 = text1_update(events)
    text_player2 = text2_update(events)

    for event in events:
        if event.type == pg.QUIT:
            return False
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_position = pg.mouse.get_pos()
            if button_run.collide_point(mouse_position):
                global game1_screen
                game1_screen = 2
                players_names = text_input1.get_text(), text_input2.get_text()
                game1.init_screen2(players_names)
                return True
            elif button_quit.collide_point(mouse_position):
                return False
            elif text_player1.collidepoint(mouse_position):
                text_input1.focused = True
                text_input2.focused = False
            elif text_player2.collidepoint(mouse_position):
                text_input2.focused = True
                text_input1.focused = False

    return True


game1_screen = 1
game1.players_names = player1.name, player2.name

# Create TextInput-object
text_input1 = TextInput(focused=True)
text_input2 = TextInput(focused=False)

# Game Loop
running = True
while running:
    if game1_screen == 1:
        running = game1_screen1_loop()
    elif game1_screen == 2:
        running = game1_screen2_loop()
        game1.update()  # Game update first
        target1.update()  # Second update target
        player1.update()
        player2.update()

        # ***************** Debug *********************
        # pg.draw.circle(game1.screen.screen, (0, 200, 0), (target1.center_x, target1.center_y), radius=60, width=2)
        # pg.draw.circle(game1.screen.screen, (220, 0, 0), (player1.x, player1.y), radius=20, width=2)
        # pg.draw.circle(game1.screen.screen, (220, 0, 0), (player2.x, player2.y), radius=20, width=2)
        #
        # w = player1.img_rotated.get_width()
        # h = player1.img_rotated.get_height()
        # x = player1.x - w // 2
        # y = player1.y - h // 2
        # pg.draw.rect(game1.screen.screen, (0, 0, 220), pg.Rect(x, y, w, h), width=1)
        #
        # w = player2.img_rotated.get_width()
        # h = player2.img_rotated.get_height()
        # x = player2.x - w // 2
        # y = player2.y - h // 2
        # pg.draw.rect(game1.screen.screen, (0, 0, 220), pg.Rect(x, y, w, h), width=1)
        #
        # draw_track(track1)
        # draw_track(track2)
        # *************** END * Debug *****************

    pg.display.update()
    fpsClock.tick(FPS)
