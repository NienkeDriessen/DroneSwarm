<script setup lang="ts">
//import { RouterView } from 'vue-router'
//import HelloWorld from './components/HelloWorld.vue'
document.documentElement.requestFullscreen()
</script>

<template>
  <router-view />
</template>

<style>
/* Reset margin and padding for the entire page */
html,
body {
  margin: 0;
  padding: 0;
  box-sizing: border-box; /* Ensure consistent box-sizing for all elements */
}

/* Optional: Ensure the app takes up the full height of the viewport */
#app {
  min-height: 100vh;
  background-color: #f7ecd8; /* Matches your HomeView background */
  padding: 0rem !important;
}
/*If we want the screen locked uncomment this! */
/*
body {
  overflow: hidden;
  touch-action: none;
  user-select: none;
} */
meta[name='viewport'] {
  content: 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no';
}
</style>
