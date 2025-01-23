<template>
  <div class="path-drawing">
    <div class="control-row">
      <button @click="goBack" class="back-button">Back</button>
      <div class="title-col">
        <h1 class="title">Create Your Path</h1>
        <p class="sub-title">Click on the grid squares to draw the path</p>
      </div>
      <div class="mode-toggle">
        <button
          id="path-mode-button"
          :class="['mode-button', currentMode === Mode.PATH ? 'active' : '']"
          @click="setMode(Mode.PATH)"
        >
          Draw a path!
        </button>
        <button
          id="points-mode-button"
          :class="['mode-button', currentMode === Mode.POINTS ? 'active' : '']"
          @click="setMode(Mode.POINTS)"
        >
          Shape the drones!
        </button>
      </div>
    </div>
    <!-- Grid container with overlay for lines -->
    <div
      class="grid-container"
      @mousedown="startDrag"
      @mouseup="endDrag"
      @mouseleave="endDrag"
      @mousemove="handleDrag"
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
          :stroke="segment.intersecting ? '#DB1F22' : '#ff99ff'"
          stroke-width="8"
        />
      </svg>
      <!-- Grid cells -->
      <div
        v-for="(cell, index) in grid"
        :key="index"
        :class="['grid-cell', cell.active ? 'active' : '']"
        :data-drone-id="currentMode === Mode.POINTS ? getDroneId(index) : ''"
        @click="toggleCell(index)"
        :style="{ width: `${cellSize}px`, height: `${cellSize}px` }"
      ></div>
    </div>
    <div v-if="notificationMessage" class="notification">
      {{ notificationMessage }}
    </div>
    <!-- Control buttons -->
    <div class="control-row">
      <div class="button-container">
        <button id="undo-button" @click="undo" class="control-button">Undo</button>
        <button id="reset-button" @click="resetPath" class="control-button">Reset</button>
        <button id="complete-button" @click="completePath" class="control-button">Done</button>
      </div>
    </div>

    <!-- Drone Status Overview -->
    <DroneStatus v-if="currentMode === Mode.POINTS" :drones="drones" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'

import {
  doLinesIntersect,
  generateIntermediatePoints,
  type Coordinate,
} from '../assets/GeometryTools'

import DroneStatus from '../components/DroneStatus.vue'
import Drone from '../models/Drone'

enum Mode {
  PATH = 'path',
  POINTS = 'points',
}

const drones = ref<Drone[]>([
  new Drone(1, true),
  new Drone(2, true),
  new Drone(3, true),
  new Drone(4, true),
  new Drone(5, false),
  new Drone(6, false),
  new Drone(7, false),
  new Drone(8, false),
])

// Helper to count available drones
const availableDronesCount = computed(() => drones.value.filter((drone) => drone.available).length)

// Define the grid size
const rows = 8
const cols = 15
const maxGridWidth = 700
const maxGridHeight = 500
const gap = 1 // Gap size between cells

const maxStepSize = 0.5 // the max length one step can have

// Calculate cell size based on the max dimensions and number of cells including gaps
const cellSize = Math.min(
  (maxGridWidth - gap * (cols - 1)) / cols,
  (maxGridHeight - gap * (rows - 1)) / rows,
)
const gridWidth = cellSize * cols + gap * (cols - 1)
const gridHeight = cellSize * rows + gap * (rows - 1)

// Initialize the grid array with inactive cells
const grid = ref(Array(rows * cols).fill({ active: false }))

// Track the selected path coordinates
const pathCoordinates = ref<Coordinate[]>([])

// Create array for the waypoint generator itself
const waypoints = ref<Coordinate[]>([])

const dronePoints = ref<{ point: Coordinate; droneId: number }[]>([])

const currentMode = ref<Mode>(Mode.PATH) // Default is draw
const isDragging = ref(false) // Default to no dragging

const notificationMessage = ref<string | null>(null) // To store the notification message

/**
 * Displays a notification message for a set duration.
 * @param message The message to display.
 * @param duration Time (in milliseconds) to display the message.
 */
const showNotification = (message: string, duration = 5000) => {
  notificationMessage.value = message
  setTimeout(() => {
    notificationMessage.value = null
  }, duration)
}

// Watch for mode changes and reset the grid
watch(currentMode, (newMode, oldMode) => {
  if (newMode !== oldMode) {
    resetPath()
  }
})
const setMode = (mode: Mode) => {
  currentMode.value = mode
}

