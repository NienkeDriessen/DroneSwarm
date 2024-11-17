<template>
  <div class="path-drawing">
    <button @click="goBack" class="back-button">Back</button>
    <h1>Create Your Path</h1>
    <p>Click on the grid squares to draw the path</p>

    <!-- Grid container with overlay for lines -->
    <div
      class="grid-container"
      :style="{
        gridTemplateColumns: `repeat(${cols}, ${cellSize}px)`,
        gridTemplateRows: `repeat(${rows}, ${cellSize}px)`,
        width: `${gridWidth}px`,
        height: `${gridHeight}px`,
      }"
    >
      <!-- Lines -->
      <svg class="line-overlay" :width="gridWidth" :height="gridHeight">
        <line
          v-for="(segment, index) in lineSegments"
          :key="index"
          :x1="segment.start.x * (cellSize + gap) + cellSize / 2"
          :y1="segment.start.y * (cellSize + gap) + cellSize / 2"
          :x2="segment.end.x * (cellSize + gap) + cellSize / 2"
          :y2="segment.end.y * (cellSize + gap) + cellSize / 2"
          :stroke="segment.intersecting ? 'red' : '#43b7ff'"
          stroke-width="10"
        />
      </svg>
      <!-- Grid cells -->
      <div
        v-for="(cell, index) in grid"
        :key="index"
        :class="['grid-cell', cell.active ? 'active' : '']"
        @click="toggleCell(index)"
        :style="{ width: `${cellSize}px`, height: `${cellSize}px` }"
      ></div>
    </div>

    <!-- Control buttons -->
    <div class="button-container">
      <button @click="undo" class="control-button">Undo</button>
      <button @click="resetPath" class="control-button">Reset</button>
      <button @click="completePath" class="control-button">Done</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

// Define the grid size
const rows = 8
const cols = 15
const maxGridWidth = 700
const maxGridHeight = 500
const gap = 2 // Gap size between cells

const stepsPerSegment = 10; // Number of intermediate points between each pair of points


// Calculate cell size based on the max dimensions and number of cells including gaps
const cellSize = Math.min(
  (maxGridWidth - gap * (cols - 1)) / cols,
  (maxGridHeight - gap * (rows - 1)) / rows,
)
const gridWidth = cellSize * cols + gap * (cols - 1)
const gridHeight = cellSize * rows + gap * (rows - 1)

// Coordinate
interface Coordinate {
  x: number
  y: number
}

// Initialize the grid array with inactive cells
const grid = ref(Array(rows * cols).fill({ active: false }))

// Track the selected path coordinates
const pathCoordinates = ref<Coordinate[]>([])

// Create array for the waypoint generator itself
const waypoints= ref<Coordinate[]>([])

const lineSegments = computed(() => {
  const segments = pathCoordinates.value.slice(1).map((end, index) => ({
    start: pathCoordinates.value[index],
    end: end,
    intersecting: false, // Default to false
  }));

  // Check each segment for intersections with every other segment
  segments.forEach((segment, i) => {
    for (let j = 0; j < i; j++) {
      if (
        doLinesIntersect(
          segment.start,
          segment.end,
          segments[j].start,
          segments[j].end
        )
      ) {
        segment.intersecting = true;
        segments[j].intersecting = true;
      }
    }
  });

  return segments;
});


// Handle cell clicks to activate a path
const toggleCell = (index: number) => {
  if (pathCoordinates.value.length === 0 || !grid.value[index].active) {
    grid.value[index] = { active: true }
    pathCoordinates.value.push({
      x: index % cols, // Calculate x from  the col count
      y: Math.floor(index / cols), // Calculate y based on the col count
    })
  }
}

// Undo the last cell in the path
const undo = () => {
  if (pathCoordinates.value.length > 0) {
    const lastPoint = pathCoordinates.value.pop()
    if (lastPoint) {
      const lastIndex = lastPoint.y * cols + lastPoint.x
      grid.value[lastIndex] = { active: false }
    }
  }
}

// Reset the path and grid
const resetPath = () => {
  pathCoordinates.value = []
  grid.value = Array(rows * cols).fill({ active: false })
}

// Interpolation to generate intermediate points between 2 points (like np.linspace)
const generateIntermediatePoints = (start: Coordinate, end: Coordinate, steps: number): Coordinate[] => {
  const points: Coordinate[] = [];
  for (let i = 1; i < steps; i++) {
    points.push({
      x: start.x + ((end.x - start.x) * i) / steps,
      y: start.y + ((end.y - start.y) * i) / steps,
    });
  }
  return points;
};


// Check if the points in PathCoordinates intersect at any point
const doLinesIntersect = (a1: Coordinate, a2: Coordinate, b1: Coordinate, b2: Coordinate): boolean => {
  
  // 2d cross prod
  const cross = (v1: Coordinate, v2: Coordinate) => v1.x * v2.y - v1.y * v2.x;

  // Just element-wise operator for ease
  const subtract = (v1: Coordinate, v2: Coordinate) => ({
    x: v1.x - v2.x,
    y: v1.y - v2.y,
  });

  const d1 = subtract(a2, a1);
  const d2 = subtract(b2, b1);
  const delta = subtract(b1, a1);

  const cross1 = cross(delta, d1);
  const cross2 = cross(delta, d2);
  const denominator = cross(d1, d2);

  if (denominator === 0) {
    return false; // Lines are parallel
  }

  const t = cross2 / denominator;
  const u = cross1 / denominator;

  return t > 0 && t < 1 && u > 0 && u < 1; // Check if lines intersect within segment bounds
};


const completePath = () => {
  const hasIntersections = lineSegments.value.some(
    (segment) => segment.intersecting
  );

  // Handle intersection by asking user to undo or start from scratch
  if (hasIntersections) {
    alert('Path contains intersecting lines. Please fix them before proceeding.');
    return;
  }

  // Generate waypoints if no intersections
  waypoints.value = [];
  for (let i = 0; i < pathCoordinates.value.length - 1; i++) {
    const start = pathCoordinates.value[i];
    const end = pathCoordinates.value[i + 1];

    // Add the starting point
    waypoints.value.push(start);

    // Add intermediate points
    waypoints.value.push(...generateIntermediatePoints(start, end, stepsPerSegment));
  }

  // Add the last point
  if (pathCoordinates.value.length > 0) {
    waypoints.value.push(pathCoordinates.value[pathCoordinates.value.length - 1]);
  }

  console.log('Path completed with coordinates:', pathCoordinates.value);
  console.log('Path waypoints including intermediate points:', waypoints.value);
  alert('Path and waypoints are ready!');
};


// Go back function to navigate to the previous page
const router = useRouter()
const goBack = () => {
  router.back()
}
</script>

<style scoped>
.path-drawing {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.grid-container {
  position: relative;
  display: grid;
  grid-template-columns: repeat(30, 20px);
  grid-template-rows: repeat(20, 20px);
  gap: 2px;
  margin: 1rem 0;
}

.grid-cell {
  width: 20px;
  height: 20px;
  background-color: #e0e0e0;
  cursor: pointer;
  transition: background-color 0.3s;
}

.grid-cell.active {
  background-color: #43b7ff; /* Active cell color */
}

/* Overlay for lines */
.line-overlay {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none; /* Prevent SVG overlay from blocking clicks */
}

.button-container {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.control-button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.back-button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
  background-color: #ffffff;
  color: rgb(0, 0, 0);
  border: 2px solid black;
  border-radius: 4px;
  transition: background-color 0.3s;
  align-self: flex-start;
}
</style>
