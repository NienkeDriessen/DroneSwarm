<template>
  <div class="charades-container">
    <button @click="goBack" class="back-button">Back</button>
    <h1 class="title">Charades Game</h1>
    <p class="sub-title">Guess the correct shape!</p>

    <!-- Use the ShapeButtonGrid Component -->
    <ShapeButtonGrid
      :shapes="currentShapes"
      :selectedButton="selectedButton"
      :isCorrect="isCorrect"
      @select="checkAnswer"
    />

    <p class="sub-title" v-if="message">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { groups, shapesData, type ShapeName } from '../assets/shapesData'
import ShapeButtonGrid from '../components/CharadesButtonGrid.vue'
import axios from 'axios'

// Define the shape type explicitly
type Shape = {
  name: ShapeName
  image: string
  path: number[][]
}

const currentShapes = reactive<Shape[]>([])
const selectedButton = ref(-1)
const correctAnswerIndex = ref(0)
const isCorrect = ref(false)
const message = ref('')
// Track the current group index
const currentGroupIndex = ref(0)

const droneEndpoint = 'http://145.94.137.97:3000/api/drones'
//const droneEndpoint = 'http://145.94.177.54:3000/api/drones'

// Helper function for generating intermediate points
function generateIntermediatePoints(
  droneIndex: number,
  start: { x: number; y: number; z: number },
  end: { x: number; y: number; z: number },
  steps: number,
) {
  const points = []
  for (let i = 1; i < steps; i++) {
    const t = i / steps
    points.push({
      index: droneIndex,
      step: i,
      totalSteps: steps,
      x: start.x + (end.x - start.x) * t,
      y: start.y + (end.y - start.y) * t,
      z: start.z + (end.z - start.z) * t,
    })
  }
  return points
}

// Helper function to create an array
const createDroneArray = (
  updates: { index: number; coordinate: { x: number; y: number; z: number } }[],
) => {
  // Create an initial array
  const dronesArray: { x: number; y: number; z: number }[] = []

  // Update the array based on the provided updates
  updates.forEach(({ index, coordinate }) => {
    // Ensure the array is large enough to accommodate the index
    while (dronesArray.length <= index) {
      dronesArray.push({ x: 0, y: 0, z: 0 }) // Initialize with default coordinates
    }

    // Update the specific index with the coordinate
    dronesArray[index] = coordinate
  })

  return dronesArray
}

// Send 3D shape path to drones
const sendShapePath = (path: { x: number; y: number; z: number }[]) => {
  const maxStepSize = 0.2
  const waypoints: { x: number; y: number; z: number }[] = []

  for (let i = 0; i < path.length - 1; i++) {
    const start = path[i]
    const end = path[i + 1]

    const distance = Math.sqrt(
      Math.pow(end.x - start.x, 2) + Math.pow(end.y - start.y, 2) + Math.pow(end.z - start.z, 2),
    )
    const steps = Math.max(1, Math.ceil(distance / maxStepSize))

    waypoints.push(start)
    waypoints.push(...generateIntermediatePoints(1, start, end, steps))
  }

  if (path.length > 0) {
    waypoints.push(path[path.length - 1])
  }

  console.log('Sending smoothed 3D shape path to drones:', waypoints)

  let stepIndex = 0
  const intervalId = setInterval(async () => {
    if (stepIndex >= waypoints.length) {
      clearInterval(intervalId)
      console.log('All waypoints sent!')
      return
    }

    const currentWaypoint = waypoints[stepIndex]

    const updates = [{ index: 0, coordinate: currentWaypoint }]

    const dronesArray = createDroneArray(updates)

    // try {
    //   // Send data to the endpoint
    //   await axios.post(droneEndpoint, dronesArray)
    //   console.log(`Sent waypoint ${stepIndex + 1}/${waypoints.length}:`, dronesArray)
    // } catch (error) {
    //   console.error('Error sending data to drone endpoint:', error)
    // }

    axios
    .post(droneEndpoint, dronesArray, { timeout: 2000 })
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        if (error.response) {
          console.log("SERVER ERROR");
          console.log(error.response);
        } else if (error.request) {
          console.log("NETWORK ERROR: " + error.message);
          console.log(error.request);
          console.log(error.toJSON());
        } else {
          console.log('ERROR', error.message);
        }
      });

    stepIndex++
  }, 1000)
}

const loadNewGroup = () => {
  // Loop to the start if at the end of groups
  const group = groups[currentGroupIndex.value]
  currentGroupIndex.value = (currentGroupIndex.value + 1) % groups.length

  currentShapes.length = 0
  group.forEach((shapeName: ShapeName) => {
    currentShapes.push({ ...shapesData[shapeName], name: shapeName })
  })

  // Choose a random correct index
  correctAnswerIndex.value = Math.floor(Math.random() * currentShapes.length)
  // For testing purposes just do the first one
  correctAnswerIndex.value = 0
  console.log('correct one is: ' + currentShapes[correctAnswerIndex.value].name)
  selectedButton.value = -1
  isCorrect.value = false
  message.value = ''

  // Convert the selected shape's path to {x, y} format
  const convertedPath = currentShapes[correctAnswerIndex.value].path.map(([x, y, z]) => ({
    x,
    y,
    z,
  }))

  // Send shape path of the randomly chosen shape
  sendShapePath(convertedPath)
}

const checkAnswer = (index: number) => {
  selectedButton.value = index
  isCorrect.value = index === correctAnswerIndex.value

  message.value = isCorrect.value
    ? 'Correct! Loading next group...'
    : 'The correct answer was: ' + currentShapes[correctAnswerIndex.value].name + '. Try again!'

  // Here we might have to wait until drones are in new position?
  setTimeout(loadNewGroup, 4000)
}

onMounted(() => loadNewGroup())

const router = useRouter()
const goBack = () => router.back()
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
}
.charades-container {
  background-color: #f7ecd8;
  min-height: 100vh; /* Ensures the background color fills the viewport */
  min-width: 100vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1rem;
  padding: 1rem;
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
</style>
