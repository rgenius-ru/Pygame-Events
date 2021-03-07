from numpy import abs
from pygame.transform import rotate


class Player:
    def __init__(self, pg_img, scr, track, x, y, angle_deg=-65, gravity=1, speed=5):
        self.screen = scr
        self.img = pg_img
        self.img_rotated = self.img
        self._y = y - self.img.get_height()
        self._x = track.get_x(self._y) - self.img.get_width() // 2
        self.x = self._x + self.img.get_width() // 2
        self.y = self._y + self.img.get_height() // 2
        self.speed = speed
        self.track = track
        self.x_change = 0
        self.y_change = 0
        self.angle_deg = angle_deg
        self.gravity = gravity

    def launch(self):
        self.y_change = -self.speed

    def stop(self):
        self.y_change = 0

    def move(self):
        if self._y - self.speed > self.track.y_min:
            self._y += self.y_change + self.gravity  # - self.img_rotated.get_height() // 2
            self._x = self.track.get_x(self._y) - self.img_rotated.get_width() // 2
        else:
            self._y += self.gravity

        if self._y <= 0:
            self._y = 0
        elif self._y > self.screen.get_height() - self.img.get_height():
            self._y = self.screen.get_height() - self.img.get_height()

        angle_delta = self.angle_deg - self.track.tangent_angle(self._x)
        angle_delta = int(angle_delta)
        if abs(angle_delta) > 1:
            self.angle_deg -= angle_delta
            self.rotate(-self.angle_deg - 70)

    def redraw(self, img):
        self.screen.blit(img, (self._x, self._y))

    def rotate(self, angle_deg):
        self.img_rotated = rotate(self.img, angle_deg)

    def update(self):
        self.x = self._x + self.img_rotated.get_width() // 2
        self.y = self._y + self.img_rotated.get_height() // 2
        self.redraw(self.img_rotated)
        self.move()
