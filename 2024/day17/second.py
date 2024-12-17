with open("input.txt") as f:
    cpu = f.read()

import re
cpu_regexp = re.compile(r"Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)\n\nProgram: (.+)", re.DOTALL)
cpu = cpu_regexp.search(cpu)
A, B, C, instructions = int(cpu.group(1)), int(cpu.group(2)), int(cpu.group(3)), list(map(int, cpu.group(4).split(',')))

from first import CPU
noloop_instructions = instructions[:-2]

def check_b(A, B, needed_final_B_mod):
    print(A, A * 8 + B, B, needed_final_B_mod)
    cpu = CPU(A * 8 + B, 0, 0, noloop_instructions)
    cpu.execute()
    print(cpu.A, cpu.B, cpu.C, cpu.B % 8)
    return cpu.B % 8 == needed_final_B_mod

def findA(_A, mods):
    if len(mods) == 0:
        return _A
    for B in range(8):
        if check_b(_A, B, mods[0]):
            result = findA(_A * 8 + B, mods[1:])
            if result is not None:
                return result
    return None

print(findA(0, instructions[::-1]))
