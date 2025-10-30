"""
Cohesion - go to centroid
Seperation - avoid neighbors
Alignment - go with direction of group
"""


import numpy as np
import pyglet, random
from pyglet import window, shapes
from math import atan2, cos, sin, degrees
BOIDS = 3
SIZE = 500

boid_type = np.dtype([('theta',np.float32),('x',np.float32),('y',np.float32)])

win = window.Window()
win.size = SIZE,SIZE
pyglet.gl.glClearColor(1,1,1,1)
win.set_caption("Boids") 

batch = pyglet.graphics.Batch()

boids_array = np.empty(0,dtype=boid_type)
shape_array: list[shapes.Circle] = []

def calculate_centroid():
    return (np.mean(boids_array['x']),np.mean(boids_array['y']))


for n in range(BOIDS):
    new_theta = random.random()*360
    new_x = random.randint(0,SIZE)
    new_y = random.randint(0,SIZE)
    new_boid = np.array([(new_theta,new_x,new_y)],dtype=boid_type)
    boids_array = np.concatenate([boids_array,new_boid])
    
    shape_array.append(shapes.Circle(new_x,new_y,radius=5,segments=20, color=(64,128,128), batch=batch))

centroid = calculate_centroid()
centroid_shape = shapes.Circle(centroid[0],centroid[1],radius=10,segments=20, color=(255,0,0), batch=batch)

def update(hz):

    # update numpy arrays using boids rules xt+1 = Bboids(xt)
    # update visuals 
    centroid = calculate_centroid()
    centroid_shape.x = centroid[0]
    centroid_shape.y = centroid[1]

    rand_strength = 10
    cohesion_strength = 2
    for i, boid in enumerate(boids_array):

        rand_dx = (random.random() * rand_strength * 2) - rand_strength
        rand_dy = (random.random() * rand_strength * 2) - rand_strength

        angle_to_centroid = atan2((centroid[1] - boid['y']),(centroid[0] - boid['x']))
        cohesion_dx = cos(angle_to_centroid) * cohesion_strength
        cohesion_dy = sin(angle_to_centroid) * cohesion_strength

        dx = rand_dx + cohesion_dx
        dy = rand_dy + cohesion_dy
        new_heading = atan2(dy,dx)

        boid['x'] += dx
        boid['y'] += dy
        boid['theta'] = new_heading
        print(degrees(new_heading))

        shape_array[i].x += dx
        shape_array[i].y += dy

@win.event
def on_draw():
    win.clear()
    batch.draw()

pyglet.clock.schedule_interval(update, 1/60.0)

pyglet.app.run()