from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initial dummy drones data
drones_data = [
    {"id": 1, "available": True},
    {"id": 2, "available": True},
    {"id": 3, "available": True},
    {"id": 4, "available": True},
    {"id": 5, "available": False},
    {"id": 6, "available": False},
    {"id": 7, "available": False},
    {"id": 8, "available": False},
]

lock = threading.Lock()  # lock to ensure safe data updates


@app.route('/api/drones', methods=['GET'])
def get_drones():
    """Endpoint to retrieve drones data."""
    with lock:
        return jsonify(drones_data), 200
    
@app.route('/api/drones', methods=['POST'])
def drones():
    data = request.get_json()
    print("Received data:", data)
    return jsonify({"message": "Data received successfully!"}), 200


def simulate_drone_unavailability():

    while True:
        time.sleep(2)  # Wait for 2 seconds
        with lock:
            # Randomly mark a drone as unavailable
            if drones_data:
                drone = drones_data[random.randrange(len(drones_data))]
                drone["available"] = not drone["available"]
                print(f"Drone {drone['id']} became unavailable.")


def simulate_drone_removal():
    while True:
        time.sleep(10)
        with lock:
            if drones_data:
                removed_drone = drones_data.pop(0)  # Remove the first drone in the list
                print(f"Drone {removed_drone['id']} was removed from the pool.")


threading.Thread(target=simulate_drone_unavailability, daemon=True).start()
#if you want to also simulate drones being popped
threading.Thread(target=simulate_drone_removal, daemon=True).start() #if you want to also simulate drones being popped


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)  # Allows access from other devices in the same network
