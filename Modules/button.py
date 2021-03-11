from pygame import image, font, rect


class Button:
    def __init__(self, screen, position, text, img1, img2=None, is_active=True):
        """

        :param screen:
        :param img1:
        :param img2:
        :param position:
        :param text:
        """
        self.img_active = image.load(img1)
        if img2:
            self.img_inactive = image.load(img2)
        self.width = self.img_active.get_width()
        self.height = self.img_active.get_height()
        self.left = position[0] - self.width // 2
        self.top = position[1] - self.height // 2
        self.text = text
        self.screen = screen
        self.font = font.Font('freesansbold.ttf', 32)
        self.rect = rect.Rect(self.left, self.top, self.width, self.height)
        self.is_active = is_active

    def update(self):
        if self.is_active:
            color = (250, 250, 250)
            blit = self.screen.blit(self.img_active, (self.left, self.top))
        else:
            color = (160, 160, 160)
            blit = self.screen.blit(self.img_inactive, (self.left, self.top))
        text_render = self.font.render(self.text, True, color)
        left = self.left + self.width // 2 - text_render.get_width() // 2
        top = self.top + self.height // 2 - text_render.get_height() // 2
        self.screen.blit(text_render, (left, top))
        return blit

    def collide_point(self, position):
        """

        :param position: list of x, y
        :return: bool if collided
        """
        if not self.is_active:
            return False

        return self.rect.collidepoint(position)
