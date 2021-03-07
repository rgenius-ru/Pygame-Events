from pygame import font, image, mixer, display


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.is_round_over = False
        self.is_game_over = False

        # Score
        self.font = font.Font('freesansbold.ttf', 32)
        self.score1_value = 0
        self.score2_value = 0

        self.score1_x = 10
        self.score1_y = 10

        self.score2_x = screen.width - 10
        self.score2_y = 10

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
        self.show_score1()
        self.show_score2()

    def show_score1(self):
        score = self.font.render("Score : " + str(self.score1_value), True, (255, 255, 255))
        self.screen.screen.blit(score, (self.score1_x, self.score1_y))

    def show_score2(self):
        score = self.font.render("Score : " + str(self.score2_value), True, (255, 255, 255))
        self.screen.screen.blit(score, (self.score2_x - score.get_width(), self.score2_y))

    def game_over_text(self):
        over_text = self.over_font.render("GAME OVER", True, (255, 255, 255))
        self.screen.screen.blit(over_text, (200, 250))

    def round_over(self):
        self.is_round_over = True

    def game_over(self):
        """
        Game Over
        :return:
        """
        self.is_game_over = True
        self.game_over_text()
