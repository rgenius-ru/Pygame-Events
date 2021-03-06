import math
# import random
import pygame as pg

# Initialize the pygame
pg.mixer.pre_init(frequency=44100)
pg.init()
pg.mixer.init(frequency=44100)

# create the screen
# 1280×1024
# 1024×768
window_width = 800
window_height = 600
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

# Player
playerImg = pg.image.load('Media/Images/player.png')
playerX = 20
playerY = window_height - playerImg.get_height() // 2
playerX_change = 0
playerY_change = 0
player_gravity = 2

# Target
targetImg = pg.image.load('Media/Images/target.png')
targetX = window_width // 2
targetY = targetImg.get_height() // 2 + 20

# y = a(x-b)^2 + c
c = targetY
b = targetX
a = (playerY - c) / ((playerX - b) ** 2)
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


def player(x, y):
    x = x - playerImg.get_width() // 2
    y = y - playerImg.get_height() // 2
    screen.blit(playerImg, (x, y))


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
            if event.key == pg.K_LEFT:
                playerX_change = -5
            if event.key == pg.K_RIGHT:
                playerX_change = 5
            if event.key == pg.K_SPACE:
                playerY_change = -5
                if bullet_state == "ready":
                    bulletSound.play()
                    # Get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                playerX_change = 0
            if event.key == pg.K_SPACE:
                playerY_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerY += playerY_change + player_gravity
    if playerY <= 0:
        playerY = 0
    elif playerY >= window_height:
        playerY = window_height

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= window_width:
        playerX = window_width

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

    player(playerX, playerY)
    show_score(textX, testY)
    pg.display.update()