const lineSegments = computed(() => {
  const segments = pathCoordinates.value.slice(1).map((end, index) => ({
    start: pathCoordinates.value[index],
    end: end,
    intersecting: false, // Default to false
  }))

  // Check each segment for intersections with every other segment
  segments.forEach((segment, i) => {
    for (let j = 0; j < i; j++) {
      if (doLinesIntersect(segment.start, segment.end, segments[j].start, segments[j].end)) {
        segment.intersecting = true
        segments[j].intersecting = true
      }
    }
  })

  return segments
})

const getDroneId = (index: number) => {
  const point = { x: index % cols, y: Math.floor(index / cols) }
  const drone = dronePoints.value.find((dp) => dp.point.x === point.x && dp.point.y === point.y)
  return drone ? drone.droneId : ''
}

const startDrag = () => {
  if (currentMode.value === Mode.PATH) isDragging.value = true
}

const endDrag = () => {
  isDragging.value = false
}

const handleDrag = (event: MouseEvent) => {
  if (!isDragging.value || currentMode.value !== Mode.PATH) return
  const rect = (event.target as HTMLElement).closest('.grid-container')?.getBoundingClientRect()
  if (!rect) return

  const x = Math.floor((event.clientX - rect.left) / cellSize)
  const y = Math.floor((event.clientY - rect.top) / cellSize)
  const index = y * cols + x

  if (x >= 0 && x < cols && y >= 0 && y < rows && !grid.value[index].active) {
    toggleCell(index)
  }
}

const toggleCell = (index: number) => {
  const point = { x: index % cols, y: Math.floor(index / cols) }

  if (currentMode.value === Mode.PATH) {
    if (!grid.value[index].active) {
      grid.value[index] = { active: true }
      pathCoordinates.value.push(point)
    }
  } else if (currentMode.value === Mode.POINTS) {
    const droneIndex = dronePoints.value.findIndex(
      (dp) => dp.point.x === point.x && dp.point.y === point.y,
    )
    if (droneIndex !== -1) {
      grid.value[index] = { active: false }
      dronePoints.value.splice(droneIndex, 1)
    } else {
      const availableDrone = drones.value.find(
        (drone) => drone.available && !dronePoints.value.some((dp) => dp.droneId === drone.id),
      )
      if (availableDrone) {
        grid.value[index] = { active: true }
        dronePoints.value.push({ point, droneId: availableDrone.id })
      } else {
        alert('No available drones!')
      }
    }
  }
}

// Undo the last cell in the path
const undo = () => {
  if (currentMode.value === Mode.PATH && pathCoordinates.value.length > 0) {
    const lastPoint = pathCoordinates.value.pop()!
    const index = lastPoint.y * cols + lastPoint.x
    grid.value[index] = { active: false }
  } else if (currentMode.value === Mode.POINTS && dronePoints.value.length > 0) {
    const lastPoint = dronePoints.value.pop()!
    const index = lastPoint.point.y * cols + lastPoint.point.x
    grid.value[index] = { active: false }
  }
}
// Reset the path and grid
const resetPath = () => {
  pathCoordinates.value = []
  dronePoints.value = []
  waypoints.value = []
  grid.value = Array(rows * cols).fill({ active: false })
}

