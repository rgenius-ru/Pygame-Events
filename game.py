import math
from pygame.font import Font


class Game:
    def __init__(self, screen):
        self.screen = screen

        # Score
        self.score_value = 0
        self.font = Font('freesansbold.ttf', 32)

        self.score_x = 10
        self.score_y = 10

        # Game Over
        self.over_font = Font('freesansbold.ttf', 64)

        # Game
        self.flag_game_over = False

        # Gravity
        self.gravity = 1 * screen.height / 600

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
