<template>
  <div class="path-drawing">
    <div class="control-row">
      <button @click="goBack" class="back-button">Terug</button>
      <div class="title-col">
        <h1 class="title">Teken een pad voor de drones</h1>
        <p class="sub-title">Klik of sleep over het raster om een pad te tekenen</p>
        <div class="countdown-timer">{{ countdown_value }}</div>
      </div>
      <!-- <div class="mode-toggle">
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
      </div> -->
    </div>
    <!-- Grid container with overlay for lines -->
    <div
      class="grid-container"
      @mousedown="startDrag"
      @mouseup="endDrag"
      @mouseleave="endDrag"
      @mousemove="handleDrag"
      @touchstart.prevent="startTouch"
      @touchmove.prevent="handleTouch"
      @touchend.prevent="endTouch"
      @touchcancel.prevent="endTouch"
      :style="{
        gridTemplateColumns: `repeat(${cols}, ${cellSize}px)`,
        gridTemplateRows: `repeat(${rows}, ${cellSize}px)`,
        width: `${gridWidth}px`,
        height: `${gridHeight}px`
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
          :stroke="segment.intersecting ? '#DB1F22' : '#6f1d77'"
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
        <button id="undo-button" @click="undo" class="control-button">Ongedaan maken</button>
        <button id="reset-button" @click="resetPath" class="control-button">Reset</button>
        <button id="complete-button" @click="completePath" class="control-button">Klaar!</button>
      </div>
    </div>
    <DroneStatus :drones="drones" />
    <DroneRadar3 :drones="drones" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import {
  doLinesIntersect,
  generateIntermediatePoints,
  type Coordinate,
} from '../assets/GeometryTools'
import DroneStatus from '../components/DroneStatus.vue'
import DroneRadar3 from '../components/DroneRadar3.vue'
import Drone from '../models/Drone'

enum Mode {
  PATH = 'path',
  POINTS = 'points',
}

const DRONES_API_URL = 'http://145.94.190.242:3000/api/drones'
const POLLING_INTERVAL = 50

// Drones data, fetched periodically via axios.
const drones = ref<Drone[]>([])

interface DroneData {
  bat_level: number
  pos_x: number
  pos_y: number
  pos_z: number
  vel_x: number
  vel_y: number
  vel_z: number
}

const fetchDronesData = () => {
  axios
    .get(DRONES_API_URL)
    .then((response) => {
      const dronesData: Record<string, DroneData> = response.data // Enforce type safety
      // Map drones_data structure to Drone instances
      drones.value = Object.entries(dronesData).map(
        ([id, data]) =>
          new Drone(
            parseInt(id), // Drone ID
            true, // Assume drones are available unless there's additional info
            [], // Empty assignedPoints (or modify if necessary)
            data.bat_level, // Battery Level
            { x: data.pos_x, y: data.pos_y, z: data.pos_z }, // Position
            { x: data.vel_x, y: data.vel_y, z: data.vel_z }, // Velocity
          ),
      )
    })
    .catch((error) => {
      console.error('Error fetching drones data:', error)
    })
}

let pollingIntervalId: number | null = null
onMounted(() => {
  fetchDronesData()
  pollingIntervalId = window.setInterval(fetchDronesData, POLLING_INTERVAL)
})

onUnmounted(() => {
  if (pollingIntervalId !== null) {
    clearInterval(pollingIntervalId)
  }
})

const availableDronesCount = computed(() =>
  drones.value.filter((drone) => drone.available).length,
)

// Dimensions and grid calculation constants
const rows = 14
const cols = 18
const maxGridWidth = 700
const maxGridHeight = 500
const gap = 2
const maxStepSize = 0.5
const countdown_max = 25
let countdown_value = countdown_max

const cellSize = Math.min(
  (maxGridWidth - gap * (cols - 1)) / cols,
  (maxGridHeight - gap * (rows - 1)) / rows,
)
const gridWidth = cellSize * cols + gap * (cols - 1)
const gridHeight = cellSize * rows + gap * (rows - 1)

// Initialize the grid array with inactive cells (note: each cell is the same object reference)
const grid = ref(Array(rows * cols).fill({ active: false }))

// State for drawn path and drone assignments.
const pathCoordinates = ref<Coordinate[]>([])
const waypoints = ref<Coordinate[]>([])
const dronePoints = ref<{ point: Coordinate; droneId: number }[]>([])

