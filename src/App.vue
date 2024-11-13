<script setup lang="ts">
//import { RouterView } from 'vue-router'
//import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <router-view />
</template>

<style scoped>
/* Header styles */
/* header {
  text-align: center;
  margin-bottom: 2rem;
  line-height: 1.5;
  max-height: 100vh;
} */

/* Button container styling */
#app {
  text-align: center;
  margin-left: auto;
  margin-right: auto;
  display: flex !important; /* Force flex layout */
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.button-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* Button styling */
.styled-button {
  background-color: white;
  border: 2px solid black;
  color: black;
  font-size: 1.25rem;
  padding: 0.75rem 1.5rem;
  width: 400px; /* Ensures both buttons are the same width */
  height: 150px;
  cursor: pointer;
  transition:
    background-color 0.3s,
    color 0.3s;
}

.styled-button:hover {
  background-color: black;
  color: white;
}

/* Additional layout styling for large screens */
@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;
    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
