with open("input.txt") as f:
    cpu = f.read()

import re
cpu_regexp = re.compile(r"Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)\n\nProgram: (.+)", re.DOTALL)
cpu = cpu_regexp.search(cpu)
A, B, C, instructions = int(cpu.group(1)), int(cpu.group(2)), int(cpu.group(3)), list(map(int, cpu.group(4).split(',')))

class CPU:
    def __init__(self, A, B, C, instructions):
        self.A = A
        self.B = B
        self.C = C
        self.instructions = instructions
        self.instruction_pointer = 0
        self.output = []

    def execute_next_command(self):
        instruction = self.instructions[self.instruction_pointer]
        literal_operand = self.instructions[self.instruction_pointer + 1]
        if literal_operand <= 3:
            combo_operand = literal_operand
        elif literal_operand == 4:
            combo_operand = self.A
        elif literal_operand == 5:
            combo_operand = self.B
        elif literal_operand == 6:
            combo_operand = self.C
        else:
            raise ValueError(f"Invalid literal operand {literal_operand}")

        if instruction == 0:
            self.adv(combo_operand)
        elif instruction == 1:
            self.bxl(literal_operand)
        elif instruction == 2:
            self.bst(combo_operand)
        elif instruction == 3:
            self.jnz(literal_operand)
        elif instruction == 4:
            self.bxc(combo_operand)
        elif instruction == 5:
            self.out(combo_operand)
        elif instruction == 6:
            self.bdv(combo_operand)
        elif instruction == 7:
            self.cdv(combo_operand)

    def adv(self, operand):
        self.A >>= operand

    def bdv(self, operand):
        self.B = self.A >> operand

    def cdv(self, operand):
        self.C = self.A >> operand

    def bxl(self, operand):
        self.B ^= operand

    def bst(self, operand):
        self.B = operand % 8

    def jnz(self, operand):
        if self.A != 0:
            self.instruction_pointer = operand - 2

    def bxc(self, operand):
        self.B ^= self.C

    def out(self, operand):
        self.output.append(operand % 8)

    def execute(self):
        while self.instruction_pointer < len(self.instructions):
            self.execute_next_command()
            self.instruction_pointer += 2
        return self.output

if __name__ == "__main__":
    cpu = CPU(A, B, C, instructions)
    output = cpu.execute()
    print(','.join(map(str, output)))
