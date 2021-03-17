from pygame import rect, draw


class VolumeBar:
    def __init__(self, screen, x, y, w=30, h=140, value=0):
        self.screen = screen
        self.w = w
        self.h = h
        self.volume_bar_x = x
        self.y = y - self.h
        self.rect = rect.Rect(x, self.y, self.w, self.h)
        self.value = value

    def update(self):
        draw.rect(self.screen, (240, 240, 240), self.rect, width=0, border_radius=2)

        value = self.value * self.h // 100
        value_rect = rect.Rect(self.volume_bar_x, self.y + self.h - value, self.w, value)
        draw.rect(self.screen, (100, 240, 240), value_rect, width=0, border_radius=2)

        draw.rect(self.screen, (170, 170, 170), self.rect, width=2, border_radius=2)


class ConnectionGroup(VolumeBar):
    def __init__(self, screen, img_active, img_inactive=None, x=0, y=0, w=30, h=140, align='Left', is_active=True):
        self.screen = screen
        self.img_active = img_active
        self.img_inactive = img_inactive
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.is_active = is_active

        top = self.y
        left = self.x + self.img_active.get_width() + 10

        self.align = align
        if align != 'Left':
            left = self.x - self.w - 10

        super().__init__(screen, left, top, w, h)

    def update(self):
        super(ConnectionGroup, self).update()
        if self.is_active:
            img = self.img_active
        else:
            img = self.img_inactive
            self.value = 0
        self.screen.blit(img, (self.x, self.y))
