import re
from dataclasses import dataclass
with open("input.txt") as f:
    wires, gates = f.read().split("\n\n")

wires = list(map(lambda x: x.split(": "), wires.splitlines()))

gates_regexp = re.compile(r"(.+)\s(XOR|AND|OR)\s(.+) -> (.+)")
gates = list(map(lambda x: gates_regexp.match(x).groups(), gates.splitlines()))

wires_values = {}
for wire_name, value in wires:
    wires_values[wire_name] = value

# the idea here is that higher bits of x, y can't affect lower bits of z
depends_on = {}

z_names = set()
for wire_name, value in wires:
    if wire_name[0] == "z":
        z_names.add(wire_name)
        depends_on[wire_name] = set()
for x, op, y, z in gates:
    if z[0] == "z":
        z_names.add(z)
        depends_on[z] = set()
for z in z_names:
    depends_on[z].add(z)
    new_depends_on = set([z])
    while new_depends_on:
        new_new_depends_on = set()
        for x, op, y, _z in gates:
            if _z in new_depends_on:
                depends_on[z].add(x)
                depends_on[z].add(y)
                new_new_depends_on.add(x)
                new_new_depends_on.add(y)
        new_depends_on = new_new_depends_on
print(depends_on)

for z in depends_on:
    # only starting with x or y here
    depends_on[z] = sorted(list(filter(lambda x: x[0] in ["x", "y"], depends_on[z])))
print(depends_on)

for z in depends_on:
    z_index = int(z[1:])
    # only x and y with higher index
    depends_on[z] = list(filter(lambda x: int(x[1:]) > z_index, depends_on[z]))
print(depends_on)


# # (but they can be in formula, for example x XOR a XOR a)
# # so for each z, we want to calculate the formula of it, in some standart form, that will eliminate all bits that doesn't actually affect if
# # as such general form we can use so called "sum of products" form
# @dataclass
# class Factor:
#     variable: str
#     negated: bool = False
# @dataclass
# class Product:
#     factors: list[Factor]
# @dataclass
# class SumOfProducts:
#     products: list[Product]

# # we are starting with AND, OR, or XOR gate. AND and OR are already in sum of products form
# def and_gate(x: str, y: str) -> SumOfProducts:
#     return SumOfProducts([Product([Factor(x), Factor(y)])])
# def or_gate(x: str, y: str) -> SumOfProducts:
#     return SumOfProducts([Product([Factor(x)]), Product([Factor(y)])])

# # XOR is not in sum of products form, but we can convert it to it
# # x XOR y = (x AND NOT y) OR (NOT x AND y)
# def xor_gate(x: str, y: str) -> SumOfProducts:
#     return SumOfProducts([
#         Product([Factor(x, False), Factor(y, True)]),
#         Product([Factor(x, True), Factor(y, False)])
#     ])

# # now, as we go up in the tree, we must be able to do the substitution
# # for that we'll need few helper functions
# def negate_sum_of_products(sop: SumOfProducts) -> SumOfProducts:
#     # not (abc OR def) = (not a OR not b OR not c) AND (not d OR not e OR not f) = (not a AND not d) OR (not a AND not e) OR (not a AND not f) OR ...
