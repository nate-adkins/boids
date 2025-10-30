from pyglet import shapes
import math

def create_arrow(x, y, length, angle, color, batch):
    """
    Draws an arrow starting at (x, y), with given length and angle (in degrees).
    """
    angle_rad = math.radians(angle*-1 + 90)
    end_x = x + length * math.cos(angle_rad)
    end_y = y + length * math.sin(angle_rad)
    line = shapes.Line(x, y, end_x, end_y, thickness=2, color=color, batch=batch)
    arrow_size = 10
    left_x = end_x - arrow_size * math.cos(angle_rad - math.pi/6)
    left_y = end_y - arrow_size * math.sin(angle_rad - math.pi/6)
    
    right_x = end_x - arrow_size * math.cos(angle_rad + math.pi/6)
    right_y = end_y - arrow_size * math.sin(angle_rad + math.pi/6)
    
    arrow_head = shapes.Triangle(end_x, end_y, left_x, left_y, right_x, right_y, color=color, batch=batch)
    
    return line, arrow_head
