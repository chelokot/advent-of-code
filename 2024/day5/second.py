with open("input.txt") as f:
    data = f.read()
instructions, updates = data.split("\n\n")
instructions = instructions.splitlines()
updates = updates.splitlines()

all_pages = set()
ordering_rules = {}
for instruction in instructions:
    a, b = instruction.split("|")
    ordering_rules[(a, b)] = -1
    ordering_rules[(b, a)] = 1
    all_pages.add(a)
    all_pages.add(b)

for page in all_pages:
    for other_page in all_pages:
        if (page, other_page) not in ordering_rules:
            ordering_rules[(page, other_page)] = 0

from functools import cmp_to_key
required_order = sorted(list(all_pages), key = cmp_to_key(lambda a, b: ordering_rules[(a, b)]))

correct_update_lists = []
for update in updates:
    update_list = update.split(",")

    # Python's sorted() function guarantees stability (will only swap elements if they are in strictly wrong order)
    correct_update_list = sorted(update_list, key = cmp_to_key(lambda a, b: ordering_rules[(a, b)]))
    correct_update = ",".join(correct_update_list)

    if update != correct_update:
        correct_update_lists.append(correct_update_list)

print(sum([int(l[len(l) // 2]) for l in correct_update_lists]))
