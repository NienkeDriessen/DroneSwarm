export type ShapeName = 'Lijn' | 'Driehoek' | 'Cirkel' | 'Vierkant' | 'Hart' | 'Druppel' | 'Maan'

export const groups: ShapeName[][] = [
  ['Driehoek', 'Lijn', 'Cirkel', 'Vierkant'], // Group 1
  ['Driehoek', 'Druppel', 'Hart', 'Maan'], // Group 2
]

const startPath = new URL('@/assets/charades_icons/', import.meta.url).href

//\charades_icons\Hart.svg
export const shapesData: Record<ShapeName, { image: string; path: number[][] }> = {
  Lijn: {
    image: startPath + '/Lijn.svg',
    path: [
      [0, 0, 1.25],
      [0, -1, 1.5],
      [0, 0, 1.5],
      [0, 1, 1.5],
      [0, 0, 1.25],
    ],
  },
  Driehoek: {
    image: startPath + '/Driehoek.svg',
    path: [
      [0, 0, 1.25],
      [0, -0.5, 1],
      [0, 0, 1.8],
      [0, 0.5, 1],
      [0, -0.5, 1],
      [0, 0, 1.25],
    ],
  },
  Cirkel: {
    image: startPath + '/Cirkel.svg',
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
  Vierkant: {
    image: startPath + '/Vierkant.svg',
    path: [
      [0, 0, 1.25],
      [0, -0.85, 1.875],
      [0, -0.85, 0.625],
      [1, 0.85, 0.625],
      [1, 0.85, 1.875],
      [0, 0, 1.25],
    ],
  },
  Hart: {
    image: startPath + '/Hart.svg',
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
  Maan: {
    image: startPath + '/Maan.svg',
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
