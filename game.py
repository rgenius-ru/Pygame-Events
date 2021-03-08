from pygame import font, image, mixer, display


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.is_round_over = False
        self.is_game_over = False

        self.win_round_player = None
        self.win_game_player = None
        self.players_names = []

        # Score
        self.font = font.Font('freesansbold.ttf', 32)
        self.score1_value = 0
        self.score2_value = 0

        self.score1_x = 10
        self.score1_y = 10

        self.score2_x = screen.width - 10
        self.score2_y = 10

        # Game Over
        self.game_over_font = font.Font('freesansbold.ttf', 64)

        # Round Over
        self.round_over_font = font.Font('freesansbold.ttf', 48)

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

    def show_score1(self):
        name = self.font.render(self.players_names[0], True, (200, 200, 0))
        self.screen.screen.blit(name, (self.score1_x, self.score1_y))

        score = self.font.render("Счёт : " + str(self.score1_value), True, (255, 255, 255))
        self.screen.screen.blit(score, (self.score1_x, self.score1_y + name.get_height() + 5))

    def show_score2(self):
        name = self.font.render(self.players_names[1], True, (200, 200, 0))
        self.screen.screen.blit(name, (self.score2_x - name.get_width(), self.score2_y))

        score = self.font.render("Счёт : " + str(self.score2_value), True, (255, 255, 255))
        self.screen.screen.blit(score, (self.score2_x - score.get_width(), self.score2_y + name.get_height() + 5))

    def game_over_text(self):
        over_text = self.game_over_font.render("GAME OVER", True, (255, 255, 255))
        self.screen.screen.blit(over_text, (200, 250))

    def round_over_text(self):
        over_text = self.round_over_font.render(f'Победил {self.win_round_player.name}', True, (255, 255, 255))
        x = self.screen.width // 2 - over_text.get_width() // 2
        y = self.screen.height - over_text.get_height() - 100
        self.screen.screen.blit(over_text, (x, y))

    def round_over(self):
        self.is_round_over = True
        self.round_over_text()

    def game_over(self):
        """
        Game Over
        :return:
        """
        self.is_game_over = True
        self.game_over_text()

    def update(self):
        self.screen.screen.blit(self.background, (0, 0))
        self.show_score1()
        self.show_score2()
        if self.is_round_over:
            self.round_over_text()
