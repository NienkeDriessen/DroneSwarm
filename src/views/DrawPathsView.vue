<template>
  <div class="path-drawing">
    <button @click="goBack" class="back-button">Back</button>
    <h1 class="title">Create Your Path</h1>
    <p class="sub-title">Click on the grid squares to draw the path</p>

    <div class="mode-toggle">
      <label for="mode">Mode:</label>
      <select id="mode" v-model="currentMode">
        <option value="path">Path Drawing</option>
        <option value="points">Point Assignment</option>
      </select>
    </div>

    <!-- Drone Status Overview -->


    <!-- Grid container with overlay for lines -->
    <div
      class="grid-container"
      @mousedown="startDrag"
      @mouseup="endDrag"
      @mouseleave="endDrag"
      @mousemove="handleDrag"
      :style="{
        gridTemplateColumns: `repeat(${cols}, ${cellSize}px)`,
        gridTemplateRows: `repeat(${rows}, ${cellSize}px)`
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
          :stroke="segment.intersecting ? 'red' : '#435799'"
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
    <DroneStatus :drones="drones" />
    <DroneRadar3 :drones="drones" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import {
  doLinesIntersect,
  generateIntermediatePoints,
  type Coordinate,
} from '../assets/GeometryTools';
import DroneStatus from '../components/DroneStatus.vue';
// import DroneRadar from '../components/DroneRadar.vue';
import DroneRadar3 from '../components/DroneRadar3.vue';
import Drone from '../models/Drone';


const DRONES_API_URL = 'http://145.94.139.79:3000/api/drones';
const POLLING_INTERVAL = 50;

const drones = ref<Drone[]>([]);



// Define the expected structure of the incoming drone data
interface DroneData {
  bat_level: number;
  pos_x: number;
  pos_y: number;
  pos_z: number;
  vel_x: number;
  vel_y: number;
  vel_z: number;
}

// Fetch drones data
const fetchDronesData = async () => {
  try {
    const response = await axios.get(DRONES_API_URL);
    const dronesData: Record<string, DroneData> = response.data; // Enforce type safety
    console.log(dronesData); // Debugging output

    // Map drones_data structure to Drone instances
    drones.value = Object.entries(dronesData).map(([id, data]) =>
      new Drone(
        parseInt(id), // Drone ID
        true, // Assume drones are available unless there's additional info
        [], // Empty assignedPoints (or modify if necessary)
        data.bat_level, // Battery Level
        { x: data.pos_x, y: data.pos_y, z: data.pos_z }, // Position
        { x: data.vel_x, y: data.vel_y, z: data.vel_z } // Velocity
      )
    );

    console.log('Drones data updated:', drones.value);
  } catch (error) {
    console.error('Error fetching drones data:', error);
  }
};


let pollingIntervalId: number | null = null;
onMounted(() => {
  fetchDronesData();
  pollingIntervalId = window.setInterval(fetchDronesData, POLLING_INTERVAL);
});

onUnmounted(() => {
  if (pollingIntervalId !== null) {
    clearInterval(pollingIntervalId);
  }
});

const availableDronesCount = computed(() =>
  drones.value.filter((drone) => drone.available).length
);

const rows = 8;
const cols = 15;
const maxGridWidth = 700;
const maxGridHeight = 500;
const gap = 1;
const maxStepSize = 0.5;
const cellSize = Math.min(
  (maxGridWidth - gap * (cols - 1)) / cols,
  (maxGridHeight - gap * (rows - 1)) / rows
);
const gridWidth = cellSize * cols + gap * (cols - 1);
const gridHeight = cellSize * rows + gap * (rows - 1);

const grid = ref(Array(rows * cols).fill({ active: false }));
const pathCoordinates = ref<Coordinate[]>([]);
const waypoints = ref<Coordinate[]>([]);
const dronePoints = ref<{ point: Coordinate; droneId: number }[]>([]);
const currentMode = ref('path');
const isDragging = ref(false);

watch(currentMode, (newMode, oldMode) => {
  if (newMode !== oldMode) {
    resetPath();
  }
});

const lineSegments = computed(() => {
  const segments = pathCoordinates.value.slice(1).map((end, index) => ({
    start: pathCoordinates.value[index],
    end: end,
    intersecting: false,
  }));

  segments.forEach((segment, i) => {
    for (let j = 0; j < i; j++) {
      if (doLinesIntersect(segment.start, segment.end, segments[j].start, segments[j].end)) {
        segment.intersecting = true;
        segments[j].intersecting = true;
      }
    }
  });

  return segments;
});

const getDroneId = (index: number) => {
  const point = { x: index % cols, y: Math.floor(index / cols) };
  const drone = dronePoints.value.find(
    (dp) => dp.point.x === point.x && dp.point.y === point.y
  );
  return drone ? drone.droneId : '';
};

const startDrag = () => {
  if (currentMode.value === 'path') {
    isDragging.value = true;
  }
};

const endDrag = () => {
  isDragging.value = false;
};

const handleDrag = (event: MouseEvent) => {
  if (!isDragging.value || currentMode.value !== 'path') return;

  const rect = (event.target as HTMLElement)
    .closest('.grid-container')
    ?.getBoundingClientRect();
  if (!rect) return;

  const x = Math.floor((event.clientX - rect.left) / cellSize);
  const y = Math.floor((event.clientY - rect.top) / cellSize);

  if (x >= 0 && x < cols && y >= 0 && y < rows) {
    const index = y * cols + x;
    if (!grid.value[index].active) {
      toggleCell(index);
    }
  }
};

