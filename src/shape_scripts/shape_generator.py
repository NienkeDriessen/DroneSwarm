import math
from typing import List, Tuple, Dict

def generate_circle_path(
    centroid: Tuple[float, float, float], 
    radius: float, 
    num_points: int
) -> Dict[str, List[List[float]]]:
    cx, cy, cz = centroid
    path = []

    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        y = cy + radius * math.cos(angle)
        z = cz + radius * math.sin(angle)
        path.append([cx, y, z])

    return {"path": path}

def generate_heart_path(
    centroid: Tuple[float, float, float], 
    scale: float, 
    num_points: int
) -> Dict[str, List[List[float]]]:
    cx, cy, cz = centroid
    path = []

    for i in range(num_points):
        t = 2 * math.pi * i / num_points
        # Parametric equations for a heart shape (in 2D)
        y = 16 * math.sin(t)**3
        z = (13 * math.cos(t) 
             - 5 * math.cos(2*t) 
             - 2 * math.cos(3*t) 
             - math.cos(4*t))
        
        # Scale and shift
        y = cy + scale * y
        z = cz + scale * z
        path.append([cx, y, z])

    return {"path": path}

def generate_droplet_path_parametric(
    centroid: Tuple[float, float, float], 
    a: float, 
    b: float, 
    num_points: int
) -> Dict[str, List[List[float]]]:
    cx, cy, cz = centroid
    path = []

    for i in range(num_points):
        t = 2 * math.pi * i / num_points
        y = a * (1 - math.sin(t)) * math.cos(t)
        z = 2.3 + b * (math.sin(t) - 1)
        path.append([cx, cy + y, cz + z])

    return {"path": path}

def generate_moon_path(
    centroid: Tuple[float, float, float],
    outer_radius: float,
    inner_radius: float,
    offset: float,  # offset of the inner circle along Y-axis
    num_points: int
) -> Dict[str, List[List[float]]]:
    cx, cy, cz = centroid
    path = []

    # Full outer circle
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        y = cy + outer_radius * math.cos(angle)
        z = 1.2 + cz + outer_radius * math.sin(angle)
        path.append([cx, y, z])
    
    # Full inner circle in reverse
    for i in reversed(range(num_points)):
        angle = 2 * math.pi * i / num_points
        y = cy + offset + inner_radius * math.cos(angle)
        z = 1.2 + cz + inner_radius * math.sin(angle)
        path.append([cx, y, z])

    return {"path": path}

# print("Circle:" ,generate_circle_path([0.0,0.0,1.3],0.8,15))
#
# print("Heart:",generate_heart_path([0.0,0.0,1.3],0.07,15))

# print("Droplet:",generate_droplet_path_parametric((0, 0, 0), a=0.6, b=1,num_points=15))

print("Maan:",generate_moon_path((0, 0, 0), outer_radius=1.0, inner_radius=0.5, offset=1.2, num_points=25))