const currentMode = ref<Mode>(Mode.PATH) // Default mode: draw path
const isDragging = ref(false) // Interaction flag for drag events

const notificationMessage = ref<string | null>(null) // For showing temporary messages

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

// Watch for mode changes and reset the grid when the mode changes.
watch(currentMode, (newMode, oldMode) => {
  if (newMode !== oldMode) {
    resetPath()
  }
})
// const setMode = (mode: Mode) => {
//   currentMode.value = mode
// }

const lineSegments = computed(() => {
  // Create consecutive segments from the drawn path.
  const segments = pathCoordinates.value.slice(1).map((end, index) => ({
    start: pathCoordinates.value[index],
    end: end,
    intersecting: false, // Default to false
  }))

  // Check each segment for intersections with any previous segments.
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

// Mouse drag event handlers
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

// New functions for touch event support
const startTouch = () => {
  if (currentMode.value === Mode.PATH) {
    isDragging.value = true
  }
}

const handleTouch = (event: TouchEvent) => {
  if (!isDragging.value || currentMode.value !== Mode.PATH) return
  const touch = event.touches[0]
  const gridContainer = (event.target as HTMLElement).closest('.grid-container')
  if (!gridContainer) return
  const rect = gridContainer.getBoundingClientRect()
  const x = Math.floor((touch.clientX - rect.left) / cellSize)
  const y = Math.floor((touch.clientY - rect.top) / cellSize)
  const index = y * cols + x
  if (x >= 0 && x < cols && y >= 0 && y < rows && !grid.value[index].active) {
    toggleCell(index)
  }
}

const endTouch = () => {
  isDragging.value = false
}

const toggleCell = (index: number) => {
  const point = { x: index % cols, y: Math.floor(index / cols) }
  if (currentMode.value === Mode.PATH) {
    if (!grid.value[index].active) {
      if (pathCoordinates.value.length < countdown_max) {
        grid.value[index] = { active: true }
        pathCoordinates.value.push(point)
        countdown_value = countdown_max - pathCoordinates.value.length
      }
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

const undo = () => {
  if (currentMode.value === Mode.PATH && pathCoordinates.value.length > 0) {
    const lastPoint = pathCoordinates.value.pop()!
    const index = lastPoint.y * cols + lastPoint.x
    grid.value[index] = { active: false }
    countdown_value = countdown_max - pathCoordinates.value.length
  } else if (currentMode.value === Mode.POINTS && dronePoints.value.length > 0) {
    const lastPoint = dronePoints.value.pop()!
    const index = lastPoint.point.y * cols + lastPoint.point.x
    grid.value[index] = { active: false }
  }
}

const resetPath = () => {
  pathCoordinates.value = []
  dronePoints.value = []
  waypoints.value = []
  grid.value = Array(rows * cols).fill({ active: false })
  countdown_value = countdown_max - pathCoordinates.value.length
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
      // Dynamically determine the number of steps (at least 1)
      const steps = Math.max(1, Math.ceil(distance / maxStepSize))
      // Add the starting point and intermediate points
      waypoints.value.push(start)
      waypoints.value.push(...generateIntermediatePoints(start, end, steps))
    }
    // Add the last point
    if (pathCoordinates.value.length > 0) {
      waypoints.value.push(pathCoordinates.value[pathCoordinates.value.length - 1])
    }
    console.log('Path completed with coordinates:', pathCoordinates.value)
    console.log('Path waypoints including intermediate points:', waypoints.value)
    sendPathCoordinates()
    showNotification('Path and waypoints are ready!')
  } else if (currentMode.value === Mode.POINTS) {
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

// ----- New function to map and send coordinates -----
// These constants define the real-life space that your UI grid maps to.
// const REAL_ORIGIN = { y: 1.8, z: 0.0 } // Adjust origin as needed. Big
const REAL_ORIGIN = { y: 1.25, z: 0.0 } // Adjust origin as needed. small
// const REAL_WIDTH = 3.9 // Total width in real-life units. Big
const REAL_WIDTH = 2.7 // Total width in real-life units. small
// const REAL_HEIGHT = 2.5 // Total height in real-life units. Big
const REAL_HEIGHT = 2.0 // Total height in real-life units. small
const FIXED_X = 0.0 // Fixed third coordinate for 2D drawing.

// Map a UI grid coordinate (with x,y) to real-life coordinates.
function mapGridToReal(coord: Coordinate) {
  return {
    x: FIXED_X,
    y: REAL_ORIGIN.y - coord.x * (REAL_WIDTH / cols),
    z: REAL_ORIGIN.z + (rows - coord.y) * (REAL_HEIGHT / rows),
  }
}

// Replace the existing sendPathCoordinates function with this version:
const sendPathCoordinates = async () => {
  const availableDrones = drones.value.filter((drone) => drone.available)
  const mappedWaypoints = waypoints.value.map((wp) => mapGridToReal(wp))
  const SENDING_INTERVAL = 200 // adjust sending rate (ms) as needed
  const DRONE_OFFSET = 5 // offset in waypoint steps between following drones
  let index = 0

  const intervalId = setInterval(() => {
    // Ensure we run a few extra iterations so trailing drones can reach the end
    if (index >= mappedWaypoints.length + (availableDrones.length - 1) * DRONE_OFFSET) {
      clearInterval(intervalId)
      return
    }
    // For each drone, calculate an offset based on its position in availableDrones.
    const updates = availableDrones.map((drone, dIndex) => {
      const waypointIndex = index - dIndex * DRONE_OFFSET
      let waypoint: { x: number; y: number; z: number }
      if (waypointIndex < 0) {
        // Before starting, hold on at the first waypoint.
        waypoint = mappedWaypoints[0]
      } else if (waypointIndex >= mappedWaypoints.length) {
        // After finishing the drawn path, assign a standby point on a line in the x direction.
        const finalWaypoint = mappedWaypoints[mappedWaypoints.length - 1]
        let standbyX: number
        if (availableDrones.length > 1) {
          standbyX = 1.25 + dIndex * ((-1.75 - 1.25) / (availableDrones.length - 1))
        } else {
          standbyX = 1.25
        }
        waypoint = { x: standbyX, y: finalWaypoint.y, z: finalWaypoint.z }
      } else {
        waypoint = mappedWaypoints[waypointIndex]
      }
      return {
        droneId: drone.id,
        pos_x: waypoint.x,
        pos_y: waypoint.y,
        pos_z: waypoint.z,
        vel_x: 0.0,
        vel_y: 0.0,
        vel_z: 0.0,
      }
    })

    axios
      .post(DRONES_API_URL, updates, { timeout: 2000 })
      .then((response) => {
        console.log(response)
      })
      .catch((error) => {
        if (error.response) {
          console.log('SERVER ERROR')
          console.log(error.response)
        } else if (error.request) {
          console.log('NETWORK ERROR: ' + error.message)
          console.log(error.request)
          console.log(error.toJSON())
        } else {
          console.log('ERROR', error.message)
        }
      })

    index++
  }, SENDING_INTERVAL)
}

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
.countdown-timer {
  position: absolute;
  top: 3vh;
  right: 5vw;
  /* color: #ff99ff; */
  color: #6f1d77;
  font-size: 4.75rem;
  font-family: mainFont, 'Arial Narrow', Arial, sans-serif;
  height: 10vh;
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
  font-size: 4rem;
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
  border: 2px solid #ccacc9;
  cursor: pointer;
  transition: background-color 0.3s;
}

.grid-cell.active {
  background-color: #ff99ff; /* Active cell color */
  border: 7px solid #6f1d77;
  z-index: 100;
  border-radius: 50%;
  -webkit-tap-highlight-color: transparent;
  transform: scale(0.95);
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
  position: absolute;
  padding: 1rem 2rem;
  left: 3vw;
  top: 4vh;
  font-size: 1rem;
  cursor: pointer;
  background-color: #6f1d77;
  color: #f7ecd8;
  border: 0px solid #f7ecd8;
  border-radius: 4px;
  align-self: flex-start;
}

#undo-button {
  background-color: #6f1d77;
  color: #f7ecd8;
  font-size: 1.7rem;
}

#complete-button {
  background-color: #6f1d77;
  color: #f7ecd8;
  font-size: 1.7rem;
}

#reset-button {
  background-color: #6f1d77;
  color: #f7ecd8;
  font-size: 1.7rem;
}

#undo-button:focus #complete-butt:focus #reset-button:focus {
  -webkit-tap-highlight-color: transparent;
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
