<template>
  <div class="drone-status-container">
    <h3>Drone Status</h3>
    <div class="drone-status">
      <div
        v-for="drone in drones"
        :key="drone.id"
        :class="['drone-box', { unavailable: !drone.available, available: drone.available }]"
      >
        <div class="drone-header">
          <span>Drone {{ drone.id }}</span>
          <span
            :class="[
              'status-indicator',
              { available: drone.available, unavailable: !drone.available },
            ]"
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
</template>

<script setup lang="ts">
import Drone from '../models/Drone'

defineProps<{
  drones: Drone[]
}>()
</script>

<style scoped>
.drone-status-container {
  padding: 20px;
  border: 2px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
  max-width: 90%;
  margin: 20px auto;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  overflow: scroll;
}

.drone-status-container h3 {
  text-align: center;
  color: #333;
  font-family: 'Arial', sans-serif;
  margin-bottom: 15px;
}

.drone-status {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  grid-auto-rows: auto;
  grid-auto-flow: column;
  gap: 15px;
}

.drone-box {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background-color: #fff;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition:
    transform 0.2s ease-in-out,
    box-shadow 0.2s ease-in-out;
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
  font-size: 16px;
  color: #333;
}

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

.drone-status-text {
  font-size: 14px;
  color: #555;
}

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
