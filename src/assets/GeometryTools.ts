export interface Coordinate {
    x: number
    y: number
  }
  
  // Interpolation to generate intermediate points between two points
  export const generateIntermediatePoints = (
    start: Coordinate,
    end: Coordinate,
    steps: number,
  ): Coordinate[] => {
    const points: Coordinate[] = []
    for (let i = 1; i < steps; i++) {
      points.push({
        x: start.x + ((end.x - start.x) * i) / steps,
        y: start.y + ((end.y - start.y) * i) / steps,
      })
    }
    return points
  }
  
  // Check if two line segments intersect
  export const doLinesIntersect = (
    a1: Coordinate,
    a2: Coordinate,
    b1: Coordinate,
    b2: Coordinate,
  ): boolean => {
    const cross = (v1: Coordinate, v2: Coordinate) => v1.x * v2.y - v1.y * v2.x
    const subtract = (v1: Coordinate, v2: Coordinate) => ({
      x: v1.x - v2.x,
      y: v1.y - v2.y,
    })
  
    const d1 = subtract(a2, a1)
    const d2 = subtract(b2, b1)
    const delta = subtract(b1, a1)
  
    const cross1 = cross(delta, d1)
    const cross2 = cross(delta, d2)
    const denominator = cross(d1, d2)
  
    if (denominator === 0) {
      return false // Lines are parallel
    }
  
    const t = cross2 / denominator
    const u = cross1 / denominator
  
    return t > 0 && t < 1 && u > 0 && u < 1
  }


  