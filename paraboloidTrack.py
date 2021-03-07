from numpy import arctan, degrees


class Track:
    """
    side: 'left' or 'right'
    Formula movement: y = a(x-b)^2 + c
    """
    def __init__(self, side, x1, y1, x2, y2):
        self.b = x1  # targetX
        self.c = y1  # targetY
        self.a = (y2 - self.c) / ((x2 - self.b) ** 2)
        self.y_min = y1
        self.y_max = y2
        if side == 'left':
            self.get_x = self.__get_x1
            self.tangent_angle = self.__tangent_angle1
        elif side == 'right':
            self.get_x = self.__get_x2
            self.tangent_angle = self.__tangent_angle2

    def __get_x1(self, y):
        return self.b - ((y - self.c) / self.a) ** 0.5  # paraboloid movement

    def __get_x2(self, y):
        return ((y - self.c) / self.a) ** 0.5 + self.b  # paraboloid movement

    def __tangent_angle1(self, x):
        angle_rad = arctan(2 * self.a * (x - self.b))  # tan(angle) = y' = (a(x-b)^2)' = 2a(x-b)
        return degrees(angle_rad)

    def __tangent_angle2(self, x):
        angle_rad = arctan(2 * self.a * (x - self.b))  # tan(angle) = y' = (a(x-b)^2)' = 2a(x-b)
        return degrees(angle_rad) - 135
