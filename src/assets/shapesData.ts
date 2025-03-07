export type ShapeName = 'Line' | 'Triangle' | 'Circle' | 'Square' | 'Heart' | 'Druppel' | 'Moon'

export const groups: ShapeName[][] = [
  ['Triangle', 'Line', 'Circle', 'Square'], // Group 1
  ['Triangle', 'Druppel', 'Heart', 'Moon'], // Group 2
]

const startPath = new URL('@/assets/charades_icons/', import.meta.url).href

//\charades_icons\Heart.svg
export const shapesData: Record<ShapeName, { image: string; path: number[][] }> = {
  Line: {
    image: startPath + '/Line.svg',
    path: [
      [0, 0, 1.25],
      [0, -1, 1.5],
      [0, 0, 1.5],
      [0, 1, 1.5],
      [0, 0, 1.25],
    ],
  },
  Triangle: {
    image: startPath + '/Triangle.svg',
    path: [
      [0, 0, 1.25],
      [0, -0.5, 1],
      [0, 0, 1.8],
      [0, 0.5, 1],
      [0, -0.5, 1],
      [0, 0, 1.25],
    ],
  },
  Circle: {
    image: startPath + '/Circle.svg',
    path: [
      [0, 0, 1.25],
      [0, 0, 2],
      [0, 0.71, 1.71],
      [0, 1, 1],
      [0, 0.71, 0.39],
      [0, 0, -1],
      [0, -0.71, -0.71],
      [0, -1, 0],
      [0, -0.71, 0.71],
      [0, 0, 1],
      [0, 0, 1.25],
    ],
  },
  Square: {
    image: startPath + '/Square.svg',
    path: [
      [0, 0, 1.25],
      [0, -0.85, 1.875],
      [0, -0.85, 0.625],
      [1, 0.85, 0.625],
      [1, 0.85, 1.875],
      [0, 0, 1.25],
    ],
  },
  Heart: {
    image: startPath + '/Heart.svg',
    path: [
      [0, 0, 1.25],
      [0, 0, 0.31],
      [0, -0.85, 0.94],
      [0, -1.275, 1.56],
      [0, -0.85, 1.875],
      [0, 0, 1.56],
      [0, 0.85, 1.875],
      [0, 1.275, 1.56],
      [0, 0.85, 0.94],
      [0, 0, 0.31],
      [0, 0, 1.25],
    ],
  },
  Druppel: {
    image: startPath + '/Druppel.svg',
    path: [
      [0, 0, 0.625],
      [0, -0.45, 0.31],
      [0, -0.85, 0.31],
      [0, -1.275, 0.94],
      [0, -1.275, 1.56],
      [0, -0.45, 1.875],
      [0, 0, 1.56],
      [0, 0.45, 1.875],
      [0, 1.275, 1.56],
      [0, 1.275, 0.94],
      [0, 0.85, 0.31],
      [0, 0.45, 0.31],
      [0, 0, 0.625],
    ],
  },
  Moon: {
    image: startPath + '/Moon.svg',
    path: [
      [0, 0, 1.25],
      [0, 0, 0.31],
      [0, -0.85, 0.625],
      [0, 0, 0.94],
      [0, 0.45, 1.25],
      [0, 0, 1.56],
      [0, -0.85, 1.875],
      [0, 0, 2.19],
      [0, 0.85, 1.875],
      [0, 1.275, 1.56],
      [0, 1.275, 0.94],
      [0, 0.85, 0.31],
      [0, 0, 0.31],
      [0, 0, 1.25],
    ],
  },
}
