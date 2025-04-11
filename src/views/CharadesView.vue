<template>
  <div class="charades-container">
    <button @click="goBack" class="back-button">Terug</button>
    <h1 class="title">Raad de vorm</h1>
    <p class="sub-title">Stem op de vorm die je de drones ziet vliegen</p>
    <div class="countdown-timer">
      <button v-if="!started" @click="startCountdown" class="start-button">Start</button>
      <span v-else>{{ countdown }}</span>
    </div>
    <!-- Use the ShapeButtonGrid Component -->
    <ShapeButtonGrid
      :shapes="currentShapes"
      :selectedButton="selectedButton"
      :isCorrect="isCorrect"
      :showCorrect="showCorrect"
      :clickCounts="votes"
      @select="vote"
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
let showCorrect = false
const message = ref('')
// Track the current group index
const currentGroupIndex = ref(0)
const uiDebug = true

// Countdown timer
const countdown = ref(0)
const countdown_value = 20 // Start countdown from 10
// Store votes for each button
const votes = reactive<number[]>([])
const numDrones = 2 // We have to get this in stead of being hardcoded
const repeatCount = 5 // Repeat the shape path 10 times

// const droneEndpoint = 'http://192.168.1.143:3000/api/drones'
const droneEndpoint = 'http://145.94.180.195:3000/api/drones'
const started = ref(false) // Track if countdown has started

// Intervals
let timer: number | null = null
let positionInterval: number | null = null

const loadNewGroup = () => {
  // Currently we loop through all the groups
  // Loop to the start if at the end of groups
  const group = groups[currentGroupIndex.value]
  currentGroupIndex.value = (currentGroupIndex.value + 1) % groups.length

  // Assuming there are always 4 options, choose a random index to be correct
  correctAnswerIndex.value = Math.floor(Math.random() * 4)
  currentShapes.splice(0)

  group.forEach((shapeName: ShapeName) => {
    currentShapes.push({ ...shapesData[shapeName], name: shapeName })
  })

  console.log('correct one is: ' + currentShapes[correctAnswerIndex.value].name)
  selectedButton.value = -1
  isCorrect.value = false
  message.value = ''
  showCorrect = false

  // Reset votes
  votes.length = 0
  for (let i = 0; i < currentShapes.length; i++) {
    votes.push(0)
  }

  // Reset counter
  countdown.value = countdown_value
  started.value = false

  // Send waiting positions for the drones once
  const waitingPositions = createWaitingPositions(numDrones)

  if (!uiDebug) {
    axios
      .post(droneEndpoint, waitingPositions, { timeout: 2000 })
      .then((response) => {
        console.log('Waiting positions sent:', response)
      })
      .catch((error) => {
        console.error('Error sending waiting positions:', error)
      })
  } else {
    console.log('Debug, but otherwise axios post waiting positions!')
  }
}

const startCountdown = () => {
  // Convert the selected shape's path to {x, y,z} format
  const convertedPath = currentShapes[correctAnswerIndex.value].path.map(
    ([pos_x, pos_y, pos_z]) => ({
      pos_x,
      pos_y,
      pos_z,
    }),
  )

  // Send shape path of the randomly chosen shape
  sendShapePath(convertedPath)

  started.value = true
  countdown.value = countdown_value

  timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      if (timer) clearInterval(timer)
      if (positionInterval) clearInterval(positionInterval) // Kill position sending
      evaluateResults()
    }
  }, 1000)
}

// Helper function for generating intermediate points between two defined points in the shape data
function generateIntermediatePoints(
  droneIndex: number,
  start: { pos_x: number; pos_y: number; pos_z: number },
  end: { pos_x: number; pos_y: number; pos_z: number },
  steps: number,
) {
  const points = []
  for (let i = 1; i < steps; i++) {
    const t = i / steps
    points.push({
      index: droneIndex,
      step: i,
      totalSteps: steps,
      pos_x: start.pos_x + (end.pos_x - start.pos_x) * t,
      pos_y: start.pos_y + (end.pos_y - start.pos_y) * t,
      pos_z: start.pos_z + (end.pos_z - start.pos_z) * t,
    })
  }
  return points
}

// Helper function to create an array of positions
const createDroneArray = (
  updates: { index: number; coordinate: { pos_x: number; pos_y: number; pos_z: number } }[],
) => {
  // Create an initial array
  const dronesArray: { pos_x: number; pos_y: number; pos_z: number }[] = []

  // Update the array based on the provided updates
  updates.forEach(({ index, coordinate }) => {
    // Ensure the array is large enough to accommodate the index
    while (dronesArray.length <= index) {
      dronesArray.push({ pos_x: 0, pos_y: 0, pos_z: 0 }) // Initialize with default coordinates
    }

    // Update the specific index with the coordinate
    dronesArray[index] = coordinate
  })

  return dronesArray
}

