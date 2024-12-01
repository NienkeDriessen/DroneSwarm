<template>
  <div class="path-drawing">
    <button @click="goBack" class="back-button">Back</button>
    <h1>Create Your Path</h1>
    <p>Click on the grid squares to draw the path</p>

    <div class="mode-toggle">
      <label for="mode">Mode:</label>
      <select id="mode" v-model="currentMode">
        <option value="path">Path Drawing</option>
        <option value="points">Point Assignment</option>
      </select>
    </div>

    <!-- Drone Status Overview -->
    <div class="drone-status-container">
      <h3>Drone Status</h3>
      <div class="drone-status">
        <div
          v-for="drone in drones"
          :key="drone.id"
          :class="['drone-box', { 'unavailable': !drone.available, 'available': drone.available }]"
        >
          <div class="drone-header">
            <span>Drone {{ drone.id }}</span>
            <span
              :class="['status-indicator', { 'available': drone.available, 'unavailable': !drone.available }]"
            ></span>
          </div>
          <div class="drone-status-text" v-if="drone.available">Available</div>
          <div class="drone-status-text" v-else>Unavailable</div>
          <div v-if="drone.assignedPoints && drone.assignedPoints.length > 0" class="assigned-points">
            <strong>Assigned Points:</strong>
            <ul>
              <li v-for="point in drone.assignedPoints" :key="`${point.x}-${point.y}`">
                ({{ point.x }}, {{ point.y }})
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>


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
        :data-drone-id="currentMode === 'points' ? getDroneId(index) : ''"
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
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { doLinesIntersect, generateIntermediatePoints, type Coordinate } from '../assets/GeometryTools'

interface Drone {
  id: number;
  available: boolean;
  assignedPoints: Coordinate[];
}

//Dummy drones available
const drones = ref<Drone[]>([
  { id: 1, available: true, assignedPoints: [] },
  { id: 2, available: true, assignedPoints: [] },
  { id: 3, available: true, assignedPoints: [] },
  { id: 4, available: true, assignedPoints: [] },
  { id: 5, available: false, assignedPoints: [] },
  { id: 6, available: false, assignedPoints: [] },
  { id: 7, available: false, assignedPoints: [] },
  { id: 8, available: false, assignedPoints: [] },
]);

// Helper to count available drones
const availableDronesCount = computed(() =>
  drones.value.filter((drone) => drone.available).length
);



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

const dronePoints = ref<{ point: Coordinate, droneId: number }[]>([]);

const currentMode = ref('path'); // Default to Path Drawing mode

// Watch for mode changes and reset the grid
watch(currentMode, (newMode, oldMode) => {
  if (newMode !== oldMode) {
    resetPath();
  }
});

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
  const point = { x: index % cols, y: Math.floor(index / cols) };
  const drone = dronePoints.value.find((dp) => dp.point.x === point.x && dp.point.y === point.y);
  return drone ? drone.droneId : '';
};

const toggleCell = (index: number) => {
  if (currentMode.value === 'path') {
    // Existing path drawing logic
    if (pathCoordinates.value.length === 0 || !grid.value[index].active) {
      grid.value[index] = { active: true };
      pathCoordinates.value.push({
        x: index % cols,
        y: Math.floor(index / cols),
      });
    }
  } else if (currentMode.value === 'points') {
    const availableDronesCount = drones.value.filter((drone) => drone.available).length;

    // Check if the cell is already assigned
    const cellIndex = dronePoints.value.findIndex(
      (dp) => dp.point.x === index % cols && dp.point.y === Math.floor(index / cols)
    );

    if (cellIndex !== -1) {
      // Deactivate the cell and remove its assignment
      grid.value[index] = { active: false };
      dronePoints.value.splice(cellIndex, 1);
    } else if (!grid.value[index].active) {
      // Check if adding another point exceeds the available drones
      if (dronePoints.value.length >= availableDronesCount) {
        alert('You cannot assign more points than the number of available drones!');
        return;
      }

      // Activate the cell and assign it to the next available drone
      grid.value[index] = { active: true };
      const point = {
        x: index % cols,
        y: Math.floor(index / cols),
      };

      const availableDrone = drones.value[dronePoints.value.length];
      if (availableDrone && availableDrone.available) {
        dronePoints.value.push({ droneId: availableDrone.id, point });
      }
    }
  }
};


