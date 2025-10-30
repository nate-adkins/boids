from pyglet import shapes
from math import sin, cos

class BoidShape():
    def __init__(self, x, y, theta, batch):
        self.length = 15
        self._circle = shapes.Circle(x, y, radius=5, segments=20, color=(64,128,128), batch=batch)
        x2 = x + self.length * cos(theta)
        y2 = y + self.length * sin(theta)
        self._line = shapes.Line(x, y, x2, y2, 3, color=(64,128,128), batch=batch)

    def update_pos(self, dx, dy, new_theta):
        self._circle.x += dx
        self._circle.y += dy

        x = self._circle.x
        y = self._circle.y
        
        self._line.x = x
        self._line.y = y
        self._line.x2 = x + self.length * cos(new_theta)
        self._line.y2 = y + self.length * sin(new_theta)

