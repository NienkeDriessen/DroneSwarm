<script setup lang="ts">
import { ref } from 'vue'
import { api as fullscreen } from 'vue-fullscreen'

const fullscreenState = ref(false)

const toggleFullscreen = () => {
  fullscreen.toggle(document.documentElement, {
    callback: (isFullscreen) => {
      fullscreenState.value = isFullscreen
    },
  })
}
</script>

<template>
  <!-- <button @click="toggleFullscreen">Toggle Fullscreen</button> -->
  <button @click="toggleFullscreen" v-if="!fullscreenState" class="toggle_button">
    Enter Fullscreen
  </button>
  <!-- <div v-if="fullscreenState" class="fullscreen-message">Fullscreen Activated</div> -->
  <router-view />
</template>

<style>
.toggle_button {
  background-color: #f7ecd8;
  color: #6f1d77;
}
#app {
  min-height: 100vh;
  background-color: #f7ecd8; /* Matches your HomeView background */
  padding: 0rem !important;
}
/*If we want the screen locked uncomment this! */

body {
  overflow: hidden;
  touch-action: none;
  user-select: none;
}
/* Add custom styles if needed */
/* Reset margin and padding for the entire page */
html,
body {
  margin: 0;
  padding: 0;
  box-sizing: border-box; /* Ensure consistent box-sizing for all elements */
}
</style>
