<template>
  <div
    class="drone-radar-container"
    :style="{
      top: position.top,
      left: position.left,
      width: isMinimized ? '250px' : containerSize.width,
      height: isMinimized ? '75px' : containerSize.height
    }"
  >
    <div class="drone-radar-header" @mousedown="startDrag">
      <span>Drone Radar</span>
      <button @click.stop="toggleMinimize">
        {{ isMinimized ? 'Maximize' : 'Minimise' }}
      </button>
    </div>
    <div v-if="!isMinimized" class="drone-radar-content">
      <!-- Plotly 3D scatter plot will be rendered here -->
      <div ref="plotlyContainer" style="width: 100%; height: 100%;"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, onMounted, watch } from 'vue';
import Drone from '../models/Drone';
import Plotly from 'plotly.js-dist-min';

// interface PlotlyCamera {
//   eye: { x: number; y: number; z: number };
//   center: { x: number; y: number; z: number };
//   up: { x: number; y: number; z: number };
// }

const props = defineProps<{
  drones: Drone[];
}>();

// Maximize/Minimize controls and drag for the overall window.
const isMinimized = ref(false);
const position = ref({ top: '50px', left: '50px' });
const containerSize = ref({ width: '500px', height: '5' });

const toggleMinimize = () => {
  isMinimized.value = !isMinimized.value;
};

// Drag functionality for the header.
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

// Ref for Plotly container.
const plotlyContainer = ref<HTMLElement | null>(null);

// Base layout with fixed axes extents.
const layout: Partial<Plotly.Layout> = {
  margin: { l: 0, r: 0, b: 0, t: 0 },
  scene: {
    xaxis: { title: 'X', range: [-50, 50] },
    yaxis: { title: 'Y', range: [-50, 50] },
    zaxis: { title: 'Z', range: [-50, 50] },
    aspectmode: 'cube', // Fixed aspect mode for balanced view.
  },
  paper_bgcolor: "rgba(0,0,0,0)",
  plot_bgcolor: "rgba(0,0,0,0)"
};

onMounted(() => {
  if (plotlyContainer.value) {
    // Initial rendering.
    Plotly.newPlot(
      plotlyContainer.value,
      [
        {
          x: props.drones.map(drone => drone.position.x),
          y: props.drones.map(drone => drone.position.y),
          z: props.drones.map(drone => drone.position.z),
          mode: 'markers',
          type: 'scatter3d',
          marker: { size: 4, color: 'rgb(23, 190, 207)' },
        }
      ],
      layout
    );
  }
});

// Watch changes in drone data using JSON.stringify to avoid deep watching continuously.
watch(
  () => JSON.stringify(props.drones),
  () => {
    if (plotlyContainer.value) {
      Plotly.react(
        plotlyContainer.value,
        [
          {
            x: props.drones.map(drone => drone.position.x),
            y: props.drones.map(drone => drone.position.y),
            z: props.drones.map(drone => drone.position.z),
            mode: 'markers',
            type: 'scatter3d',
            marker: { size: 4, color: 'rgb(23, 190, 207)' },
          }
        ],
        layout
      );
    }
  }
);
</script>

<style scoped>
.drone-radar-container {
  position: absolute;
  border: 0px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.drone-radar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  cursor: move;
  user-select: none;
}

.drone-radar-header button {
  background-color: #0056b3;
  color: #fff;
  border: none;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
}

.drone-radar-content {
  width: 100%;
  height: calc(100% - 40px);
  position: relative;
  background-color: #fafafa;
}
</style>
