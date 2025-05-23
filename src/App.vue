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
  <button @click="toggleFullscreen" v-if="!fullscreenState" class="toggle_button">
    Enter Fullscreen
  </button>
  <router-view />
</template>

<style>
.toggle_button {
  background-color: #f7ecd8;
  color: #6f1d77;
}
#app {
  min-height: 100vh;
  background-color: #f7ecd8;
  padding: 0rem !important;
}

body {
  overflow: hidden;
  touch-action: none;
  user-select: none;
}
html,
body {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
</style>
