from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initial dummy drones data with extra parameters
drones_data = [
    {
        "id": 1,
        "available": True,
        "batteryLevel": 100,
        "position": {"x": 0.0, "y": 0.0, "z": 0.0},
        "velocity": {"x": 0.0, "y": 0.0, "z": 0.0}
    },
    {
        "id": 2,
        "available": True,
        "batteryLevel": 95,
        "position": {"x": -0.2, "y": 1.2, "z": 0.0},
        "velocity": {"x": 0.1, "y": 0.0, "z": 0.0}
    },
    {
        "id": 3,
        "available": True,
        "batteryLevel": 90,
        "position": {"x": -1.0, "y": -0.5, "z": 0.0},
        "velocity": {"x": 0.0, "y": 0.0, "z": 0.0}
    },
    {
        "id": 4,
        "available": True,
        "batteryLevel": 87,
        "position": {"x": 2.0, "y": 1.1, "z": 0.0},
        "velocity": {"x": 0.0, "y": 0.1, "z": 0.0}
    },
    {
        "id": 5,
        "available": False,
        "batteryLevel": 75,
        "position": {"x": 1.5, "y": -2.0, "z": 0.0},
        "velocity": {"x": 0.2, "y": 0.0, "z": 0.0}
    },
    {
        "id": 6,
        "available": False,
        "batteryLevel": 50,
        "position": {"x": 0.5, "y": 0.5, "z": 0.0},
        "velocity": {"x": -0.1, "y": 0.0, "z": 0.0}
    },
    {
        "id": 7,
        "available": False,
        "batteryLevel": 30,
        "position": {"x": -2.0, "y": 0.0, "z": 0.0},
        "velocity": {"x": 0.0, "y": 0.0, "z": -0.1}
    },
    {
        "id": 8,
        "available": False,
        "batteryLevel": 20,
        "position": {"x": 0.0, "y": -1.0, "z": 0.0},
        "velocity": {"x": 0.0, "y": 0.1, "z": 0.0}
    },
]

lock = threading.Lock()  # Lock to ensure safe data updates


@app.route('/api/drones', methods=['GET'])
def get_drones():
    """Endpoint to retrieve drones data."""
    with lock:
        return jsonify(drones_data), 200


@app.route('/api/drones', methods=['POST'])
def update_drones():
    """Endpoint to update drones data."""
    data = request.get_json()
    print("Received data:", data)
    return jsonify({"message": "Data received successfully!"}), 200


def simulate_drone_unavailability():
    """Simulate drones becoming unavailable or available."""
    while True:
        time.sleep(2)  # Wait for 2 seconds
        with lock:
            # Randomly toggle a drone's availability
            if drones_data:
                drone = drones_data[random.randrange(len(drones_data))]
                drone["available"] = not drone["available"]
                print(f"Drone {drone['id']} availability changed to {drone['available']}.")


def simulate_drone_status_changes():
    """Simulate updates to drone battery, position, and velocity."""
    while True:
        time.sleep(0.5)  # Wait for 5 seconds
        with lock:
            for drone in drones_data:
                # Update battery level
                drone["batteryLevel"] = max(0, drone["batteryLevel"] - random.randint(1, 5))

                # Update position (simulate random movement)
                drone["position"]["x"] += random.uniform(-0.1, 0.1)
                drone["position"]["y"] += random.uniform(-0.1, 0.1)
                drone["position"]["z"] += random.uniform(-0.1, 0.1)

                # Update velocity
                drone["velocity"]["x"] = random.uniform(-0.2, 0.2)
                drone["velocity"]["y"] = random.uniform(-0.2, 0.2)
                drone["velocity"]["z"] = random.uniform(-0.2, 0.2)

                print(f"Updated Drone {drone['id']}: {drone}")


def simulate_drone_removal():
    """Simulate removal of drones from the pool."""
    while True:
        time.sleep(10)
        with lock:
            if drones_data:
                removed_drone = drones_data.pop(0)  # Remove the first drone in the list
                print(f"Drone {removed_drone['id']} was removed from the pool.")


# Start the background threads
threading.Thread(target=simulate_drone_unavailability, daemon=True).start()
threading.Thread(target=simulate_drone_status_changes, daemon=True).start()
# threading.Thread(target=simulate_drone_removal, daemon=True).start()  # Optional: Simulate drone removal


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)  # Allows access from other devices in the same network
