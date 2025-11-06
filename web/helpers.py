import math, random, heapq

def distance(a,b): return math.sqrt((a['x']-b['x'])**2+(a['y']-b['y'])**2)

def calc_centroid(agents): return sum([a["x"] for a in agents])/len(agents), sum([a["y"] for a in agents])/len(agents)

def calc_avg_heading(agents): return math.atan2(sum(math.sin(a['theta']) for a in agents), sum(math.cos(a['theta']) for a in agents))

def generate_random_states(count):
    return [{"x": random.random(), 
             "y": random.random(), 
             "theta": random.random()*2*math.pi} 
             for _ in range(count)]

def angle_diff(a, b): return (a - b + math.pi) % (2 * math.pi) - math.pi # wrap around diffs to +-pi

def k_nearest_neighbors(swarm, agent_index, k=5):
    curr_boid = swarm[agent_index]
    distances = []
    for i, boid in enumerate(swarm):
        if i == agent_index: continue
        dist = distance(curr_boid, boid)
        distances.append((dist, i))

    return heapq.nsmallest(k, distances, key=lambda x: x[0])

def seperation(neighbors, agent):
    fx, fy = 0.0, 0.0
    for neighbor in neighbors:
        dist = distance(neighbor,agent)
        if dist == 0: continue
        fx += (agent["x"] - neighbor["x"]) / (dist**2)
        fy += (agent["y"] - neighbor["y"]) / (dist**2)
    if fx == 0 and fy == 0: return 0.0
    
    repulsion_angle = math.atan2(fy, fx)
    return angle_diff(repulsion_angle, agent["theta"])

def cohesion(centroid, a):
    angle_to_centroid = math.atan2((centroid[1] - a["y"]),(centroid[0] - a["x"]))
    return angle_diff(angle_to_centroid, a['theta'])

def alignment(avg_heading, a): return angle_diff(avg_heading, a['theta'])