from pygame import mixer, image


class Bullet:
    def __init__(self, screen):
        """
        Ready - You can't see the bullet on the screen
        Fire - The bullet is currently moving
        """
        self.screen = screen
        self.sound = mixer.Sound("Media/Sounds/laser.wav")
        self.img = image.load('Media/Images/bullet.png')
        self.x = 0
        self.y = 480
        self.x_change = 0
        self.y_change = 10
        self.state = "ready"

    def fire_bullet(self, x, y):
        self.state = "fire"
        self.screen.blit(self.img, (x + 16, y + 10))

    # def move(self):
    #     # Bullet Movement
    #     if bulletY <= 0:
    #         bulletY = 480
    #         self.state = "ready"
    #
    #     if self.state == "fire":
    #         fire_bullet(bulletX, bulletY)
    #         bulletY -= self.y_change
    #
    # if bullet_state == "ready":
    #     bulletSound.play()
    #     # Get the current x coordinate of the spaceship
    #     bulletX = player1.x
    #     fire_bullet(bulletX, bulletY)
