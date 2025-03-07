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

// const droneEndpoint = 'http://192.168.1.143:3000/api/drones'
const droneEndpoint = 'http://145.94.63.16:3000/api/drones'

// Helper function for generating intermediate points between two defined points in the shape data
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

// Helper function to create an array of positions
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

// Send 3D shape path to drones (for each drone it's position at the time index it is sent)
const sendShapePath = (path: { x: number; y: number; z: number }[]) => {
  const maxStepSize = 6
  const waypoints: { x: number; y: number; z: number }[] = []
  const numDrones = 1 // We have to get this in stead of being hardcoded

  // Generate waypoints for each drone
  const waypointsPerDrone: { x: number; y: number; z: number }[][] = Array.from(
    { length: numDrones },
    () => [],
  )

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

  // waypoints is just an array of all the steps each drone needs to take.
  // Now we want to have an array (size of nr of drones) of edited waypoints, all lenght (waypoints + delay * nr drones)
  // We add for each drone, the waypoints (and prepend a static location or something)
  // For each drone an offset of delay * index
  // We can then access for a certain timestamp, for each drone the needed coordinates.
  // So we need to extend the updates array to include each drone and their index and waypoint at that stepindex, in stead of the just one waypoint
  // so maybe for each drone, updates += {index of drone, waypointsPerDrone[index of drone][stepIndex]} (or a more efficient way to code that)
  // Extend waypoints with delays for each drone

  const delay = Math.floor(waypoints.length / numDrones) // Delays for each drone in timestamps, its nr of waypoints / nr of drones

  // We need to create for each drone a waiting position. Maybe just
  const waitingPositions = createWaitingPositions(numDrones)
  const maxLength = waypoints.length + (numDrones - 1) * delay + 5

  for (let i = 0; i < numDrones; i++) {
    const staticLocation = waitingPositions[i]

    // Prepend static location for delay
    waypointsPerDrone[i] = Array(i * delay + 5)
      .fill(staticLocation)
      .concat(waypoints)

    // Append waiting positions until max_length is reached (and then add one more)
    while (waypointsPerDrone[i].length <= maxLength) {
      waypointsPerDrone[i].push(staticLocation)
    }
  }

  let stepIndex = 0
  const intervalId = setInterval(async () => {
    if (stepIndex >= waypointsPerDrone[0].length) {
      clearInterval(intervalId)
      console.log('All waypoints sent!')
      return
    }

    const updates = waypointsPerDrone.map((waypoints, index) => ({
      index,
      coordinate: waypoints[stepIndex] || waypoints[waypoints.length - 1], // Repeat last position if out of range
    }))

    const dronesArray = createDroneArray(updates)

    console.log('dronesArray is : ', dronesArray)

    try {
      // Send data to the endpoint
      await axios.post(droneEndpoint, dronesArray)
      console.log(`Sent waypoint ${stepIndex + 1}/${waypoints.length}:`, dronesArray)
    } catch (error) {
      console.error('Error sending data to drone endpoint:', error)
    }
    console.log('dummy sending drone array: ', dronesArray)

    // axios
    //   .post(droneEndpoint, dronesArray, { timeout: 2000 })
    //   .then((response) => {
    //     console.log(response)
    //   })
    //   .catch((error) => {
    //     if (error.response) {
    //       console.log('SERVER ERROR')
    //       console.log(error.response)
    //     } else if (error.request) {
    //       console.log('NETWORK ERROR: ' + error.message)
    //       console.log(error.request)
    //       console.log(error.toJSON())
    //     } else {
    //       console.log('ERROR', error.message)
    //     }
    //   })

    stepIndex++
  }, 1000)
}

const createWaitingPositions = (numDrones: number) => {
  const positions = []
  let x = 1
  let y = -1
  const yIncrement = 0.4
  const yMax = 1
  const xDecrement = 0.4

  // So it places at z = 0.5, and then at x = -1.5, with incrementing y positions. If it overflows, we increment x.
  for (let i = 0; i < numDrones; i++) {
    positions.push({ x, y, z: 0.5 })

    y += yIncrement
    if (y > yMax) {
      y = -1.5 // Reset y
      x -= xDecrement // Move x closer
    }
  }

  return positions
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
  // correctAnswerIndex.value = 0
  console.log('correct one is: ' + currentShapes[correctAnswerIndex.value].name)
  selectedButton.value = -1
  isCorrect.value = false
  message.value = ''

  // Convert the selected shape's path to {x, y,z} format
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
  setTimeout(loadNewGroup, 2000)
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
