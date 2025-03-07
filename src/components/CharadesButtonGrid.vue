<template>
  <div class="button-grid">
    <button
      v-for="(shape, index) in shapes"
      :key="index"
      @click="$emit('select', index)"
      :class="[
        'shape-button',
        {
          correct: isCorrect && selectedButton === index,
          wrong: !isCorrect && selectedButton === index,
        },
      ]"
    >
      {{ shape.name }}
      <img :src="shape.image" alt="Button icon" class="button_icon" id="icon" />
    </button>
  </div>
</template>

<script setup lang="ts">
type Shape = {
  name: string
  image: string
  path: number[][]
}

// Define props with proper typing
defineProps({
  shapes: Array as () => Shape[],
  selectedButton: Number,
  isCorrect: Boolean,
})

// Define the event emitted
defineEmits(['select'])

// const getIconPath = (path: string) => {
//   return new URL(`${path}`, import.meta.url).href
// }
</script>

<style scoped>
.button_icon {
  width: 40%;
}

.button-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  width: 100%;
  max-width: 800px;
}

.shape-button {
  position: relative; /* Enables positioning for pseudo-elements */
  background-color: #6f1d77; /* Foreground button color */
  border: 4px solid #6f1d77; /* Border color */
  color: #6f1d77;
  font-size: 2rem;
  font-family: 'Arial Narrow', Arial, sans-serif;
  padding-bottom: 10%;
  padding-right: 10%;
  margin: 1vh;
  width: 35vw;
  height: 25vh;
  cursor: pointer;
  transition:
    background-color 0.3s,
    color 0.3s;
  border-radius: 30px 0px 30px 0px; /* Rounded corners for the foreground */
  z-index: 5; /* Ensure the foreground is above */
}

/* Add the background shape using a pseudo-element */
.shape-button::before {
  content: ''; /* Creates the background element */
  position: absolute;
  top: -14px; /* Offset slightly down */
  left: -20px; /* Offset slightly to the right */
  width: 103%; /* Match the size of the button */
  height: 103%;
  background-color: #f7ecd8; /* Background shape color */
  border: 4px solid #6f1d77;
  border-radius: 30px 0px 30px 0px; /* Match the shape of the button */
  z-index: -1; /* Places the background below the button */
  box-sizing: border-box;
}

.shape-button.correct::before {
  background-color: #009b77;
}
.shape-button.correct {
  color: #f7ecd8;
}

.shape-button.wrong::before {
  background-color: #a40034;
}

.shape-button.wrong {
  color: #f7ecd8;
}
</style>
