<template>
  <div id="home-layout">
    <h1 class="title" id="swarming_title">Zwermende</h1>
    <h1 class="title" id="lab_title">Robots</h1>
    <img
      ref="drone_1"
      src="@/assets/drone_svg/drone_flying_shadow_2.svg"
      alt="Drone SVG"
      class="drone-svg"
      id="drone_1"
    />
    <img
      ref="drone_2"
      src="@/assets/drone_svg/drone_flying_shadow_2.svg"
      alt="Drone SVG"
      class="drone-svg"
      id="drone_2"
    />
    <img
      ref="drone_3"
      src="@/assets/drone_svg/drone_flying_shadow_2.svg"
      alt="Drone SVG"
      class="drone-svg"
      id="drone_3"
    />
    <div class="button-container">
      <router-link to="/charades">
        <button class="styled-button">Raad de vorm</button>
      </router-link>
      <router-link to="/draw-your-own-path">
        <button class="styled-button">Teken je eigen pad</button>
      </router-link>
    </div>
  </div>
</template>

<style scoped>
@font-face {
  font-family: mainFont;
  src: url('@/assets/Alkaline_Caps_Heavy.otf');
}
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
  color: #6f1d77;
  font-size: 10.75rem;
  -webkit-text-stroke: 3px #6f1d77;
  font-family: mainFont;
  height: 25dvh;
  z-index: 10;
}

#drone_1 {
  width: 40vh;
  left: 4vw;
  top: 8vh;
}

#drone_2 {
  width: 22vh;
  left: 75vw;
  top: 30vh;
}

#drone_3 {
  width: 25vh;
  left: 60vw;
  top: 5vh;
}

.drone-svg {
  z-index: 0;
  position: absolute; /* Ensures the drone can be moved with left and top */
}
.title {
  color: #6f1d77;
  font-weight: 900;
  font-size: 3.75rem;
  font-family: 'Arial Narrow', Arial, sans-serif;
}

.button-container {
  display: flex;
  gap: 1rem;
  padding-top: 5%;
}

.styled-button {
  position: relative; /* Enables positioning for pseudo-elements */
  background-color: #6f1d77; /* Foreground button color */
  border: 2px solid #6f1d77; /* Border color */
  font-size: 2rem;
  padding-bottom: 5%;
  padding-right: 10%;
  width: 35vw;
  height: 20vh;
  cursor: pointer;
  transition:
    background-color 0.3s,
    color 0.3s;
  border-radius: 30px 0px 30px 0px; /* Rounded corners for the foreground */
  z-index: 5; /* Ensure the foreground is above */
  color: #6f1d77;
}

/* Add the background shape using a pseudo-element */
.styled-button::before {
  content: ''; /* Creates the background element */
  position: absolute;
  top: -12px; /* Offset slightly down */
  left: -15px; /* Offset slightly to the right */
  width: 102%; /* Match the size of the button */
  height: 102%;
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

<script lang="ts">
export default {}
</script>
