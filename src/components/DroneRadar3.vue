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
    <!-- Added touchstart on header for dragging -->
    <div class="drone-radar-header" @mousedown="startDrag" @touchstart="startDrag">
      <span>Drone Radar</span>
      <button @click.stop="toggleMinimize">
        {{ isMinimized ? 'Maximize' : 'Minimise' }}
      </button>
    </div>
    <div class="drone-radar-content" v-show="!isMinimized">
      <div ref="threeContainer" style="width: 100%; height: 100%; position: relative;"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import Drone from '../models/Drone';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { CSS2DRenderer, CSS2DObject } from 'three/examples/jsm/renderers/CSS2DRenderer.js';

const props = defineProps<{ drones: Drone[] }>();

// Window controls
const isMinimized = ref(false);
const position = ref({ top: '50px', left: '50px' });
const containerSize = ref({ width: '500px', height: '500px' });

const toggleMinimize = () => {
  isMinimized.value = !isMinimized.value;
};

// Updated startDrag to support mouse and touch events while preserving clicks on the toggle button.
const startDrag = (event: MouseEvent | TouchEvent) => {
  // Do not initiate drag if a button was clicked.
  const target = event.target as HTMLElement;
  if (target.closest('button')) return;

  event.preventDefault();
  let startX: number, startY: number;
  if ('touches' in event) {
    startX = event.touches[0].clientX;
    startY = event.touches[0].clientY;
  } else {
    startX = event.clientX;
    startY = event.clientY;
  }

  const startTop = parseInt(position.value.top, 10);
  const startLeft = parseInt(position.value.left, 10);

  const onMove = (moveEvent: MouseEvent | TouchEvent) => {
    moveEvent.preventDefault();
    let currentX: number, currentY: number;
    if ('touches' in moveEvent) {
      currentX = moveEvent.touches[0].clientX;
      currentY = moveEvent.touches[0].clientY;
    } else {
      currentX = moveEvent.clientX;
      currentY = moveEvent.clientY;
    }
    requestAnimationFrame(() => {
      position.value = {
        top: `${startTop + (currentY - startY)}px`,
        left: `${startLeft + (currentX - startX)}px`
      };
    });
  };

  const onEnd = () => {
    document.removeEventListener('mousemove', onMove);
    document.removeEventListener('mouseup', onEnd);
    document.removeEventListener('touchmove', onMove);
    document.removeEventListener('touchend', onEnd);
    document.removeEventListener('touchcancel', onEnd);
  };

  document.addEventListener('mousemove', onMove);
  document.addEventListener('mouseup', onEnd);
  document.addEventListener('touchmove', onMove, { passive: false });
  document.addEventListener('touchend', onEnd);
  document.addEventListener('touchcancel', onEnd);
};

// Three.js scene setup and other code remain unchanged
const threeContainer = ref<HTMLElement | null>(null);
let scene: THREE.Scene;
let camera: THREE.PerspectiveCamera;
let renderer: THREE.WebGLRenderer;
let labelRenderer: CSS2DRenderer;
let controls: OrbitControls;
let fixedBoxHelper: THREE.Box3Helper;
let arrowsGroup: THREE.Group;

function createAxisLabel(text: string, pos: THREE.Vector3): CSS2DObject {
  const div = document.createElement('div');
  div.className = 'axis-label';
  div.style.fontSize = '10px';
  div.textContent = text;
  const label = new CSS2DObject(div);
  label.position.copy(pos);
  return label;
}

function updateArrows() {
  while (arrowsGroup.children.length > 0) {
    arrowsGroup.remove(arrowsGroup.children[0]);
  }
  props.drones.forEach(drone => {
    const velocity = new THREE.Vector3(drone.velocity.x, drone.velocity.y, drone.velocity.z);
    const direction = velocity.length() === 0 ? new THREE.Vector3(1, 0, 0) : velocity.normalize();
    const pos = new THREE.Vector3(drone.position.x, drone.position.y, drone.position.z);
    const arrow = new THREE.ArrowHelper(direction, pos, 0.12, 0x00ffff, 0.06, 0.06);
    (arrow.cone.material as THREE.MeshBasicMaterial).transparent = true;
    (arrow.cone.material as THREE.MeshBasicMaterial).opacity = 0.8;
    (arrow.line.material as THREE.LineBasicMaterial).transparent = true;
    (arrow.line.material as THREE.LineBasicMaterial).opacity = 0.8;
    arrowsGroup.add(arrow);
    const sphereGeometry = new THREE.SphereGeometry(0.05, 8, 8);
    const sphereMaterial = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
    sphere.position.copy(pos);
    arrowsGroup.add(sphere);
  });
}

