from pyglet import shapes
from math import sin, cos, atan2
import numpy as np
from numpy.typing import NDArray
import random

def angle_diff(a, b):
    return (a - b + np.pi) % (2 * np.pi) - np.pi

boid_type = np.dtype([
    ('theta',np.float32),
    ('x',np.float32),
    ('y',np.float32),
    ])

class Boids():
    def __init__(self, n: int, maxes: tuple[int], batch, speed_changes = False):
        self.speed_changes = speed_changes 
        self.count = n
        self.maxes = maxes
        self.boids_array = np.zeros(n,dtype=boid_type)
        self.randomize_states()
        self.shape_array: list[BoidShape] = []
        self.__create_shapes(batch)

    def __create_shapes(self, batch): 
        for boid_state in self.boids_array: 
            self.shape_array.append(BoidShape(boid_state['x'],boid_state['y'],boid_state['theta'],(0,255,255),batch))

    def __shape_update(self):
        for shape, boid_state in zip(self.shape_array, self.boids_array):
            shape.update_pos(boid_state['x'],boid_state['y'],boid_state['theta'])

    def update_state(self, d_thetas: NDArray[np.float32]):
        for i in range(self.count):
            self.boids_array[i]['theta'] += d_thetas[i]
            self.boids_array[i]['x'] += cos(self.boids_array[i]['theta'])
            self.boids_array[i]['y'] += sin(self.boids_array[i]['theta'])
            
            self.boids_array[i]['x'] %= self.maxes[0]
            self.boids_array[i]['y'] %= self.maxes[1]

            self.boids_array[i]['theta'] = (self.boids_array[i]['theta'] + np.pi) % (2 * np.pi) - np.pi
        self.__shape_update()


    def randomize_states(self):
        for i in range(self.count):
            new_theta = random.random() * 2 * np.pi
            new_x = random.randint(0,self.maxes[0])
            new_y = random.randint(0,self.maxes[1])
            self.boids_array[i] = np.array([(new_theta,new_x,new_y,)],dtype=boid_type)

    def calc_centroid(self) -> tuple[np.floating]:
        return (np.mean(self.boids_array['x']),np.mean(self.boids_array['y']))
    
    def calc_avg_head(self):
        mean_x = np.mean(np.cos(self.boids_array['theta']))
        mean_y = np.mean(np.sin(self.boids_array['theta']))
        return atan2(mean_y, mean_x)




class BoidShape():

    def __init__(self, x, y, theta, color, batch):
        '''
        strickly for animating the movement of the boids. all movement math and state update logic should happen in the Boids class 
        '''
        self.length = 15
        self._circle = shapes.Circle(x, y, radius=5, segments=20, color=color, batch=batch)
        x2 = x + self.length * cos(theta)
        y2 = y + self.length * sin(theta)
        self._line = shapes.Line(x, y, x2, y2, 3, color=color, batch=batch)

    def update_pos(self, x, y, theta):
        self._circle.x = x
        self._circle.y = y

        self._line.x = self._circle.x
        self._line.y = self._circle.y
        self._line.x2 = self._circle.x + self.length * cos(theta)
        self._line.y2 = self._circle.y + self.length * sin(theta)

    def delete(self):
        self._line.delete()
        self._circle.delete()

