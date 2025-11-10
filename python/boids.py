import numpy as np
from scipy.spatial import cKDTree
import time 

def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f'Function {func.__name__} took {end_time - start_time:.4f} seconds')
        return result
    return wrapper

def angle_diff(a, b):
    return (a - b + np.pi) % (2 * np.pi) - np.pi  # wrap to +-pi

class BoidSwarm:
    def __init__(self, count, k, speed, separation_gain, alignment_gain, cohesion_gain):
        self.count = count
        self.k = k
        self.S = separation_gain
        self.A = alignment_gain
        self.C = cohesion_gain
        self.speed = speed

        self.d_thetas = np.empty(self.count, dtype=np.float32)
        self.boids = np.empty(count, dtype=[
            ('theta', np.float32),
            ('x', np.float32),
            ('y', np.float32),
        ])
        self.randomize_states()

    def randomize_states(self):
        rng = np.random.default_rng()
        self.boids['theta'] = rng.uniform(0, 2 * np.pi, self.count)
        self.boids['x'] = rng.uniform(0,1, self.count)
        self.boids['y'] = rng.uniform(0,1, self.count)
    
    # @timeit
    def update(self):
        positions = np.column_stack((self.boids['x'], self.boids['y']))
        tree = cKDTree(positions)
        dists, neighbors = tree.query(positions, k=self.k + 1)
        neighbors = neighbors[:, 1:]

        x_neighbors = self.boids['x'][neighbors]
        y_neighbors = self.boids['y'][neighbors]
        theta_neighbors = self.boids['theta'][neighbors]

        # Seperation
        dx = self.boids['x'][:, None] - x_neighbors
        dy = self.boids['y'][:, None] - y_neighbors
        dist2 = dx**2 + dy**2
        mask = dist2 > 1e-8 
        sep_dx = np.sum(np.where(mask, dx / dist2, 0), axis=1)
        sep_dy = np.sum(np.where(mask, dy / dist2, 0), axis=1)
        sep_theta = np.arctan2(sep_dy, sep_dx)
        d_theta_sep = angle_diff(sep_theta, self.boids['theta']) * self.S

        # Alignment
        avg_heading = np.arctan2(np.mean(np.sin(theta_neighbors), axis=1),np.mean(np.cos(theta_neighbors), axis=1))
        d_theta_align = angle_diff(avg_heading, self.boids['theta']) * self.A

        # Cohesion
        centroid_x = np.mean(x_neighbors, axis=1)
        centroid_y = np.mean(y_neighbors, axis=1)
        angle_to_centroid = np.arctan2(centroid_y - self.boids['y'],centroid_x - self.boids['x'])
        d_theta_coh = angle_diff(angle_to_centroid, self.boids['theta']) * self.C

        self.d_thetas[:] = d_theta_sep + d_theta_align + d_theta_coh
        self.boids['theta'] += self.d_thetas % (np.pi*2)
        self.boids['x'] = (self.boids['x'] + np.cos(self.boids['theta']) * self.speed)%1
        self.boids['y'] = (self.boids['y'] + np.sin(self.boids['theta']) * self.speed)%1