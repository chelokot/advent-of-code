from tqdm import tqdm
from copy import deepcopy
with open("input.txt") as f:
    computer_codes = list(map(lambda x: tuple(x.split('-')), f.read().splitlines()))

connections = {}

for computer1, computer2 in computer_codes:
    if computer1 not in connections:
        connections[computer1] = set()
    if computer2 not in connections:
        connections[computer2] = set()
    connections[computer1].add(computer2)
    connections[computer2].add(computer1)

current_biggest_group = set()
def find_big_groups(current_computers, current_candidates, new_computer, forbidden_computers):
    global current_biggest_group
    if len(current_computers) + len(current_candidates) <= len(current_biggest_group):
        return []
    current_computers.add(new_computer)
    current_candidates = current_candidates.intersection(connections[new_computer])
    new_big_groups = []
    new_forbidden_computers = set()
    for computer in current_candidates:
        if computer not in current_computers and computer not in forbidden_computers:
            new_big_groups += find_big_groups(current_computers, current_candidates, computer, forbidden_computers)
            new_forbidden_computers.add(computer)
            forbidden_computers.add(computer)
    for computer in new_forbidden_computers:
        forbidden_computers.remove(computer)
    if len(current_computers) > len(current_biggest_group):
        current_biggest_group = deepcopy(current_computers)
    result = new_big_groups + [tuple(current_computers)]
    current_computers.remove(new_computer)
    return result

groups = []
already_checked = set()
for computer in tqdm(connections):
    big_groups = find_big_groups(set(), connections[computer], computer, already_checked)
    groups += big_groups
    already_checked.add(computer)

print(",".join(sorted(current_biggest_group)))
