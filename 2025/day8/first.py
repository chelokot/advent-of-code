from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class Box:
    x: int
    y: int
    z: int
    distances: dict[tuple[int, int, int], float] = field(default_factory=lambda: defaultdict(lambda: float('inf')))
    circuit: "Circuit | None" = None
    
    def measureDistance(self, otherBox: "Box"):
        distance = (self.x - otherBox.x) ** 2 + (self.y - otherBox.y) ** 2 + (self.z - otherBox.z) ** 2
        self.distances[(otherBox.x, otherBox.y, otherBox.z)] = distance
        otherBox.distances[(self.x, self.y, self.z)] = distance
    
@dataclass
class Circuit:
    boxes: list[Box] = field(default_factory=list)
    distances: dict[tuple[int, int, int], float] = field(default_factory=lambda: defaultdict(lambda: float('inf')))

    def addBox(self, box: Box):
        self.boxes.append(box)
        for position, distance in box.distances.items():
            if position not in self.distances:
                self.distances[position] = distance
            self.distances[position] = min(self.distances[position], distance)
        box.circuit = self
        box.distances = self.distances
        
        if (box.x, box.y, box.z) in self.distances:
            del self.distances[(box.x, box.y, box.z)]
        
        # for box in self.boxes:
        #     if (box.x, box.y, box.z) in self.distances:
        #         del self.distances[(box.x, box.y, box.z)]

    def mergeCircuit(self, otherCircuit: "Circuit"):
        if self == otherCircuit:
            return
        for box in otherCircuit.boxes:
            self.addBox(box)

with open("input.txt") as f:
    boxesCoordinates = f.read().splitlines()

boxes: list[Box] = []
coordinatesToBox: dict[tuple[int, int, int], Box] = {}
for boxCoordinates in boxesCoordinates:
    x, y, z = map(int, boxCoordinates.split(','))
    box = Box(x, y, z)
    coordinatesToBox[(x,y,z)] = box
    boxes.append(box)

for i in range(len(boxes)):
    for j in range(i+1, len(boxes)):
        boxes[i].measureDistance(boxes[j])

circuits: list[Circuit] = []
for box in boxes:
    circuit = Circuit()
    circuit.addBox(box)
    circuits.append(circuit)

steps = 10
for step in range(steps):
    print(step)
    minPair: tuple[Circuit, Box] | None = None
    minDistance: float = float('inf')
    for circuit in circuits:
        minCandidate = min(circuit.distances.items(), key=lambda x: x[1])
        if minCandidate[1] < minDistance:
            minDistance = minCandidate[1]
            minPair = (circuit, coordinatesToBox[minCandidate[0]])
    circuit = minPair[0]
    otherCircuit = minPair[1].circuit
    print(minPair)
    if circuit != otherCircuit:
        circuits.remove(otherCircuit)
        circuit.mergeCircuit(otherCircuit)
    else:
        del circuit.distances[(minPair[1].x, minPair[1].y, minPair[1].z)]

biggestLengths = list(sorted(map(lambda circuit: len(circuit.boxes), circuits)))
print(biggestLengths)
print(biggestLengths[-1] * biggestLengths[-2] * biggestLengths[-3])

    
    
