from tqdm import tqdm
import functools

with open("input.txt") as f:
    data = f.read()

towels, designs = data.split("\n\n")
towels = towels.split(", ")
designs = designs.splitlines()

@functools.lru_cache(maxsize=None)
def check_if_possible(design):
    count = design == ""
    for towel in towels:
        count += design.startswith(towel) and check_if_possible(design[len(towel):])
    return count

print(sum(tqdm(check_if_possible(design) for design in designs)))
