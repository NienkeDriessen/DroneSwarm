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

const sendShapePath = (path: number[][]) => {
  console.log('Sending shape path to drones:', path)
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

  // Send shape path of the randomly chosen shape
  sendShapePath(currentShapes[correctAnswerIndex.value].path)
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
