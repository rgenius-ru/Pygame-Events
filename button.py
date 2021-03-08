from pygame import image, font, rect


class Button:
    def __init__(self, screen, img: str, position, text):
        """

        :param screen:
        :param img:
        :param position:
        :param text:
        """
        self.img = image.load(img)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.left = position[0] - self.width // 2
        self.top = position[1] - self.height // 2
        self.text = text
        self.screen = screen
        self.font = font.Font('freesansbold.ttf', 32)
        self.rect = rect.Rect(self.left, self.top, self.width, self.height)

    def update(self):
        blit = self.screen.blit(self.img, (self.left, self.top))
        text_render = self.font.render(self.text, True, (250, 250, 250))
        left = self.left + self.width // 2 - text_render.get_width() // 2
        top = self.top + self.height // 2 - text_render.get_height() // 2
        self.screen.blit(text_render, (left, top))
        return blit

    def collide_point(self, position):
        """

        :param position: list of x, y
        :return: bool if collided
        """
        return self.rect.collidepoint(position)
