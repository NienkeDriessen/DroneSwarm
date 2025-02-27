<template>
  <div
    class="drone-status-container"
    :style="{
      top: position.top,
      left: position.left,
      width: isMinimized ? '250px' : size.width,
      height: isMinimized ? '75px' : size.height
    }"
  >
    <div class="drone-status-header" @mousedown="startDrag">
      <h3>Drone Status</h3>
      <button @click.stop="toggleMinimize">
        {{ isMinimized ? 'Maximize' : 'Minimise' }}
      </button>
    </div>
    <div v-if="!isMinimized" class="drone-status">
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
        <div class="drone-details">
          <div class="battery-level">Battery: {{ drone.batteryLevel }}%</div>
          <div class="position">
            Position: ({{ drone.position.x.toFixed(2) }},
            {{ drone.position.y.toFixed(2) }},
            {{ drone.position.z.toFixed(2) }})
          </div>
          <div class="velocity">
            Velocity: ({{ drone.velocity.x.toFixed(2) }},
            {{ drone.velocity.y.toFixed(2) }},
            {{ drone.velocity.z.toFixed(2) }})
          </div>
        </div>
        <div v-if="drone.assignedPoints && drone.assignedPoints.length > 0" class="assigned-points">
          <strong>Assigned Points:</strong>
          <ul>
            <li v-for="point in drone.assignedPoints" :key="`${point.x},${point.y}`">
              ({{ point.x }}, {{ point.y }})
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div class="resize-handle" @mousedown.stop @mousedown="startResize"></div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import Drone from '../models/Drone';

defineProps<{
  drones: Drone[];
}>();

const isMinimized = ref(false);
const position = ref({ top: '20px', left: '20px' });
const size = ref({ width: '400px', height: '300px' });

const toggleMinimize = () => {
  isMinimized.value = !isMinimized.value;
};

const startDrag = (event: MouseEvent) => {
  const initialX = event.clientX;
  const initialY = event.clientY;
  const startTop = parseInt(position.value.top, 10);
  const startLeft = parseInt(position.value.left, 10);

  const onMouseMove = (moveEvent: MouseEvent) => {
    position.value = {
      top: `${startTop + (moveEvent.clientY - initialY)}px`,
      left: `${startLeft + (moveEvent.clientX - initialX)}px`
    };
  };

  const onMouseUp = () => {
    document.removeEventListener('mousemove', onMouseMove);
    document.removeEventListener('mouseup', onMouseUp);
  };

  document.addEventListener('mousemove', onMouseMove);
  document.addEventListener('mouseup', onMouseUp);
};

const startResize = (event: MouseEvent) => {
  const startX = event.clientX;
  const startY = event.clientY;
  const parent = (event.target as HTMLElement).parentElement;
  if (!parent) return;
  const computedStyle = document.defaultView?.getComputedStyle(parent);
  if (!computedStyle) return;
  const startWidth = parseInt(computedStyle.width, 10);
  const startHeight = parseInt(computedStyle.height, 10);

  const onMouseMove = (moveEvent: MouseEvent) => {
    size.value = {
      width: `${startWidth + moveEvent.clientX - startX}px`,
      height: `${startHeight + moveEvent.clientY - startY}px`,
    };
  };

  const onMouseUp = () => {
    document.removeEventListener('mousemove', onMouseMove);
    document.removeEventListener('mouseup', onMouseUp);
  };

  document.addEventListener('mousemove', onMouseMove);
  document.addEventListener('mouseup', onMouseUp);
};
</script>

<style scoped>
.drone-status-container {
  position: absolute;
  border: 0px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  max-width: 90%;
}

.drone-status-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background-color: #007bff;
  color: #fff;
  cursor: move;
  user-select: none;
}

.drone-status-header h3 {
  font-size: 16px;
  color: #fff;
}

.drone-status-header button {
  background-color: #0056b3;
  color: #fff;
  border: none;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
}

.drone-status-header button:hover {
  background-color: #0056b3;
}

/* Added scroll slider styles to .drone-status */
.drone-status {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  grid-gap: 10px 2%;
  overflow-y: auto;
  max-height: calc(100% - 50px); /* Adjust based on header height */
}

.drone-box {
  padding: 4px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background-color: #f9f9f9;
  display: flex;
  flex-direction: column;
  gap: 1px;
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

.drone-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 12px;
  color: #333;
}

.status-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.status-indicator.available {
  background-color: #4caf50;
}

.status-indicator.unavailable {
  background-color: #f44336;
}

.drone-status-text {
  font-size: 11px;
  color: #555;
}

.drone-details {
  font-size: 11px;
  color: #444;
}

.battery-level {
  font-weight: bold;
  color: #333;
}

.assigned-points {
  background-color: #f1f1f1;
  padding: 6px;
  border-radius: 4px;
  font-size: 12px;
  color: #333;
}

.assigned-points ul {
  padding-left: 20px;
  margin: 5px 0;
}

.assigned-points li {
  list-style: square;
  font-size: 10px;
  color: #333;
}

.resize-handle {
  width: 15px;
  height: 15px;
  background-color: #007bff;
  position: absolute;
  bottom: 0;
  right: 0;
  cursor: nesw-resize;
}
</style>
