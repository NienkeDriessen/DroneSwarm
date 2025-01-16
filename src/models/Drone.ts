import { type Coordinate } from '../assets/GeometryTools'

class Drone {
  id: number;
  available: boolean;
  assignedPoints: Coordinate[];

  constructor(id: number, available: boolean = true, assignedPoints: Coordinate[] = []) {
      this.id = id;
      this.available = available;
      this.assignedPoints = assignedPoints;
  }

  // Method to assign points to the drone
  assignPoints(points: Coordinate[]) {
      this.assignedPoints = points;
  }

  // Method to toggle availability
  toggleAvailability() {
      this.available = !this.available;
  }
}

export default Drone;