const toggleCell = (index: number) => {
  if (currentMode.value === 'path') {
    if (pathCoordinates.value.length === 0 || !grid.value[index].active) {
      grid.value[index] = { active: true };
      pathCoordinates.value.push({
        x: index % cols,
        y: Math.floor(index / cols),
      });
    }
  } else if (currentMode.value === 'points') {
    const availableDrones = drones.value.filter((drone) => drone.available);
    const usedDroneIds = new Set(dronePoints.value.map((dp) => dp.droneId));
    const availableDroneIds = availableDrones
      .map((drone) => drone.id)
      .filter((id) => !usedDroneIds.has(id))
      .sort((a, b) => a - b);

    const cellIndex = dronePoints.value.findIndex(
      (dp) => dp.point.x === index % cols && dp.point.y === Math.floor(index / cols)
    );

    if (cellIndex !== -1) {
      grid.value[index] = { active: false };
      dronePoints.value.splice(cellIndex, 1);
    } else if (!grid.value[index].active) {
      if (dronePoints.value.length >= availableDrones.length) {
        alert('You cannot assign more points than the number of available drones!');
        return;
      }

      grid.value[index] = { active: true };
      const point = {
        x: index % cols,
        y: Math.floor(index / cols),
      };

      if (availableDroneIds.length > 0) {
        const nextDroneId = availableDroneIds[0];
        dronePoints.value.push({ droneId: nextDroneId, point });
      }
    }
  }
};

const undo = () => {
  if (currentMode.value === 'path') {
    if (pathCoordinates.value.length > 0) {
      const lastPoint = pathCoordinates.value.pop();
      if (lastPoint) {
        const lastIndex = lastPoint.y * cols + lastPoint.x;
        grid.value[lastIndex] = { active: false };
      }
    }
  } else if (currentMode.value === 'points') {
    if (dronePoints.value.length > 0) {
      const lastPoint = dronePoints.value.pop();
      if (lastPoint) {
        const lastIndex = lastPoint.point.y * cols + lastPoint.point.x;
        grid.value[lastIndex] = { active: false };
      }
    }
  }
};

const resetPath = () => {
  pathCoordinates.value = [];
  dronePoints.value = [];
  waypoints.value = [];
  grid.value = Array(rows * cols).fill({ active: false });
};

const completePath = () => {
  if (currentMode.value === 'path') {
    const hasIntersections = lineSegments.value.some((segment) => segment.intersecting);

    if (hasIntersections) {
      alert('Path contains intersecting lines. Please fix them before proceeding.');
      return;
    }

    waypoints.value = [];
    for (let i = 0; i < pathCoordinates.value.length - 1; i++) {
      const start = pathCoordinates.value[i];
      const end = pathCoordinates.value[i + 1];

      const distance = Math.sqrt(
        Math.pow(end.x - start.x, 2) + Math.pow(end.y - start.y, 2)
      );
      const steps = Math.max(1, Math.ceil(distance / maxStepSize));

      waypoints.value.push(start);
      waypoints.value.push(...generateIntermediatePoints(start, end, steps));
    }

    if (pathCoordinates.value.length > 0) {
      waypoints.value.push(pathCoordinates.value[pathCoordinates.value.length - 1]);
    }

    console.log('Path completed with coordinates:', pathCoordinates.value);
    console.log('Path waypoints including intermediate points:', waypoints.value);
    alert('Path and waypoints are ready!');
  } else if (currentMode.value === 'points') {
    if (dronePoints.value.length > availableDronesCount.value) {
      alert('You have assigned more points than the number of available drones!');
      return;
    }

    drones.value.forEach((drone) => drone.assignPoints([]));
    dronePoints.value.forEach((dronePoint) => {
      const drone = drones.value.find((d) => d.id === dronePoint.droneId);
      if (drone && drone.available) {
        drone.assignPoints([dronePoint.point]);
      }
    });

    console.log('Drone assignments for points:', dronePoints.value);
    alert('Drone assignments for points have been made successfully!');
  } else {
    alert('Invalid mode selected!');
  }
};

const router = useRouter();
const goBack = () => {
  router.back();
};
</script>

<style scoped>
@font-face {
  font-family: mainFont;
  src: url('@/assets/Alkaline_Caps_Heavy.otf');
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
  min-height: 100vh;
  min-width: 100vw;
}

.grid-container {
  position: relative;
  display: grid;
  gap: 2px;
  margin: 1rem 0;
}

.grid-cell {
  background-color: #e0e0e0;
  cursor: pointer;
  transition: background-color 0.3s;
}

.grid-cell.active {
  background-color: #43b7ff;
}

.grid-cell::after {
  content: attr(data-drone-id);
  display: block;
  text-align: center;
  font-size: 1.5rem;
  color: black;
}

.line-overlay {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none;
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
  padding: 1rem 2rem;
  margin-left: 1vw;
  margin-top: 1vh;
  font-size: 1rem;
  cursor: pointer;
  background-color: #6f1d77;
  color: #f7ecd8;
  border: none;
  border-radius: 4px;
  align-self: flex-start;
}
</style>
