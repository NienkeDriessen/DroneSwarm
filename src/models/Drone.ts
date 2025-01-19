import { type Coordinate } from '../assets/GeometryTools'

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
  available: boolean;
  assignedPoints: Coordinate[];
  batteryLevel: number;
  position: Position;
  velocity: Velocity;

  constructor(
    id: number,
    available: boolean = true,
    assignedPoints: Coordinate[] = [],
    batteryLevel: number = 100,
    position: Position = {x: 0, y: 0, z: 0},
    velocity: Velocity = {x: 0, y: 0, z: 0}
  ) {
    this.id = id;
    this.available = available;
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
    this.available = !this.available;
  }

  // Method to update drone status from API data
  updateStatus(batteryLevel: number, position: Position, velocity: Velocity) {
    this.batteryLevel = batteryLevel;
    this.position = position;
    this.velocity = velocity;
  }
}

export default Drone;
