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

def calc_centroid():
    return (np.mean(boids_array['x']),np.mean(boids_array['y']))

def calc_avg_head():
    return np.mean(boids_array['theta'])

for n in range(BOIDS):
    new_theta = random.random()*360
    new_x = random.randint(0,SIZE)
    new_y = random.randint(0,SIZE)
    new_boid = np.array([(new_theta,new_x,new_y)],dtype=boid_type)
    boids_array = np.concatenate([boids_array,new_boid])
    
    shape_array.append(BoidShape(new_x,new_y,new_theta,(64,128,128),batch))

centroid = calc_centroid()
centroid_boid = BoidShape(centroid[0],centroid[1],0,(255,0,0),batch)

def update(hz):

    centroid = calc_centroid()
    avg_heading = calc_avg_head()

    centroid_boid.update_pos(centroid[0],centroid[1])
    rand_strength = 0
    cohesion_strength = 2
    alginment_strength = 4

    for i, boid in enumerate(boids_array):

        if rand_strength != 0: 
            rand_dx, rand_dy = (random.gauss(0,1), random.gauss(0,1)) * rand_strength
        else: # skip gaussian sampling
            rand_dx, rand_dy = 0,0

        # cohesion
        angle_to_centroid = atan2((centroid[1] - boid['y']),(centroid[0] - boid['x']))
        cohesion_dx = cos(angle_to_centroid) * cohesion_strength
        cohesion_dy = sin(angle_to_centroid) * cohesion_strength

        # alignment 
        alignment_dx = cos(avg_heading) * alginment_strength
        alignment_dy = sin(avg_heading) * alginment_strength

        dx = rand_dx + cohesion_dx + alignment_dx
        dy = rand_dy + cohesion_dy + alignment_dy

        boid['x'] += dx
        boid['y'] += dy
        boid['theta'] = atan2(dy,dx)

        shape_array[i].update_pos(dx,dy)

@win.event
def on_draw():
    win.clear()
    batch.draw()

pyglet.clock.schedule_interval(update, 1/60.0)

pyglet.app.run()