// Send 3D shape path to drones in interval (for each drone it's position at the time index it is sent)
const sendShapePath = (path: { pos_x: number; pos_y: number; pos_z: number }[]) => {
  const maxStepSize = 0.5
  const waypoints: { pos_x: number; pos_y: number; pos_z: number }[] = []

  // Generate waypoints for each drone
  const waypointsPerDrone: { pos_x: number; pos_y: number; pos_z: number }[][] = Array.from(
    { length: numDrones },
    () => [],
  )

  // Create the waypoints array for the shape
  for (let i = 0; i < path.length - 1; i++) {
    const start = path[i]
    const end = path[i + 1]

    const distance = Math.sqrt(
      Math.pow(end.pos_x - start.pos_x, 2) +
        Math.pow(end.pos_y - start.pos_y, 2) +
        Math.pow(end.pos_z - start.pos_z, 2),
    )
    const steps = Math.max(1, Math.ceil(distance / maxStepSize))

    waypoints.push(start)
    waypoints.push(...generateIntermediatePoints(1, start, end, steps))
  }

  // if (path.length > 0) {
  //   waypoints.push(path[path.length - 1])
  // }

  const delay = Math.floor(waypoints.length / numDrones) // Delays for each drone in timestamps, its nr of waypoints / nr of drones

  // We need to create for each drone a waiting position. Maybe just
  const waitingPositions = createWaitingPositions(numDrones)

  const maxLength = waypoints.length + (numDrones - 1) * delay + 5

  // Add waitingpositions before and after the shape until it reaches maxLength (to account for the shift)
  for (let i = 0; i < numDrones; i++) {
    const staticLocation = waitingPositions[i]

    // Prepend static location for delay
    waypointsPerDrone[i] = Array(i * delay + 5).fill(staticLocation)

    // Repeat the path multiple times before returning to waiting position
    for (let j = 0; j < repeatCount; j++) {
      waypointsPerDrone[i] = waypointsPerDrone[i].concat(waypoints)
    }

    // Append waiting positions until max_length is reached
    while (waypointsPerDrone[i].length <= maxLength) {
      waypointsPerDrone[i].push(staticLocation)
    }
  }

  let stepIndex = 0
  // Send in an interval the positions of all drones at that timestamp
  positionInterval = setInterval(async () => {
    const updates = waypointsPerDrone.map((waypoints, index) => ({
      index,
      coordinate: waypoints[stepIndex] || waypoints[waypoints.length - 1],
    }))

    const dronesArray = createDroneArray(updates)

    if (!uiDebug) {
      axios
        .post(droneEndpoint, dronesArray, { timeout: 2000 })
        .then((response) => {
          console.log(response)
        })
        .catch((error) => {
          if (error.response) {
            console.log('SERVER ERROR')
            console.log(error.response)
          } else if (error.request) {
            console.log('NETWORK ERROR: ' + error.message)
            console.log(error.request)
            console.log(error.toJSON())
          } else {
            console.log('ERROR', error.message)
          }
        })
    } else {
      console.log("Debug, 'sent' positions: " + dronesArray)
    }
    stepIndex++
  }, 500)
}

const createWaitingPositions = (numDrones: number) => {
  const positions = []
  let pos_x = 1
  let pos_y = -1
  const yIncrement = 0.4
  const yMax = 1
  const xDecrement = 0.4

  // So it places at z = 0.5, and then at x = -1.5, with incrementing y positions. If it overflows, we increment x.
  for (let i = 0; i < numDrones; i++) {
    positions.push({ pos_x, pos_y, pos_z: 0.5 })

    pos_y += yIncrement
    if (pos_y > yMax) {
      pos_y = -1.5 // Reset y
      pos_x -= xDecrement // Move x closer
    }
  }

  return positions
}

const vote = (index: number) => {
  votes[index]++
}

const evaluateResults = () => {
  const maxVotes = Math.max(...votes)
  const topChoices = votes
    .map((count, index) => (count === maxVotes ? index : -1))
    .filter((index) => index !== -1)

  if (topChoices.length > 1) {
    message.value = "It's a tie!"
  } else {
    const chosenIndex = topChoices[0]
    isCorrect.value = chosenIndex === correctAnswerIndex.value
    message.value = isCorrect.value
      ? 'Correct! Nieuwe vorm wordt geladen...'
      : 'Het goede antwoord was: ' +
        currentShapes[correctAnswerIndex.value].name +
        '. Nieuwe vorm wordt geladen...'
  }
  showCorrect = true

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
.countdown-timer {
  position: absolute;
  top: 5vh;
  right: 10vw;
  /* color: #ff99ff; */
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

.start-button {
  background-color: #6f1d77;
  color: #f7ecd8;
  font-size: 1.5rem;
  border: 3px solid #6f1d77;
  padding: 1em 1.5em;
  cursor: pointer;
  border-radius: 10px;
  transition: background-color 0.3s;
  font-family: 'Arial Narrow', Arial, sans-serif;
}
</style>
