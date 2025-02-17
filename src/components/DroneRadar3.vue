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
      <!-- Custom 3D scatter plot rendered with Three.js -->
      <div ref="threeContainer" style="width: 100%; height: 100%; position: relative;"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, onMounted, watch } from 'vue';
import Drone from '../models/Drone';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { CSS2DRenderer, CSS2DObject } from 'three/examples/jsm/renderers/CSS2DRenderer.js';

const props = defineProps<{
  drones: Drone[];
}>();

// Window controls
const isMinimized = ref(false);
const position = ref({ top: '50px', left: '50px' });
const containerSize = ref({ width: '500px', height: '500px' });

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

// Three.js scene setup
const threeContainer = ref<HTMLElement | null>(null);
let scene: THREE.Scene;
let camera: THREE.PerspectiveCamera;
let renderer: THREE.WebGLRenderer;
let labelRenderer: CSS2DRenderer;
let controls: OrbitControls;
let scatterPoints: THREE.Points;

function createAxisLabel(text: string, pos: THREE.Vector3): CSS2DObject {
  const div = document.createElement('div');
  div.className = 'axis-label';
  div.textContent = text;
  const label = new CSS2DObject(div);
  label.position.copy(pos);
  return label;
}

function createScatterGeometry(): THREE.BufferGeometry {
  const geometry = new THREE.BufferGeometry();
  const positions: number[] = [];
  props.drones.forEach((drone) => {
    positions.push(drone.position.x, drone.position.y, drone.position.z);
  });
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  return geometry;
}

onMounted(() => {
  if (threeContainer.value) {
    // Scene & Camera
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, threeContainer.value.clientWidth / threeContainer.value.clientHeight, 0.1, 1000);
    camera.position.set(0, 0, 100);

    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(threeContainer.value.clientWidth, threeContainer.value.clientHeight);
    threeContainer.value.appendChild(renderer.domElement);

    // Label Renderer for axis labels
    labelRenderer = new CSS2DRenderer();
    labelRenderer.setSize(threeContainer.value.clientWidth, threeContainer.value.clientHeight);
    labelRenderer.domElement.style.position = 'absolute';
    labelRenderer.domElement.style.top = '0px';
    threeContainer.value.appendChild(labelRenderer.domElement);

    // Controls for rotation, not forcing a fixed rotation
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    // Axes helper and custom axis labels (fixed axis extents)
    const axesLength = 50;
    const axesHelper = new THREE.AxesHelper(axesLength);
    scene.add(axesHelper);
    scene.add(createAxisLabel('X', new THREE.Vector3(axesLength + 5, 0, 0)));
    scene.add(createAxisLabel('Y', new THREE.Vector3(0, axesLength + 5, 0)));
    scene.add(createAxisLabel('Z', new THREE.Vector3(0, 0, axesLength + 5)));

    // Scatter points
    const geometry = createScatterGeometry();
    const material = new THREE.PointsMaterial({ color: 0x17BECB, size: 2 });
    scatterPoints = new THREE.Points(geometry, material);
    scene.add(scatterPoints);

    // Animation loop
    function animate() {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
      labelRenderer.render(scene, camera);
    }
    animate();
  }
});

// Update scatter points when drone data changes
watch(
  () => JSON.stringify(props.drones),
  () => {
    if (scene && scatterPoints) {
      const positions: number[] = [];
      props.drones.forEach((drone) => {
        positions.push(drone.position.x, drone.position.y, drone.position.z);
      });
      scatterPoints.geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
      scatterPoints.geometry.attributes.position.needsUpdate = true;
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
/* Axis label styles */
.axis-label {
  font-size: 12px;
  color: #000;
  background: rgba(255,255,255,0.7);
  padding: 2px 4px;
  border-radius: 3px;
}
</style>
