from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initial dummy drones data with extra parameters
drones_data = {
    1: {
        "bat_level": 100,
        "pos_x": 0.0, "pos_y": 0.0, "pos_z": 0.0,
        "vel_x": 0.0, "vel_y": 0.0, "vel_z": 0.0
    },
    2: {
        "bat_level": 95,
        "pos_x": -0.2, "pos_y": 1.2, "pos_z": 0.0,
        "vel_x": 0.1, "vel_y": 0.0, "vel_z": 0.0
    },
    3: {
        "bat_level": 90,
        "pos_x": -1.0, "pos_y": -0.5, "pos_z": 0.0,
        "vel_x": 0.0, "vel_y": 0.0, "vel_z": 0.0
    },
    4: {
        "bat_level": 87,
        "pos_x": 2.0, "pos_y": 1.1, "pos_z": 0.0,
        "vel_x": 0.0, "vel_y": 0.1, "vel_z": 0.0
    },
    5: {
        "bat_level": 75,
        "pos_x": 1.5, "pos_y": -2.0, "pos_z": 0.0,
        "vel_x": 0.2, "vel_y": 0.0, "vel_z": 0.0
    },
    6: {
        "bat_level": 50,
        "pos_x": 0.5, "pos_y": 0.5, "pos_z": 0.0,
        "vel_x": -0.1, "vel_y": 0.0, "vel_z": 0.0
    },

    7: {
        "bat_level": 75,
        "pos_x": 1.5, "pos_y": -2.0, "pos_z": 0.0,
        "vel_x": 0.2, "vel_y": 0.0, "vel_z": 0.0
    },
    8: {
        "bat_level": 50,
        "pos_x": 0.5, "pos_y": 0.5, "pos_z": 0.0,
        "vel_x": -0.1, "vel_y": 0.0, "vel_z": 0.0
    },


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


@app.route('/api/drones', methods=['GET'])
def get_drones():
    """Endpoint to retrieve drones data."""
    with lock:
        return jsonify(drones_data), 200

@app.route('/api/drones', methods=['POST'])
def update_drones():
    data = request.get_json()
    with lock:
        for drone_id, drone_data in data.items():
            if drone_id in drones_data:
                drones_data[drone_id].update(drone_data)
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
    while True:
        time.sleep(0.1)
        with lock:
            for drone in drones_data.values():
                drone["bat_level"] = max(0, drone["bat_level"] - random.randint(0, 1))
                drone["pos_x"] += random.uniform(-1, 1)
                drone["pos_y"] += random.uniform(-1, 1)
                drone["pos_z"] += random.uniform(-1, 1)
                drone["vel_x"] = random.uniform(-0.2, 0.2)
                drone["vel_y"] = random.uniform(-0.2, 0.2)
                drone["vel_z"] = random.uniform(-0.2, 0.2)

# threading.Thread(target=simulate_drone_status_changes, daemon=True).start()

# Start the background threads
# threading.Thread(target=simulate_drone_unavailability, daemon=True).start()
threading.Thread(target=simulate_drone_status_changes, daemon=True).start()
# threading.Thread(target=simulate_drone_removal, daemon=True).start()  # Optional: Simulate drone removal


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)  # Allows access from other devices in the same network
