from numpy import abs
from pygame.transform import rotate


class Player:
    def __init__(self, pg_img, scr, track, x, y, angle_deg=-65, gravity=1, speed=5):
        self.screen = scr
        self.img = pg_img
        self.img_rotated = self.img
        self.y = y - self.img.get_height()
        self.x = track.get_x(self.y) - self.img.get_width() // 2
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
        if self.y - self.speed > self.track.y_min:
            self.y += self.y_change + self.gravity  # - self.img_rotated.get_height() // 2
            self.x = self.track.get_x(self.y) - self.img_rotated.get_width() // 2
        else:
            self.y += self.gravity

        if self.y <= 0:
            self.y = 0
        elif self.y > self.screen.get_height() - self.img.get_height():
            self.y = self.screen.get_height() - self.img.get_height()

        angle_delta = self.angle_deg - self.track.tangent_angle(self.x)
        angle_delta = int(angle_delta)
        if abs(angle_delta) > 1:
            self.angle_deg -= angle_delta
            self.rotate(-self.angle_deg - 70)

    def redraw(self, img):
        self.screen.blit(img, (self.x, self.y))

    def rotate(self, angle_deg):
        self.img_rotated = rotate(self.img, angle_deg)

    def update(self):
        self.redraw(self.img_rotated)
        self.move()
