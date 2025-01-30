import { type Coordinate } from '../assets/GeometryTools';

interface Position {
  x: number;
  y: number;
  z: number;
}

interface Velocity {
  x: number;
  y: number;
  z: number;
}

class Drone {
  id: number;
  status: string;
  assignedPoints: Coordinate[];
  batteryLevel: number;
  position: Position;
  velocity: Velocity;

  constructor(
    id: number,
    status: string = "unknown",
    assignedPoints: Coordinate[] = [],
    batteryLevel: number = 100,
    position: Position = { x: 0, y: 0, z: 0 },
    velocity: Velocity = { x: 0, y: 0, z: 0 }
  ) {
    this.id = id;
    this.status = status;
    this.assignedPoints = assignedPoints;
    this.batteryLevel = batteryLevel;
    this.position = position;
    this.velocity = velocity;
  }

  // Method to assign points to the drone
  assignPoints(points: Coordinate[]) {
    this.assignedPoints = points;
  }

  // Method to toggle availability
  toggleAvailability() {
    this.status = "available";
  }

  // Method to toggle availability
  toggleUnavailability() {
    this.status = "unavailable";
  }

  // Method to update drone status from API data
  updateStatus(batteryLevel: number, position: Position, velocity: Velocity) {
    this.batteryLevel = batteryLevel;
    this.position = position;
    this.velocity = velocity;
  }
}

export default Drone;
