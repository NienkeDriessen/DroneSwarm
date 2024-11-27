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
</script>

<style scoped>
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
</style>
