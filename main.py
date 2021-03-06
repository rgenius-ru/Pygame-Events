import math
# import random
import pygame as pg
import numpy as np

# Initialize the pygame
pg.mixer.pre_init(frequency=44100)
pg.init()
pg.mixer.init(frequency=44100)

FPS = 30  # frames per second setting
fpsClock = pg.time.Clock()

# create the screen
# 1280×1024
# 1024×768
screen_size = ((800, 600), (1024, 768), (1280, 1024), (1440, 960), (1920, 1080))
window_width, window_height = screen_size[3]
screen = pg.display.set_mode((window_width, window_height))

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

# Gravity
gravity = 1 * window_height / 600

# Players speed
players_speed = 5 * window_height / 600

# Player 1
player1_img = pg.image.load('Media/Images/player.png')
player1_img_rotated = player1_img
player1_x = 20
player1_y = window_height - player1_img.get_height() // 2
player1_x_change = 0
player1_y_change = 0
player1_angle_deg = -65

# Player 2
player2_img = pg.image.load('Media/Images/player.png')
player2_img_rotated = player2_img
player2_x = window_width - player2_img.get_width() // 2 - 20
player2_y = window_height - player2_img.get_height() // 2
player2_x_change = 0
player2_y_change = 0
player2_angle_deg = -65

# Target
targetImg = pg.image.load('Media/Images/target.png')
targetX = window_width // 2
targetY = targetImg.get_height() // 2 + 20

# Paraboloid
# y = a(x-b)^2 + c
c = targetY
b = targetX
a = (player1_y - c) / ((player1_x - b) ** 2)
print(a, b, c)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pg.image.load('Media/Images/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score

score_value = 0
font = pg.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pg.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y, img):
    x = x - img.get_width() // 2
    y = y - img.get_height() // 2
    screen.blit(img, (x, y))


def target(x, y):
    x = x - targetImg.get_width() // 2
    y = y - targetImg.get_height() // 2
    screen.blit(targetImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                player1_y_change = -players_speed
                if bullet_state == "ready":
                    bulletSound.play()
                    # Get the current x coordinate of the spaceship
                    bulletX = player1_x
                    fire_bullet(bulletX, bulletY)
            if event.key == pg.K_UP:
                player2_y_change = -players_speed

        if event.type == pg.KEYUP:
            if event.key == pg.K_w:
                player1_y_change = 0
            if event.key == pg.K_UP:
                player2_y_change = 0

    # Player 1
    if player1_y - players_speed > c:
        player1_y += player1_y_change + gravity
        player1_x = b - ((player1_y - c) / a) ** 0.5  # paraboloid movement
    else:
        player1_y += gravity

    if player1_y <= 0:
        player1_y = 0
    elif player1_y > window_height - player1_img.get_height() // 2:
        player1_y = window_height - player1_img.get_height() // 2

    player1_angle_rad = np.arctan(2 * a * (player1_x - b))  # tan(angle) = y' = (a(x-b)^2)' = 2a(x-b)
    player1_angle_delta = player1_angle_deg - np.degrees(player1_angle_rad)
    player1_angle_delta = int(player1_angle_delta)
    if np.abs(player1_angle_delta) > 1:
        player1_angle_deg -= player1_angle_delta
        player1_img_rotated = pg.transform.rotate(player1_img, -player1_angle_deg - 65)
        player1_angle_delta = 0

    # Player 2
    if player2_y - players_speed > c:
        player2_y += player2_y_change + gravity
        player2_x = ((player2_y - c) / a) ** 0.5 + b  # paraboloid movement
    else:
        player2_y += gravity

    if player2_y <= 0:
        player2_y = 0
    elif player2_y > window_height - player2_img.get_height() // 2:
        player2_y = window_height - player2_img.get_height() // 2

    player2_angle_rad = np.arctan(2 * a * (player2_x - b))  # tan(angle) = y' = (a(x-b)^2)' = 2a(x-b)
    player2_angle_delta = player2_angle_deg - np.degrees(player2_angle_rad)
    player2_angle_delta = int(player2_angle_delta)
    if np.abs(player2_angle_delta) > 1:
        player2_angle_deg -= player2_angle_delta
        player2_img_rotated = pg.transform.rotate(player2_img, -player2_angle_deg + 65)
        player2_angle_delta = 0

    # Game Over
    if targetY > 440:
        targetY = 2000
        game_over_text()
        break

    # Collision
    collision = is_collision(targetX, targetY, bulletX, bulletY)
    if collision:
        explosionSound = pg.mixer.Sound("Media/Sounds/explosion.wav")
        explosionSound.play()
        bulletY = 480
        bullet_state = "ready"
        score_value += 1

    target(targetX, targetY)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(player1_x, player1_y, player1_img_rotated)
    player(player2_x, player2_y, player2_img_rotated)
    show_score(textX, testY)
    pg.display.update()
    fpsClock.tick(FPS)