const completePath = () => {
  if (currentMode.value === Mode.PATH) {
    const hasIntersections = lineSegments.value.some((segment) => segment.intersecting)

    // Handle intersection by asking user to undo or start from scratch
    if (hasIntersections) {
      showNotification('Path contains intersecting lines. Please fix them before proceeding.')
      return
    }

    // Generate waypoints if no intersections
    waypoints.value = []
    for (let i = 0; i < pathCoordinates.value.length - 1; i++) {
      const start = pathCoordinates.value[i]
      const end = pathCoordinates.value[i + 1]

      // Calculate distance between points
      const distance = Math.sqrt(Math.pow(end.x - start.x, 2) + Math.pow(end.y - start.y, 2))
      // Dynamically determine the number of steps
      const steps = Math.max(1, Math.ceil(distance / maxStepSize)) // At least 1 step

      // Add the starting point
      waypoints.value.push(start)

      // Add intermediate points
      waypoints.value.push(...generateIntermediatePoints(start, end, steps))
    }

    // Add the last point
    if (pathCoordinates.value.length > 0) {
      waypoints.value.push(pathCoordinates.value[pathCoordinates.value.length - 1])
    }

    console.log('Path completed with coordinates:', pathCoordinates.value)
    console.log('Path waypoints including intermediate points:', waypoints.value)
    showNotification('Path and waypoints are ready!')
  } else if (currentMode.value === 'points') {
    // Validate points mode (ensure all points are within the drone limit)
    if (dronePoints.value.length > availableDronesCount.value) {
      showNotification('You have assigned more points than the number of available drones!')
      return
    }

    // Clear existing assignments
    drones.value.forEach((drone) => drone.assignPoints([]))

    // Assign points to drones using Drone class method
    dronePoints.value.forEach((dronePoint) => {
      const drone = drones.value.find((d) => d.id === dronePoint.droneId)
      if (drone && drone.available) {
        drone.assignPoints([dronePoint.point])
      }
    })

    console.log('Drone assignments for points:', dronePoints.value)
    showNotification('Drone assignments for points have been made successfully!')
  } else {
    showNotification('Invalid mode selected!')
  }
}

// Go back function to navigate to the previous page
const router = useRouter()
const goBack = () => {
  router.back()
}
</script>

<style scoped>
@font-face {
  font-family: mainFont;
  src: url('@/assets/Alkaline_Caps_Heavy.otf');
}

.control-row {
  display: flex;
  align-items: center;
  gap: 2vw;
  margin-top: 1rem;
}

.title-col {
  display: flex;
  align-items: center;
  width: 60vw;
  flex-direction: column;
}
.title {
  color: #6f1d77;
  font-size: 4.75rem;
  font-family: mainFont, 'Arial Narrow', Arial, sans-serif;
  height: 10vh;
}
.sub-title {
  color: #6f1d77;
  font-weight: 500;
  font-size: 1.75rem;
  font-family: 'Arial Narrow', Arial, sans-serif;
  margin-top: 2vh;
}
.path-drawing {
  background-color: #f7ecd8;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  min-height: 100vh; /* Ensures the background color fills the viewport */
  min-width: 100vw;
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
  background-color: #f7ecd8;
  border: 2px solid #6f1d77;
  cursor: pointer;
  transition: background-color 0.3s;
}

.grid-cell.active {
  background-color: #6f1d77; /* Active cell color */
}

/* .grid-cell::after {
  content: attr(data-drone-id);
  display: block;
  text-align: center;
  font-size: 1.5rem;
  color: black;
  background-color: #6f1d77;
} */

/* Overlay for lines */
.line-overlay {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none; /* Prevent SVG overlay from blocking clicks */
}

.notification {
  color: #6f1d77;
  font-weight: 300;
  font-size: 1.4rem;
  font-family: 'Arial Narrow', Arial, sans-serif;
}
.button-container {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.control-button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
  color: #6f1d77;
  border: 2px solid #6f1d77;
  border-radius: 10px 0px 10px 0px;
  transition: background-color 0.3s;
}

.back-button {
  padding: 1rem 2rem;
  margin-left: 1vw;
  margin-top: 1vh;
  font-size: 1rem;
  cursor: pointer;
  background-color: #6f1d77;
  color: #f7ecd8;
  border: 0px solid #f7ecd8;
  border-radius: 4px;
  align-self: flex-start;
}

#undo-button {
  background-color: #ff99ff;
}

#complete-button {
  background-color: #d8f103;
}

#reset-button {
  background-color: #ffe5ff;
}

.mode-button {
  padding: 10px 20px;
  margin: 5px;
  border: none;
  cursor: pointer;
  font-size: 16px;
  border-radius: 5px;
  transition:
    background-color 0.3s,
    color 0.3s;
  margin: 0px;
  width: 15vw;
}

.mode-button.active {
  background-color: #6f1d77; /* Active button color */
  color: #f7ecd8;
  margin: 0px;
}

.mode-button:not(.active) {
  background-color: #f7ecd8; /* Inactive button color */
  color: #6f1d77;
  border: 2px solid #6f1d77;
  cursor: not-allowed;
  margin: 0px;
}

.mode-toggle {
  width: 15vw;
}

#path-mode-button {
  border-radius: 5px 5px 0 0;
}
#points-mode-button {
  border-radius: 0 0 5px 5px;
}
</style>
