export type ShapeName = 'Line' | 'Triangle' | 'Circle' | 'Square' | 'Heart' | 'Apple' | 'Moon'

export const groups: ShapeName[][] = [
  ['Triangle', 'Line', 'Circle', 'Square'], // Group 1
  ['Triangle', 'Apple', 'Heart', 'Moon'], // Group 2
]

export const shapesData: Record<ShapeName, { image: string; path: number[][] }> = {
  Line: {
    image: 'path/to/line_image.png',
    path: [
      [0, -1, 1.5],
      [0, 0, 1.5],
      [0, 1, 1.5],
    ],
  },
  Triangle: {
    image: 'path/to/triangle_image.png',
    path: [
      [0, -0.5, 1],
      [0, 0, 1.8],
      [0, 0.5, 1],
      [0, -0.5, 1],
    ],
  },
  Circle: {
    image: 'path/to/circle_image.png',
    path: [
      [0, 0, 2],
      [0, 0.71, 1.71],
      [0, 1, 1],
      [0, 0.71, 0.39],
      [0, 0, -1],
      [0, -0.71, -0.71],
      [0, -1, 0],
      [0, -0.71, 0.71],
      [0, 0, 1],
    ],
  },
  Square: {
    image: 'path/to/square_image.png',
    path: [
      [0, 0, 0],
      [0, 1, 0],
      [1, 1, 0],
      [1, 0, 0],
      [0, 0, 0],
    ],
  },
  Heart: {
    image: 'path/to/square_image.png',
    path: [
      [0, 0, 0.8],
      [0, -0.4, 1.2],
      [0, -0.6, 1.6],
      [0, -0.3, 1.8],
      [0, 0, 1.4],
      [0, -0.3, 1.8],
      [0, -0.6, 1.6],
      [0, -0.4, 1.2],
      [0, 0, 0.8],
    ],
  },
  Apple: {
    image: 'path/to/square_image.png',
    path: [
      [0, 0, 0],
      [0, 1, 0],
      [1, 1, 0],
      [1, 0, 0],
      [0, 0, 0],
    ],
  },
  Moon: {
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
