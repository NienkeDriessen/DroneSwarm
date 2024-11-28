<template>
  <div class="charades-container">
    <button @click="goBack" class="back-button">Back</button>
    <h1>Charades Game</h1>
    <p>Guess the correct shape!</p>

    <!-- Use the ShapeButtonGrid Component -->
    <ShapeButtonGrid
      :shapes="currentShapes"
      :selectedButton="selectedButton"
      :isCorrect="isCorrect"
      @select="checkAnswer"
    />

    <p v-if="message">{{ message }}</p>
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

const droneEndpoint = 'http://127.0.0.1:3000/api/drones' // Replace with actual endpoint

// Helper function for generating intermediate points
function generateIntermediatePoints(
  start: { x: number; y: number },
  end: { x: number; y: number },
  steps: number,
) {
  const points = []
  for (let i = 1; i < steps; i++) {
    const t = i / steps
    points.push({
      x: start.x + (end.x - start.x) * t,
      y: start.y + (end.y - start.y) * t,
    })
  }
  return points
}

// Helper function to create a 20-item array (one index per drone)
const createDroneArray = (updates: { index: number; coordinate: { x: number; y: number } }[]) => {
  // Create an initial array with 20 `null` values
  const dronesArray = Array(20).fill(null)

  // Update the array based on the provided updates
  updates.forEach(({ index, coordinate }) => {
    if (index >= 0 && index < dronesArray.length) {
      dronesArray[index] = coordinate
    } else {
      console.warn(`Index ${index} is out of bounds. Skipping update.`)
    }
  })

  return dronesArray
}

const sendShapePath = (path: { x: number; y: number }[]) => {
  const maxStepSize = 0.2 // Adjust step size for smoothness
  const waypoints: { x: number; y: number }[] = []

  for (let i = 0; i < path.length - 1; i++) {
    const start = path[i]
    const end = path[i + 1]

    const distance = Math.sqrt(Math.pow(end.x - start.x, 2) + Math.pow(end.y - start.y, 2))
    const steps = Math.max(1, Math.ceil(distance / maxStepSize)) // At least 1 step

    waypoints.push(start)
    waypoints.push(...generateIntermediatePoints(start, end, steps))
  }

  if (path.length > 0) {
    waypoints.push(path[path.length - 1])
  }

  console.log('Sending smoothed shape path to drones:', waypoints)

  let stepIndex = 0
  const intervalId = setInterval(async () => {
    if (stepIndex >= waypoints.length) {
      clearInterval(intervalId)
      console.log('All waypoints sent!')
      return
    }

    const currentWaypoint = waypoints[stepIndex]

    const updates = [
      { index: 0, coordinate: currentWaypoint }, // Drone 0 gets the current waypoint
    ]

    const dronesArray = createDroneArray(updates)

    try {
      // Send data to the endpoint
      await axios.post(droneEndpoint, dronesArray)
      console.log(`Sent waypoint ${stepIndex + 1}/${waypoints.length}:`, dronesArray)
    } catch (error) {
      console.error('Error sending data to drone endpoint:', error)
    }

    stepIndex++
  }, 1000) // Send a coordinate every second
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
  console.log('correct one is: ' + currentShapes[correctAnswerIndex.value].name)
  selectedButton.value = -1
  isCorrect.value = false
  message.value = ''

  // Convert the selected shape's path to {x, y} format
  const convertedPath = currentShapes[correctAnswerIndex.value].path.map(([x, y]) => ({ x, y }))

  // Send shape path of the randomly chosen shape
  sendShapePath(convertedPath)
}

const checkAnswer = (index: number) => {
  selectedButton.value = index
  isCorrect.value = index === correctAnswerIndex.value

  message.value = isCorrect.value
    ? 'Correct! Loading next group...'
    : 'Wrong! the correct answer was: ' +
      currentShapes[correctAnswerIndex.value].name +
      '. Try again with the next group.'

  // Here we might have to wait until drones are in new position?
  setTimeout(loadNewGroup, 2000)
}

onMounted(() => loadNewGroup())

const router = useRouter()
const goBack = () => router.back()
</script>

<style scoped>
.charades-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1rem;
  padding: 1rem;
}

.back-button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
  background-color: #ffffff;
  color: #000;
  border: 2px solid black;
  border-radius: 4px;
  align-self: flex-start;
}
</style>
