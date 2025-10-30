from pyglet import shapes
from math import sin, cos, atan2

class BoidShape():
    def __init__(self, x, y, theta, color, batch):
        self.length = 15
        self._circle = shapes.Circle(x, y, radius=5, segments=20, color=color, batch=batch)
        x2 = x + self.length * cos(theta)
        y2 = y + self.length * sin(theta)
        self._line = shapes.Line(x, y, x2, y2, 3, color=color, batch=batch)

    def update_pos(self, dx, dy):
        self._circle.x += dx
        self._circle.y += dy

        new_theta = atan2(dy,dx)

        self._line.x = self._circle.x
        self._line.y = self._circle.y
        self._line.x2 = self._circle.x + self.length * cos(new_theta)
        self._line.y2 = self._circle.y + self.length * sin(new_theta)

