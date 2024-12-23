with open("input.txt") as f:
    computer_codes = map(lambda x: x.split('-'), f.read().splitlines())

connections = {}

for computer1, computer2 in computer_codes:
    if computer1 not in connections:
        connections[computer1] = set()
    if computer2 not in connections:
        connections[computer2] = set()
    connections[computer1].add(computer2)
    connections[computer2].add(computer1)

count = 0
potential_triples = set()
for computer1 in connections:
    for computer2 in connections[computer1]:
        for computer3 in connections[computer2]:
            if computer3 in connections[computer1]:
                first_letters = [computer[0] for computer in [computer1, computer2, computer3]]
                if "t" in first_letters:
                    triple = tuple(sorted([computer1, computer2, computer3]))
                    if triple not in potential_triples:
                        potential_triples.add(triple)
                        count += 1
print(count)
