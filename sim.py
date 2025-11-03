"""
Cohesion - go to centroid
Seperation - avoid neighbors
Alignment - go with direction of group
"""

from helpers import Boids, angle_diff
import numpy as np
import pyglet
from pyglet import window, shapes
from math import atan2, pi
import random
BOIDS = 40
SIZE = 1000


win = window.Window()
win.set_size(SIZE, SIZE)
pyglet.gl.glClearColor(1,1,1,1)
win.set_caption("Boids") 

batch = pyglet.graphics.Batch()

boids_swarm = Boids(BOIDS,(SIZE,SIZE),batch)

centroid_shape = shapes.Circle(SIZE//2,SIZE//2,10,10,(255,0,0),batch=batch)

def update(hz):

    centroid = boids_swarm.calc_centroid()
    avg_heading = boids_swarm.calc_avg_head()

    centroid_shape.x = centroid[0]
    centroid_shape.y = centroid[1]

    cohesion_strength = 0.01
    alignment_strength = 0.02

    d_thetas = np.zeros(BOIDS,dtype=np.float32)
    for i, boid in enumerate(boids_swarm.boids_array):

        # cohesion
        angle_to_centroid = atan2((centroid[1] - boid['y']),(centroid[0] - boid['x']))
        cohesion_dtheta = angle_diff(angle_to_centroid, boid['theta']) * cohesion_strength

        # alignment 
        alignment_dtheta = angle_diff(avg_heading, boid['theta']) * alignment_strength

        d_theta = cohesion_dtheta + alignment_dtheta

        d_theta = min(d_theta,pi/8)
        d_thetas[i] = d_theta

    boids_swarm.update_state(d_thetas)

@win.event
def on_draw():
    win.clear()
    batch.draw()

pyglet.clock.schedule_interval(update, 1/60.0)

pyglet.app.run()