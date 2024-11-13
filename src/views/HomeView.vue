<template>
  <div id="home-layout">
    <h1>Swarming Drones</h1>
    <div class="button-container">
      <router-link to="/charades">
        <button class="styled-button">Charades</button>
      </router-link>
      <router-link to="/draw-your-own-path">
        <button class="styled-button">Draw your own path!</button>
      </router-link>
    </div>
  </div>
</template>

<style scoped>
#home-layout {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.button-container {
  display: flex;
  gap: 1rem;
}

.styled-button {
  background-color: white;
  border: 2px solid black;
  color: black;
  font-size: 1.25rem;
  padding: 0.75rem 1.5rem;
  width: 400px;
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
</style>
