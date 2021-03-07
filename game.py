import math
from pygame import font, image, mixer, display


class Game:
    def __init__(self, screen):
        self.screen = screen

        # Score
        self.score_value = 0
        self.font = font.Font('freesansbold.ttf', 32)

        self.score_x = 10
        self.score_y = 10

        # Game Over
        self.over_font = font.Font('freesansbold.ttf', 64)

        # Game
        self.flag_game_over = False

        # Gravity
        self.gravity = 1 * screen.height / 600

        # Background
        self.background = image.load('Media/Images/background2.png')

        # Sound
        mixer.music.load("Media/Sounds/background.wav")
        mixer.music.play(-1)

        # Caption and Icon
        display.set_caption("Space Invader")
        icon = image.load('Media/Images/ufo.png')
        display.set_icon(icon)

    def update(self):
        self.screen.screen.blit(self.background, (0, 0))
        self.show_score()

    def show_score(self):
        score = self.font.render("Score : " + str(self.score_value), True, (255, 255, 255))
        self.screen.screen.blit(score, (self.score_x, self.score_y))

    def game_over_text(self):
        over_text = self.over_font.render("GAME OVER", True, (255, 255, 255))
        self.screen.screen.blit(over_text, (200, 250))

    def is_collision(self, enemy_x, enemy_y, bullet_x, bullet_y):
        distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + (math.pow(enemy_y - bullet_y, 2)))
        if distance < 27:
            return True
        else:
            return False

    def round_over(self):
        pass

    def game_over(self):
        """
        Game Over
        :return:
        """
        self.game_over_text()

    # # Collision
    # collision = game1.is_collision(target1.center_x, target1.center_y, bulletX, bulletY)
    # if collision:
    #     explosionSound = pg.mixer.Sound("Media/Sounds/explosion.wav")
    #     explosionSound.play()
    #     bulletY = 480
    #     bullet_state = "ready"
    #     game1.score_value += 1
