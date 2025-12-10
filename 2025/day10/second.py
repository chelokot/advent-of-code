from itertools import product
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


def getFirstNonNull(equation: Equation) -> tuple[int, float]:
    for i, coeff in enumerate(equation.coeffs):
        if abs(coeff) > 1e-12:
            return i, coeff 
    return -1, float('inf')

@dataclass
class EquationSystem:
    equations: list[Equation]
    
    def isSolvable(self):
        byFirstDigit = {}
        for newEquation in self.equations:
            while True:
                i, coeff = getFirstNonNull(newEquation)
                if i == -1:
                    break
                newEquation = newEquation * (1 / coeff)
                if i not in byFirstDigit:
                    byFirstDigit[i] = newEquation
                    break
                else:
                    newEquation = newEquation - byFirstDigit[i]
        return len(self.equations[0].coeffs) - 1 not in byFirstDigit
        
def taskToEquationSystem(task: Task) -> EquationSystem:
    # assuming only good buttons
    equationSystem = EquationSystem([])
    for i in range(len(task.voltages)):
        if task.voltages[i] > 0:
            # print(i, task.voltages[i], task.buttons)
            equationSystem.equations.append(Equation([1 if i in button else 0 for button in task.buttons] + [task.voltages[i]]))
    return equationSystem

def isTaskSolvableInFloat(task: Task) -> bool:
    return taskToEquationSystem(task).isSolvable()
    

tasks = []
with open("input.txt") as f:
    for line in f.read().splitlines():
        tasks.append(Task(list(map(lambda s: list(map(int, s[1:-1].split(','))),line.split()[1:-1])), list(map(int, line.split()[-1][1:-1].split(",")))))

def findMinimumCombination(task: Task, limit: int) -> int:
    # print(task, limit)
    result = float('inf')
    if limit == 1:
        return result
        
    oldButtons = task.buttons
    task.buttons = [button for button in oldButtons if all(task.voltages[i] != 0 for i in button)]
    
    # shouldBeSolvable = True
    
    for button in sorted(task.buttons, key = lambda x: -len(x)):
        if len(task.buttons) != 0:
            if len(max(task.buttons, key=len)) * (min(limit, result) - 1) < sum(task.voltages):
                break
            elif not set.union(*[set(button) for button in task.buttons]).issuperset(set([i for i in range(len(task.voltages)) if task.voltages[i] > 0])):
                break
            elif not isTaskSolvableInFloat(task):
                # print(task, taskToEquationSystem(task))
                # shouldBeSolvable = False
                # equationSystem = taskToEquationSystem(task)
                break
                # task.buttons.remove(button)
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
        # if result != float('inf') and not shouldBeSolvable:
        #     print(button, task, equationSystem)
        #     print(1/0)
    task.buttons = oldButtons
    # print("go up")
    return result

total = 0
for i, task in enumerate(tasks):
    print(f"{i + 1} / {len(tasks)}", task)
    result = findMinimumCombination(task, float('inf'))
    print(result)
    total += result
print(total)
        
        
            