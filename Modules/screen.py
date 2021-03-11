from pygame.display import set_mode


# Create the screen
class Screen:
    resolution_list = ((800, 600), (1024, 768), (1280, 1024), (1440, 960), (1920, 1080))

    def __init__(self, resolution_id=0):
        self.width, self.height = self.resolution_list[resolution_id]
        self.screen = set_mode((self.width, self.height))
        # RGB = Red, Green, Blue
        self.screen.fill((0, 0, 0))
