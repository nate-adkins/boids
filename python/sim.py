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
BOIDS = 40
SIZE = 1000


win = window.Window()
win.set_size(SIZE, SIZE)
pyglet.gl.glClearColor(1,1,1,1)
win.set_caption("Boids") 

batch = pyglet.graphics.Batch()

boids_swarm = Boids(BOIDS,(SIZE,SIZE),batch)

centroid_shape = shapes.Circle(SIZE//2,SIZE//2,10,10,(0,0,0,32),batch=batch)

ATTRACTOR = (200,200)
ATTRACTOR2 = [SIZE - i for i in ATTRACTOR]
attractor = shapes.Circle(ATTRACTOR[0],ATTRACTOR[1],10,10,(0,255,0),batch=batch)
attractor2 = shapes.Circle(ATTRACTOR2[0],ATTRACTOR2[1],10,10,(0,255,0),batch=batch)

def update(hz):

    centroid = boids_swarm.calc_centroid()
    avg_heading = boids_swarm.calc_avg_head()
 
    centroid_shape.x = centroid[0]
    centroid_shape.y = centroid[1]

    cohesion_strength = 0.2
    alignment_strength = 0.1
    attractor_strength = 0.1
    attractor_strength2 = 0.2

    d_thetas = np.zeros(BOIDS,dtype=np.float32)
    for i, boid in enumerate(boids_swarm.boids_array):

        # attractor
        angle_to_attractor = atan2((attractor.y - boid['y']),(attractor.x - boid['x']))
        attractor_dtheta = angle_diff(angle_to_attractor, boid['theta']) * attractor_strength

        angle_to_attractor2 = atan2((attractor2.y - boid['y']),(attractor2.x - boid['x']))
        attractor_dtheta2 = angle_diff(angle_to_attractor2, boid['theta']) * attractor_strength2

        # cohesion
        angle_to_centroid = atan2((centroid[1] - boid['y']),(centroid[0] - boid['x']))
        cohesion_dtheta = angle_diff(angle_to_centroid, boid['theta']) * cohesion_strength

        # alignment 
        alignment_dtheta = angle_diff(avg_heading, boid['theta']) * alignment_strength

        d_theta = cohesion_dtheta + alignment_dtheta + attractor_dtheta + attractor_dtheta2

        d_theta = min(d_theta,pi/8)
        if abs(d_theta) < 0.05: d_theta = 0

        d_thetas[i] = d_theta

    boids_swarm.update_state(d_thetas)

@win.event
def on_draw():
    win.clear()
    batch.draw()

pyglet.clock.schedule_interval(update, 1/60.0)

pyglet.app.run()