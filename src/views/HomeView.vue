<template>
  <div id="home-layout">
    <h1 class="title" id="swarming_title">Swarming</h1>
    <h1 class="title" id="lab_title">Lab</h1>
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

#swarming_title {
  color: #d8f103;
  font-size: 5.75rem;
  -webkit-text-stroke: 3px #6f1d77;
}

.title {
  color: #6f1d77;
  font-weight: 900;
  font-size: 3.75rem;
}

.button-container {
  display: flex;
  gap: 1rem;
  padding-top: 10%;
}

.styled-button {
  position: relative; /* Enables positioning for pseudo-elements */
  background-color: #ff99ff; /* Foreground button color */
  border: 4px solid #6f1d77; /* Border color */
  color: #6f1d77;
  font-size: 1.75rem;
  padding-bottom: 10%;
  padding-right: 10%;
  width: 400px;
  height: 150px;
  cursor: pointer;
  transition:
    background-color 0.3s,
    color 0.3s;
  border-radius: 30px 0px 30px 0px; /* Rounded corners for the foreground */
  z-index: 1; /* Ensure the foreground is above */
}

/* Add the background shape using a pseudo-element */
.styled-button::before {
  content: ''; /* Creates the background element */
  position: absolute;
  top: -12px; /* Offset slightly down */
  left: -12px; /* Offset slightly to the right */
  width: 100%; /* Match the size of the button */
  height: 100%;
  background-color: #f7ecd8; /* Background shape color */
  border: 4px solid #6f1d77;
  border-radius: 30px 0px 30px 0px; /* Match the shape of the button */
  z-index: -1; /* Places the background below the button */
  box-sizing: border-box;
}
.styled-button:hover {
  background-color: #f7ecd8; /* Match button color with background */
  border: 4px solid #6f1d77; /* Border color */
  color: #6f1d77;
}
</style>