onMounted(() => {
  if (threeContainer.value) {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(
      75,
      threeContainer.value.clientWidth / threeContainer.value.clientHeight,
      0.1,
      1000
    );
    camera.position.set(-4, 1, -2);
    camera.rotation.order = 'YXZ';

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(threeContainer.value.clientWidth, threeContainer.value.clientHeight);
    threeContainer.value.appendChild(renderer.domElement);

    labelRenderer = new CSS2DRenderer();
    labelRenderer.setSize(threeContainer.value.clientWidth, threeContainer.value.clientHeight);
    labelRenderer.domElement.style.position = 'absolute';
    labelRenderer.domElement.style.top = '0px';
    labelRenderer.domElement.style.pointerEvents = 'none';
    threeContainer.value.appendChild(labelRenderer.domElement);

    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    const sceneGroup = new THREE.Group();
    sceneGroup.rotation.x = -Math.PI / 2;
    scene.add(sceneGroup);

    const axesLength = 1;
    const axesHelper = new THREE.AxesHelper(axesLength);
    axesHelper.rotation.set(0, 0, 0);
    sceneGroup.add(axesHelper);
    sceneGroup.add(createAxisLabel('X', new THREE.Vector3(axesLength, 0, 0)));
    sceneGroup.add(createAxisLabel('Y', new THREE.Vector3(0, axesLength, 0)));
    sceneGroup.add(createAxisLabel('Z', new THREE.Vector3(0, 0, axesLength)));

    arrowsGroup = new THREE.Group();
    sceneGroup.add(arrowsGroup);
    updateArrows();

    const domainMin = new THREE.Vector3(-1.95, -1.7, 0);
    const domainMax = new THREE.Vector3(1.45, 1.8, 2.5);
    const box = new THREE.Box3(domainMin, domainMax);
    fixedBoxHelper = new THREE.Box3Helper(box, 0xff0000);
    sceneGroup.add(fixedBoxHelper);

    const corners = [
      new THREE.Vector3(domainMin.x, domainMin.y, domainMin.z),
      new THREE.Vector3(domainMax.x, domainMin.y, domainMin.z),
      new THREE.Vector3(domainMin.x, domainMax.y, domainMin.z),
      new THREE.Vector3(domainMax.x, domainMax.y, domainMin.z),
      new THREE.Vector3(domainMin.x, domainMin.y, domainMax.z),
      new THREE.Vector3(domainMax.x, domainMin.y, domainMax.z),
      new THREE.Vector3(domainMin.x, domainMax.y, domainMax.z),
      new THREE.Vector3(domainMax.x, domainMax.y, domainMax.z)
    ];

    corners.forEach(corner => {
      const labelText = `(${corner.x}, ${corner.y}, ${corner.z})`;
      const label = createAxisLabel(labelText, corner);
      label.position.add(new THREE.Vector3(0.1, 0.1, 0.1));
      sceneGroup.add(label);
    });

    const gridSize = 3.4, divisions = 15, color = 0xff0000, gridOpacity = 0.3;
    const mid = new THREE.Vector3(
      (domainMin.x + domainMax.x) / 2,
      (domainMin.y + domainMax.y) / 2,
      (domainMin.z + domainMax.z) / 2
    );

    const gridXMin = new THREE.GridHelper(gridSize, divisions, color, color);
    gridXMin.material.opacity = gridOpacity;
    gridXMin.material.transparent = true;
    gridXMin.rotation.z = -Math.PI / 2;
    gridXMin.position.set(domainMin.x, mid.y, mid.z);
    sceneGroup.add(gridXMin);

    const gridXMax = new THREE.GridHelper(gridSize, divisions, color, color);
    gridXMax.material.opacity = gridOpacity;
    gridXMax.material.transparent = true;
    gridXMax.rotation.z = -Math.PI / 2;
    gridXMax.position.set(domainMax.x, mid.y, mid.z);
    sceneGroup.add(gridXMax);

    const gridYMin = new THREE.GridHelper(gridSize, divisions, color, color);
    gridYMin.material.opacity = gridOpacity;
    gridYMin.material.transparent = true;
    gridYMin.position.set(mid.x, domainMin.y, mid.z);
    sceneGroup.add(gridYMin);

    const gridYMax = new THREE.GridHelper(gridSize, divisions, color, color);
    gridYMax.material.opacity = gridOpacity;
    gridYMax.material.transparent = true;
    gridYMax.position.set(mid.x, domainMax.y, mid.z);
    sceneGroup.add(gridYMax);

    const gridZMin = new THREE.GridHelper(gridSize, divisions, color, color);
    gridZMin.material.opacity = gridOpacity;
    gridZMin.material.transparent = true;
    gridZMin.rotation.x = -Math.PI / 2;
    gridZMin.position.set(mid.x, mid.y, domainMin.z);
    sceneGroup.add(gridZMin);

    const gridZMax = new THREE.GridHelper(gridSize, divisions, color, color);
    gridZMax.material.opacity = gridOpacity;
    gridZMax.material.transparent = true;
    gridZMax.rotation.x = -Math.PI / 2;
    gridZMax.position.set(mid.x, mid.y, domainMax.z);
    sceneGroup.add(gridZMax);

    function animate() {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
      labelRenderer.render(scene, camera);
    }
    animate();
  }
});

watch(
  () => JSON.stringify(props.drones),
  () => {
    if (arrowsGroup) {
      updateArrows();
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
.axis-label {
  font-size: 12px;
  color: #000;
  background: rgba(255,255,255,0.7);
  padding: 2px 4px;
  border-radius: 3px;
}
</style>