// Undo the last cell in the path
const undo = () => {
  if (currentMode.value === 'path') {
    if (pathCoordinates.value.length > 0) {
      const lastPoint = pathCoordinates.value.pop()
      if (lastPoint) {
        const lastIndex = lastPoint.y * cols + lastPoint.x
        grid.value[lastIndex] = { active: false }
      }
    }
  }
  else if (currentMode.value === 'points') {
    if (dronePoints.value.length > 0) {
      const lastPoint = dronePoints.value.pop()
      if (lastPoint) {
        const lastIndex = lastPoint.point.y * cols + lastPoint.point.x
        grid.value[lastIndex] = { active: false }
      }
    }
  }
}

// Reset the path and grid
const resetPath = () => {
  pathCoordinates.value = [];
  dronePoints.value = [];
  waypoints.value = [];
  grid.value = Array(rows * cols).fill({ active: false })
}


const completePath = () => {
  if (currentMode.value === 'path') {
    const hasIntersections = lineSegments.value.some((segment) => segment.intersecting);

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

      // Calculate distance between points
      const distance = Math.sqrt(Math.pow(end.x - start.x, 2) + Math.pow(end.y - start.y, 2));
      // Dynamically determine the number of steps
      const steps = Math.max(1, Math.ceil(distance / maxStepSize)); // At least 1 step

      // Add the starting point
      waypoints.value.push(start);

      // Add intermediate points
      waypoints.value.push(...generateIntermediatePoints(start, end, steps));
    }

    // Add the last point
    if (pathCoordinates.value.length > 0) {
      waypoints.value.push(pathCoordinates.value[pathCoordinates.value.length - 1]);
    }

    console.log('Path completed with coordinates:', pathCoordinates.value);
    console.log('Path waypoints including intermediate points:', waypoints.value);
    alert('Path and waypoints are ready!');

  } else if (currentMode.value === 'points') {
    // Validate points mode (ensure all points are within the drone limit)
    if (dronePoints.value.length > availableDronesCount.value) {
      alert('You have assigned more points than the number of available drones!');
      return;
    }

    // Clear any previous assignments and assign points to drones
    const availableDrones = drones.value.filter((drone) => drone.available);

    if (dronePoints.value.length > availableDrones.length) {
      alert('Not enough available drones to assign all points!');
      return;
    }

    // Assign points to drones dynamically
    dronePoints.value = dronePoints.value.map((dronePoint, index) => {
      const drone = availableDrones[index];
      if (drone) {
        return { droneId: drone.id, point: dronePoint.point };
      }
      return null; // Handle case where no drone is available
    }).filter((assignment) => assignment !== null); // Remove null assignments

    // Update drone assignments
    drones.value.forEach((drone) => (drone.assignedPoints = [])); // Reset assignments
    dronePoints.value.forEach((dronePoint) => {
      const drone = drones.value.find((d) => d.id === dronePoint.droneId);
      if (drone) {
        drone.assignedPoints.push(dronePoint.point);
      }
    });

    console.log('Drone assignments for points:', dronePoints.value);
    alert('Drone assignments for points have been made successfully!');

  } else {
    alert('Invalid mode selected!');
  }
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

.grid-cell::after {
  content: attr(data-drone-id);
  display: block;
  text-align: center;
  font-size: 1.5rem;
  color: black;
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

/* Container for the Drone Status Overview */
.drone-status-container {
  padding: 20px;
  border: 2px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
  max-width: 90%;
  margin: 20px auto;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}

/* Title */
.drone-status-container h3 {
  text-align: center;
  color: #333;
  font-family: 'Arial', sans-serif;
  margin-bottom: 15px;
}

/* Drone Status Grid */
.drone-status {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); /* Dynamic columns */
  grid-auto-rows: auto; /* Auto-adjust height */
  grid-auto-flow: column; /* Fill rows first, then columns */
  gap: 15px;
}

/* Individual Drone Box */
.drone-box {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background-color: #fff;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.drone-box.available {
  border: 2px solid #4caf50;
  background-color: #e8f5e9;
}

.drone-box.unavailable {
  border: 2px solid #f44336;
  background-color: #ffebee;
}

.drone-box:hover {
  transform: scale(1.03);
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
}

/* Drone Header */
.drone-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 16px;
  color: #333;
}

/* Status Indicator */
.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.status-indicator.available {
  background-color: #4caf50;
}

.status-indicator.unavailable {
  background-color: #f44336;
}

/* Drone Status Text */
.drone-status-text {
  font-size: 14px;
  color: #555;
}

/* Assigned Points List */
.assigned-points {
  background-color: #f1f1f1;
  padding: 8px;
  border-radius: 4px;
  font-size: 14px;
}

.assigned-points ul {
  padding-left: 20px;
  margin: 5px 0;
}

.assigned-points li {
  list-style: square;
  font-size: 12px;
  color: #333;
}
</style>
