import re
with open("input.txt") as f:
    wires, gates = f.read().split("\n\n")

wires = list(map(lambda x: x.split(": "), wires.splitlines()))

gates_regexp = re.compile(r"(.+)\s(XOR|AND|OR)\s(.+) -> (.+)")
gates = list(map(lambda x: gates_regexp.match(x).groups(), gates.splitlines()))

wires_values = {}
for wire_name, value in wires:
    wires_values[wire_name] = value

gates_set = set(gates)
while gates_set:
    for gate in list(gates_set):
        if wires_values.get(gate[0]) is not None and wires_values.get(gate[2]) is not None:
            if gate[1] == "AND":
                wires_values[gate[3]] = int(wires_values[gate[0]]) & int(wires_values[gate[2]])
            elif gate[1] == "OR":
                wires_values[gate[3]] = int(wires_values[gate[0]]) | int(wires_values[gate[2]])
            elif gate[1] == "XOR":
                wires_values[gate[3]] = int(wires_values[gate[0]]) ^ int(wires_values[gate[2]])
            gates_set.remove(gate)


wires_starting_with_z = list(filter(lambda x: x[0][0] == "z", wires_values.items()))
sorted_wires = sorted(wires_starting_with_z, key=lambda x: x[0], reverse=True)
number = 0
for wire_name, value in sorted_wires:
    number *= 2
    number += int(value)
print(number)
