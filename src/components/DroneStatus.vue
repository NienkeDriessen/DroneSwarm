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
    <div class="drone-status-header" @mousedown="startDrag" @mousedown.stop>
      <h3>Drone Status</h3>
      <button @click.stop="toggleMinimize">
        {{ isMinimized ? 'Expand' : 'Minimise' }}
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
            Position: ({{ drone.position.x.toFixed(3) }},
            {{ drone.position.y.toFixed(3) }},
            {{ drone.position.z.toFixed(3) }})
          </div>
          <div class="velocity">
            Velocity: ({{ drone.velocity.x.toFixed(3) }},
            {{ drone.velocity.y.toFixed(3) }},
            {{ drone.velocity.z.toFixed(3) }})
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
  // Listen on the header only.
  const currentTarget = event.currentTarget as HTMLElement | null;
  if (!currentTarget) return;
  const element = currentTarget.parentElement;
  if (!element) return;
  const rect = element.getBoundingClientRect();
  const offsetX = event.clientX - rect.left;
  const offsetY = event.clientY - rect.top;

  const onMouseMove = (moveEvent: MouseEvent) => {
    position.value = {
      top: `${moveEvent.clientY - offsetY}px`,
      left: `${moveEvent.clientX - offsetX}px`,
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
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
  max-width: 90%;
  margin: 20px auto;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  overflow: auto;
}

.drone-status-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  cursor: move;
}

.drone-status-header h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.drone-status-header button {
  padding: 5px 10px;
  font-size: 14px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.drone-status-header button:hover {
  background-color: #0056b3;
}

.drone-status {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  grid-gap: 10px;
}

.drone-box {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background-color: #f9f9f9;
  display: flex;
  flex-direction: column;
  gap: 6px;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.drone-box.available {
  border: 1px solid #4caf50;
  background-color: #e8f5e9;
}

.drone-box.unavailable {
  border: 1px solid #f44336;
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
  font-size: 12px;
  color: #555;
}

.drone-details {
  font-size: 12px;
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
  cursor: ew-resize;
}
</style>
