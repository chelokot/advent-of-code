from dataclasses import dataclass, field
@dataclass
class Box:
    x: int
    y: int
    z: int
    circuit: "Circuit | None" = None

@dataclass
class Circuit:
    boxes: list[Box] = field(default_factory=list)
    def addBox(self, box: Box):
        self.boxes.append(box)
        box.circuit = self

    def mergeCircuit(self, otherCircuit: "Circuit"):
        if self == otherCircuit: return
        for box in otherCircuit.boxes:
            self.addBox(box)

with open("input.txt") as f:
    boxesCoordinates = f.read().splitlines()

distances = [] 
def measureDistance(box: Box, otherBox: Box):
    distances.append(((box.x - otherBox.x) ** 2 + (box.y - otherBox.y) ** 2 + (box.z - otherBox.z) ** 2, box, otherBox))

boxes: list[Box] = []
for boxCoordinates in boxesCoordinates:
    box = Box(*map(int, boxCoordinates.split(',')))
    boxes.append(box)

for i in range(len(boxes)):
    for j in range(i+1, len(boxes)):
        measureDistance(boxes[i], boxes[j])

distances.sort(key = lambda x: x[0])
circuits: list[Circuit] = []
for box in boxes:
    circuit = Circuit()
    circuit.addBox(box)
    circuits.append(circuit)

steps = 1000
for step in range(steps):
    box1, box2 = distances[step][1:]
    if box1.circuit != box2.circuit:
        circuits.remove(box2.circuit)
    box1.circuit.mergeCircuit(box2.circuit)

biggestLengths = list(sorted(map(lambda circuit: len(circuit.boxes), circuits)))
print(biggestLengths[-1] * biggestLengths[-2] * biggestLengths[-3])

    
    
