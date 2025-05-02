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


print(generate_circle_path([0.0,0.0,1.3],0.8,15))