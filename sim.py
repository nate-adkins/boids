"""
Cohesion - go to centroid
Seperation - avoid neighbors
Alignment - go with direction of group
"""

from helpers import BoidShape
import numpy as np
import pyglet, random
from pyglet import window, shapes
from math import atan2, cos, sin, degrees
BOIDS = 1000
SIZE = 1000

boid_type = np.dtype([('theta',np.float32),('x',np.float32),('y',np.float32)])

win = window.Window()
win.size = SIZE,SIZE
pyglet.gl.glClearColor(1,1,1,1)
win.set_caption("Boids") 

batch = pyglet.graphics.Batch()

boids_array = np.empty(0,dtype=boid_type)
shape_array: list[BoidShape] = []

def calculate_centroid():
    return (np.mean(boids_array['x']),np.mean(boids_array['y']))


for n in range(BOIDS):
    new_theta = random.random()*360
    new_x = random.randint(0,SIZE)
    new_y = random.randint(0,SIZE)
    new_boid = np.array([(new_theta,new_x,new_y)],dtype=boid_type)
    boids_array = np.concatenate([boids_array,new_boid])
    
    shape_array.append(BoidShape(new_x,new_y,new_theta,batch))

centroid = calculate_centroid()
centroid_shape = shapes.Circle(centroid[0],centroid[1],radius=10,segments=20, color=(255,0,0), batch=batch)

def update(hz):

    # update numpy arrays using boids rules xt+1 = Bboids(xt)
    # update visuals 
    centroid = calculate_centroid()
    centroid_shape.x = centroid[0]
    centroid_shape.y = centroid[1]

    rand_strength = 0
    cohesion_strength = 2
    for i, boid in enumerate(boids_array):

        rand_dx = random.gauss() * rand_strength
        rand_dy = random.gauss() * rand_strength

        angle_to_centroid = atan2((centroid[1] - boid['y']),(centroid[0] - boid['x']))
        cohesion_dx = cos(angle_to_centroid) * cohesion_strength
        cohesion_dy = sin(angle_to_centroid) * cohesion_strength

        dx = rand_dx + cohesion_dx
        dy = rand_dy + cohesion_dy
        new_theta = atan2(dy,dx)

        boid['x'] += dx
        boid['y'] += dy
        boid['theta'] = new_theta

        shape_array[i].update_pos(dx,dy,new_theta)

@win.event
def on_draw():
    win.clear()
    batch.draw()

pyglet.clock.schedule_interval(update, 1/10.0)

pyglet.app.run()