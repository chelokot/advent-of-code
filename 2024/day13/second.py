with open("input.txt") as f:
    machines = f.read().split("\n\n")

import re
button_a_regex = re.compile(r"Button A: X\+(\d+), Y\+(\d+)")
button_b_regex = re.compile(r"Button B: X\+(\d+), Y\+(\d+)")
prize_regex = re.compile(r"Prize: X=(\d+), Y=(\d+)")

class Machine:
    def __init__(self, machine):
        self.machine = machine
        button_a = button_a_regex.search(machine)
        button_b = button_b_regex.search(machine)
        prize = prize_regex.search(machine)
        if button_a is None or button_b is None or prize is None:
            raise ValueError("Invalid machine")
        self.button_a = (int(button_a.group(1)), int(button_a.group(2)))
        self.button_b = (int(button_b.group(1)), int(button_b.group(2)))
        self.prize = (int(prize.group(1)) + 10000000000000, int(prize.group(2)) + 10000000000000)

    def is_solvable(self):
        # A1x + B1y = C1
        # A2x + B2y = C2
        # is only unsolvable if A1/A2 == B1/B2 != C1/C2
        # to avoid deletion by zero, it is better to check if A1B2 == A2B1 and A1C2 != A2C1
        a1, a2 = self.button_a
        b1, b2 = self.button_b
        c1, c2 = self.prize
        return a1*b2 != a2*b1 or a1*c2 != a2*c1

    def is_infinite_solutions(self):
        # only if A1B2 == A2B1 == A1C2 == A2C1
        a1, a2 = self.button_a
        b1, b2 = self.button_b
        c1, c2 = self.prize
        return a1*b2 == a2*b1 == a1*c2 == a2*c1

    def single_solution(self):
        # when system is not degenerate
        # x = (C1 - B1y) / A1
        # x = (C2 - B2y) / A2
        # (C1 - B1y) / A1 = (C2 - B2y) / A2
        # C1A2 - B1A2y = C2A1 - B2A1y
        # y = (C1A2 - C2A1) / (B1A2 - B2A1) = (C2A1 - C1A2) / (A1B2 - A2B1)
        # similarly, x = (C1B2 - C2B1) / (A1B2 - A2B1)
        a1, a2 = self.button_a
        b1, b2 = self.button_b
        c1, c2 = self.prize
        x = (c1*b2 - c2*b1) / (a1*b2 - a2*b1)
        y = (c2*a1 - c1*a2) / (a1*b2 - a2*b1)
        return x, y

    def check_solution(self, x, y):
        a1, a2 = self.button_a
        b1, b2 = self.button_b
        c1, c2 = self.prize
        return a1*x + b1*y == c1 and a2*x + b2*y == c2

    def solve_for_x(self, y):
        a1, b1 = self.button_a
        c1 = self.prize[0]
        return (c1 - b1*y) / a1

    def solve_for_y(self, x):
        a1, b1 = self.button_a
        c1 = self.prize[0]
        return (c1 - a1*x) / b1

    def best_price(self):
        if not self.is_solvable():
            print(f"Machine with A = {self.button_a}, B = {self.button_b}, C = {self.prize} is unsolvable")
            return 0
        elif not self.is_infinite_solutions():
            x, y = self.single_solution()
            if self.check_solution(int(x), int(y)):
                return 3 * int(x) + int(y)
            else:
                print(f"Machine with A = {self.button_a}, B = {self.button_b}, C = {self.prize} has no integer solutions, x = {x}, y = {y}")
                return 0
        else:
            # try to minimize A clicks, by setting x = 0
            x, y = -1, float("inf")
            while y > 0:
                y = self.solve_for_y(x)
                if y.is_integer():
                    break
                x += 1
            if self.check_solution(x, y):
                return 3 * x + y
            else:
                print(f"Machine with A = {self.button_a}, B = {self.button_b}, C = {self.prize} has no integer solutions <= 100")
                return 0

machines = [Machine(machine) for machine in machines]
print(sum(machine.best_price() for machine in machines))
