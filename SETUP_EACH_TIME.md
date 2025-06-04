# 📄 Demo Setup Instructions

Follow these steps **each time you set up at a presentation location**.

---

## First, on the Laptop, while being charged:

__Make sure the laptop is charged__

### 1. Turn On the Wi-Fi Router

- Plug in and turn on the Wi-Fi router.
- Wait a few seconds for it to start broadcasting.

---

### 2. Connect Laptop to Router

- Connect the laptop to one of the following Wi-Fi networks (doesn't matter which one):
  - Linksys00023
  - Linksys00023_5GHz
- Either the network is recognised, or use the password on the back. You can also press the WPS button on the router to connect automatically.

### 3. Start the Frontend App

Open a terminal by selecting the following icon on the left toolbar:

<img src="src\assets\terminal_image.png" alt="alt text" width="75"/>

In the terminal, paste the below command by right clicking and selecting paste (ctrl+v does not work), or just type it to navigate to the main command's directory

```bash
cd Desktop/
```

Then in the terminal again, paste/type this below to run the app

```bash
./run_app.sh
```

This will start the application and now we can connect the tablet.

## Tablet:
__Make sure the tablet charged__

### 4. Connect the Tablet


After turning on the tablet, connect it to the same Wi-Fi network as the laptop.

On the homescreen, tap the **"drone demo app"** icon.

Tap the **"fullscreen"** button to make it screen filling.

## Laptop, drone software side:

### 6. Start the Drone Application (if not already started)

Start up the drone application like normal

Click in the interface on SC-Demo
The drones will now listen for instructions from the app!

## **Now everything should be good to go!**



# Shutdown

Press Ctrl + C in the terminal(s) to stop all processes.

Power off the router and pack up.

Switch off both the tablet and the laptop.Set them to charge, so that it is ready to be used for the next time! :)

---

## Some bugs that can occur and how to fix them:

- **Sometimes the icons dissappear on the tablet.**
  On the laptop, go to the terminal in which you started the frontend (which you started with _npm run dev -- --host_). If you type _'r'_ and press enter the server reloads, and the images should be back!

![alt text](src\assets\bug_image.png)
