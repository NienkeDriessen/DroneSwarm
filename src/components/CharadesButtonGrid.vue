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
      <a class="count_nr">{{ clickCounts ? clickCounts[index] : '' }}</a>
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
  showCorrect: Boolean,
  clickCounts: Array as () => number[],
})

// Define the event emitted
defineEmits(['select'])
</script>

<style scoped>
.button_icon {
  width: 40%;
  padding-left: 10%;
}

.button-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  width: 100%;
  max-width: 800px;
}

.shape-button {
  position: relative;
  background-color: #6f1d77;
  border: 4px solid #6f1d77;
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
  border-radius: 30px 0px 30px 0px;
  z-index: 5;
}

@keyframes flash {
  0% {
    background-color: #ffe5ff;
    border-color: #d8f103;
  }
  50% {
    background-color: #ff99ff; /* Flash color */
    border-color: rgb(242, 34, 194); /* Flash border color */
  }
  100% {
    background-color: #3da5ff;
    border-color: #ffb404;
  }
}

/* Add the background shape using a pseudo-element */
.shape-button::before {
  content: '';
  position: absolute;
  top: -14px;
  left: -20px;
  width: 103%;
  height: 103%;
  background-color: #f7ecd8;
  border: 4px solid #6f1d77;
  border-radius: 30px 0px 30px 0px;
  z-index: -1;
  box-sizing: border-box;
  transition: 0.1s ease-out;
}
/* Effect when the button is clicked (active state) */
.shape-button:active::before {
  top: -2%; /* Moves the top part down */
  left: -2%;
  transition: 0.1s ease-in-out; /* Smooth animation */
}

.shape-button.correct::before {
  background-color: #009b77;
}
.shape-button.correct {
  color: #f7ecd8;
}

.shape-button:focus {
  -webkit-tap-highlight-color: transparent;
}

.shape-button.wrong::before {
  background-color: #a40034;
}

.shape-button.wrong {
  color: #f7ecd8;
}

.count_nr {
  position: absolute;
  right: 6%;
  top: 60%;
  color: #ff99ff;
  font-weight: 1000;
  font-size: 2.75rem;
}
</style>
