from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time
import random
import math

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initial dummy drones data with extra parameters
drones_data = {
    1: {
        "bat_level": 100,
        "pos_x": 0.0, "pos_y": -0.2, "pos_z": 0.03,
        "vel_x": 0.0, "vel_y": 0.0, "vel_z": 0.0
    },
    2: {
        "bat_level": 95,
        "pos_x": -0.2, "pos_y": -0.1, "pos_z": 0.01,
        "vel_x": 0.1, "vel_y": 0.0, "vel_z": 0.0
    },
    3: {
        "bat_level": 90,
        "pos_x": -0.1, "pos_y": -0, "pos_z": 0.02,
        "vel_x": 0.0, "vel_y": 0.0, "vel_z": 0.0
    },
    # 4: {
    #     "bat_level": 87,
    #     "pos_x": 0.3, "pos_y": -0.2, "pos_z": 0.05,
    #     "vel_x": 0.0, "vel_y": 0.1, "vel_z": 0.0
    # },
    # 5: {
    #     "bat_level": 75,
    #     "pos_x": 0.5, "pos_y": -0.5, "pos_z": 0.01,
    #     "vel_x": 0.2, "vel_y": 0.0, "vel_z": 0.0
    # },
    # 6: {
    #     "bat_level": 50,
    #     "pos_x": 0.1, "pos_y": -0.7, "pos_z": 0.0,
    #     "vel_x": -0.1, "vel_y": 0.0, "vel_z": 0.0
    # },

    # 7: {
    #     "bat_level": 75,
    #     "pos_x": 0.04, "pos_y": -0.6, "pos_z": 0.0,
    #     "vel_x": 0.2, "vel_y": 0.0, "vel_z": 0.0
    # },
    # 8: {
    #     "bat_level": 50,
    #     "pos_x": -0.05, "pos_y": -0.6, "pos_z": 0.0,
    #     "vel_x": -0.1, "vel_y": 0.0, "vel_z": 0.0
    # },


}
    # {
    #     "id": 7,
    #     "available": False,
    #     "batteryLevel": 30,
    #     "position": {"x": -2.0, "y": 0.0, "z": 0.0},
    #     "velocity": {"x": 0.0, "y": 0.0, "z": -0.1}
    # },
    # {
    #     "id": 8,
    #     "available": False,
    #     "batteryLevel": 20,
    #     "position": {"x": 0.0, "y": -1.0, "z": 0.0},
    #     "velocity": {"x": 0.0, "y": 0.1, "z": 0.0}
    # },

lock = threading.Lock()  # Lock to ensure safe data updates

# Global time variable for simulation.
global_time = 0.0

@app.route('/api/drones', methods=['GET'])
def get_drones():
    """Endpoint to retrieve drones data."""
    with lock:
        return jsonify(drones_data), 200

@app.route('/api/drones', methods=['POST'])
def update_drones():
    data = request.get_json()
    print("data:", data)
    with lock:
        # Iterate through the list of updates
        for update in data:
            drone_id = update.get('drone_id')
            # Ensure the drone_id exists in our dataset.
            if drone_id in drones_data:
                # Update only the allowed fields if present.
                for key in ['pos_x', 'pos_y', 'pos_z', 'vel_x', 'vel_y', 'vel_z']:
                    if key in update:
                        drones_data[drone_id][key] = update[key]
    return jsonify({"message": "Data updated successfully!"}), 200

def simulate_drone_removal():
    """Simulate removal of drones from the pool."""
    while True:
        time.sleep(10)
        with lock:
            if drones_data:
                removed_drone = drones_data.pop(0)  # Remove the first drone in the list
                print(f"Drone {removed_drone['id']} was removed from the pool.")


def simulate_drone_status_changes():
    global global_time
    spiral_vy = 0.1   # Constant upward velocity in y-direction.
    delta = 0.01        # Time step in seconds.
    while True:
        time.sleep(delta)
        global_time += delta
        with lock:
            for drone in drones_data.values():
                # If base values and phase are not set, initialize them.
                if "base_x" not in drone:
                    drone["base_x"] = drone["pos_x"]
                    drone["base_y"] = drone["pos_y"]
                    drone["base_z"] = drone["pos_z"]
                    drone["phase"] = random.uniform(0, 2 * math.pi)
                    drone["amplitude"] = 0.8 + random.uniform(-0.03, 0.03)
                # Update positions based on a spiral trajectory.
                drone["pos_x"] = drone["base_x"] + drone["amplitude"] * math.cos(global_time + drone["phase"])
                drone["pos_zy"] = drone["base_y"] + drone["amplitude"] * math.sin(global_time + drone["phase"])
                drone["pos_z"] = drone["base_z"] + spiral_vy * global_time
                # Update velocity arbitrarily.
                drone["vel_x"] = random.uniform(-0.2, 0.2)
                drone["vel_y"] = random.uniform(-0.2, 0.2)
                drone["vel_z"] = random.uniform(-0.2, 0.2)
                # Decrease battery level gradually.
                drone["bat_level"] = max(0, drone["bat_level"] - random.randint(0, 1))

# threading.Thread(target=simulate_drone_status_changes, daemon=True).start()

# Start the background threads
# threading.Thread(target=simulate_drone_unavailability, daemon=True).start()
# threading.Thread(target=simulate_drone_status_changes, daemon=True).start()
# threading.Thread(target=simulate_drone_removal, daemon=True).start()  # Optional: Simulate drone removal


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)  # Allows access from other devices in the same network
