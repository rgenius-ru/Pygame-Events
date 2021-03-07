from pygame import image


class Target:
    def __init__(self, screen):
        self.screen = screen
        self.img = image.load('Media/Images/target.png')
        self._x = self.screen.width // 2 - self.img.get_width() // 2
        self._y = self.img.get_height() // 2 - self.img.get_height() // 2 + 20
        self.center_x = self._x + self.img.get_width() // 2
        self.center_y = self._y + self.img.get_height() // 2

    def update(self):
        self.screen.screen.blit(self.img, (self._x, self._y))
