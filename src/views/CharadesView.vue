<template>
  <div class="charades-container">
    <button @click="goBack" class="back-button">Back</button>
    <h1>Charades Game</h1>
    <p>Guess the correct shape!</p>

    <!-- Buttons Grid -->
    <div class="button-grid">
      <button
        v-for="(shape, index) in currentShapes"
        :key="index"
        @click="checkAnswer(index)"
        :class="[
          'shape-button',
          {
            correct: isCorrect && selectedButton === index,
            wrong: !isCorrect && selectedButton === index,
          },
        ]"
      >
        {{ shape.name }}
      </button>
    </div>

    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'

// Mock data for groups and shapes (we specify it's a ShapeName array)
const groups: ShapeName[][] = [
  ['line', 'triangle', 'circle', 'square'], // Group 1
  // We can add more groups later, just make sure to add new shapes to shape data as well
]

// For indexing the shapes by strings
type ShapeName = 'line' | 'triangle' | 'circle' | 'square'
// This tells TypeScript that shapesData is an object where the keys are of type ShapeName and the values are of the specified structure.
const shapesData: Record<ShapeName, { image: string; path: number[][] }> = {
  line: {
    image: 'path/to/line_image.png',
    path: [
      [0, 0, 0],
      [1, 0, 0],
      [2, 0, 0],
    ],
  },
  triangle: {
    image: 'path/to/triangle_image.png',
    path: [
      [0, 0, 0],
      [1, 1, 0],
      [2, 0, 0],
      [0, 0, 0],
    ],
  },
  circle: {
    image: 'path/to/circle_image.png',
    path: [
      [0, 1, 0],
      [0.71, 0.71, 0],
      [1, 0, 0],
      [0.71, -0.71, 0],
      [0, -1, 0],
      [-0.71, -0.71, 0],
      [-1, 0, 0],
      [-0.71, 0.71, 0],
      [0, 1, 0],
    ],
  },
  square: {
    image: 'path/to/square_image.png',
    path: [
      [0, 0, 0],
      [0, 1, 0],
      [1, 1, 0],
      [1, 0, 0],
      [0, 0, 0],
    ],
  },
}

const currentShapes = reactive([] as { name: string; image: string; path: number[][] }[])
const selectedButton = ref(-1)
const correctAnswerIndex = ref(0)
const isCorrect = ref(false)
const message = ref('')

// Dummy function to send shape path to drones
const sendShapePath = (path: number[][]) => {
  console.log('Sending shape path to drones:', path)
}

// Load a random group and set up the game
const loadNewGroup = () => {
  // Pick a random group
  const randomGroup = groups[Math.floor(Math.random() * groups.length)]

  // Set current shapes
  currentShapes.length = 0
  randomGroup.forEach((shapeName: ShapeName) => {
    currentShapes.push({ ...shapesData[shapeName], name: shapeName })
  })

  // Always choose the first shape as the correct answer for now
  correctAnswerIndex.value = 0
  selectedButton.value = -1
  isCorrect.value = false
  message.value = ''

  // Send the first shape's path to the drones
  sendShapePath(currentShapes[0].path)
}

// Handle button click and check answer
const checkAnswer = (index: number) => {
  selectedButton.value = index
  isCorrect.value = index === correctAnswerIndex.value

  if (isCorrect.value) {
    message.value = 'Correct! Loading next group...'
  } else {
    message.value = 'Wrong! Try again with the next group.'
  }

  // Load new group after a short delay
  setTimeout(loadNewGroup, 2000)
}

// Initialize game on page load
onMounted(() => {
  loadNewGroup()
})

// Go back function to navigate to the previous page
const router = useRouter()
const goBack = () => {
  router.back()
}
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

.button-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  width: 100%;
  max-width: 800px;
}

.shape-button {
  padding-top: 5rem;
  padding-bottom: 5rem;
  padding-left: 7rem;
  padding-right: 7rem;
  font-size: 1.2rem;
  border: 2px solid #000;
  border-radius: 8px;
  background-color: #f0f0f0;
  cursor: pointer;
  transition:
    background-color 0.3s,
    transform 0.2s;
}

.shape-button.correct {
  background-color: #4caf50;
  color: white;
}

.shape-button.wrong {
  background-color: #f44336;
  color: white;
}

.shape-button:hover {
  transform: scale(1.05);
}
</style>
