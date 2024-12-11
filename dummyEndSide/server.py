from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  
# Enable CORS for all routes ( (Cross-Origin Resource Sharing) policy, which blocks requests from a different origin unless the server explicitly allows it. So we eed to configure your Flask server to allow requests from the frontend origin.)

@app.route('/api/drones', methods=['POST'])
def drones():
    data = request.get_json()
    print("Received data:", data)
    return jsonify({"message": "Data received successfully!"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)  # Allows access from other devices in the same network

