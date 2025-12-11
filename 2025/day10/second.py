from dataclasses import dataclass
@dataclass
class Task:
    buttons: list[list[int]]
    voltages: list[int]

@dataclass
class Equation:
    coeffs: list[float]
    def __add__(self, other):
        return Equation([a + b for a, b in zip(self.coeffs, other.coeffs)])
    def __sub__(self, other):
        return Equation([a - b for a, b in zip(self.coeffs, other.coeffs)])
    def __mul__(self, scalar):
        return Equation([a * scalar for a in self.coeffs])
    def __rmul__(self, scalar):
        return self.__mul__(scalar)


def getFirstNonNull(coeffs: list[float]) -> tuple[int, float]:
    for i, coeff in enumerate(coeffs):
        if abs(coeff) > 1e-12:
            return i, coeff 
    return -1, float('inf')

@dataclass
class EquationSystem:
    equations: list[Equation]
    
    def isSolvable(self):
        byFirstDigit = {}
        freeI = len(self.equations[0].coeffs) - 1
        for newEquation in self.equations:
            prevI = -1
            while True:
                i, coeff = getFirstNonNull(newEquation.coeffs[prevI + 1:])
                if i == -1:
                    break
                i = prevI + 1 + i
                newEquation = newEquation * (1 / coeff)
                if i not in byFirstDigit:
                    byFirstDigit[i] = newEquation
                    break
                else:
                    newEquation = newEquation - byFirstDigit[i]
                if i == freeI:
                    return False
                prevI = i
        self.equations = byFirstDigit.values()
        return True
        
def taskToEquationSystem(task: Task) -> EquationSystem:
    equationSystem = EquationSystem([])
    for i in range(len(task.voltages)):
        if task.voltages[i] > 0:
            equationSystem.equations.append(Equation([1 if i in button else 0 for button in task.buttons] + [task.voltages[i]]))
    return equationSystem

def isTaskSolvableInFloat(task: Task) -> bool:
    return taskToEquationSystem(task).isSolvable()
    

tasks = []
with open("input.txt") as f:
    for line in f.read().splitlines():
        tasks.append(Task(list(map(lambda s: list(map(int, s[1:-1].split(','))),line.split()[1:-1])), list(map(int, line.split()[-1][1:-1].split(",")))))

def findMinimumCombination(task: Task, limit: int) -> int:
    result = float('inf')
    if limit == 1:
        return result
        
    oldButtons = task.buttons
    task.buttons = [button for button in oldButtons if all(task.voltages[i] != 0 for i in button)]
    for button in sorted(task.buttons, key = lambda x: -len(x)):
        if len(task.buttons) != 0:
            if not isTaskSolvableInFloat(task) or len(max(task.buttons, key=len)) * (min(limit, result) - 1) < sum(task.voltages):
                break
            else:
                task.buttons.remove(button)
        fullButtonCount = min(task.voltages[i] for i in button)
        for buttonCount in range(fullButtonCount, -1, -1):
            for i in button: task.voltages[i] -= buttonCount
            if sum(task.voltages) == 0:
                result = min(result, buttonCount)
            else:
                result = min(result, buttonCount + findMinimumCombination(task, min(limit, result) - buttonCount))
            for i in button: task.voltages[i] += buttonCount
    task.buttons = oldButtons
    return result

total = 0
for i, task in enumerate(tasks):
    print(f"{i + 1} / {len(tasks)}", task)
    result = findMinimumCombination(task, float('inf'))
    print(result)
    total += result
print(total)
