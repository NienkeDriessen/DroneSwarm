export type ShapeName = 'line' | 'triangle' | 'circle' | 'square' | 'heart' | 'apple' | 'moon'

export const groups: ShapeName[][] = [
  ['line', 'triangle', 'circle', 'square'], // Group 1
  ['heart', 'apple', 'circle', 'moon'], // Group 2
]

export const shapesData: Record<ShapeName, { image: string; path: number[][] }> = {
  line: {
    image: 'path/to/line_image.png',
    path: [
      [0, 0, 0],
      [1, 0, 0],
      [2, 0, 0],
    ],
  },
  triangle: {
    image: 'path/to/triangle_image.png',
    path: [
      [0, 0, 0],
      [1, 1, 0],
      [2, 0, 0],
      [0, 0, 0],
    ],
  },
  circle: {
    image: 'path/to/circle_image.png',
    path: [
      [0, 1, 0],
      [0.71, 0.71, 0],
      [1, 0, 0],
      [0.71, -0.71, 0],
      [0, -1, 0],
      [-0.71, -0.71, 0],
      [-1, 0, 0],
      [-0.71, 0.71, 0],
      [0, 1, 0],
    ],
  },
  square: {
    image: 'path/to/square_image.png',
    path: [
      [0, 0, 0],
      [0, 1, 0],
      [1, 1, 0],
      [1, 0, 0],
      [0, 0, 0],
    ],
  },
  heart: {
    image: 'path/to/square_image.png',
    path: [
      [0, 0, 0],
      [0, 1, 0],
      [1, 1, 0],
      [1, 0, 0],
      [0, 0, 0],
    ],
  },
  apple: {
    image: 'path/to/square_image.png',
    path: [
      [0, 0, 0],
      [0, 1, 0],
      [1, 1, 0],
      [1, 0, 0],
      [0, 0, 0],
    ],
  },
  moon: {
    image: 'path/to/square_image.png',
    path: [
      [0, 0, 0],
      [0, 1, 0],
      [1, 1, 0],
      [1, 0, 0],
      [0, 0, 0],
    ],
  },
}
