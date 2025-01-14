<template>
  <div id="home-layout">
    <h1 class="title">Swarming</h1>
    <h1 class="title">Lab</h1>
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
  background-color: #f7ecd8;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  min-height: 100vh; /* Ensures the background color fills the viewport */
  min-width: 100vw;
  justify-content: center;
}
.title {
  color: #6f1d77;
  font-size: 3.75rem;
}

.button-container {
  display: flex;
  gap: 1rem;
  padding-top: 10%;
}

.styled-button {
  background-color: #f7ecd8; /* Match button color with background */
  border: 4px solid #6f1d77; /* Border color */
  color: #6f1d77;
  font-size: 1.75rem;
  padding: 0.75rem 1.5rem;
  width: 400px;
  height: 150px;
  cursor: pointer;
  transition:
    background-color 0.3s,
    color 0.3s;

  border-radius: 30px 0px 30px 0px;
}

.styled-button:hover {
  background-color: #f7ecd8; /* Match button color with background */
  border: 2px solid #6f1d77; /* Border color */
  color: #6f1d77;
}
</style>
