# """
# Cohesion - go to centroid
# Seperation - avoid neighbors
# Alignment - go with direction of group
# """


# import numpy as np
# import pyglet, random
# from pyglet import window, shapes
# BOIDS = 3
# SIZE = 200

# boid_type = np.dtype([('theta',np.float32),('x',np.float32),('y',np.float32)])

# win = window.Window()
# win.size = SIZE,SIZE
# pyglet.gl.glClearColor(1,1,1,1)
# win.set_caption("Boids")

# batch = pyglet.graphics.Batch()
# line = shapes.Line(100,100,180,180,2,(0,0,0), batch=batch)
# print(line.rotation)
# line.rotation += 0 

# def update(hz):
#     deg_per_sec = 360
#     line.rotation += deg_per_sec * hz




# @win.event
# def on_draw():
#     win.clear()
#     batch.draw()

# pyglet.clock.schedule_interval(update, 1/60.0)

# pyglet.app.run()

import numpy as np 

hi = np.zeros(10,np.float32)

print(len(hi))