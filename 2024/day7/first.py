with open("input.txt") as f:
    data = f.read().splitlines()
from operator import invert

from dataclasses import dataclass
from typing import Callable

@dataclass
class Operator:
    symbol: str
    operation: Callable[[int, int], int]
    inverse: Callable[[int, int], int]
    can_apply: Callable[[int, int], bool]

OPERATORS = [
    Operator(
        symbol='+',
        operation=lambda x, y: x + y,
        inverse=lambda x, y: x - y,
        can_apply=lambda x, y: True
    ),
    Operator(
        symbol='*',
        operation=lambda x, y: x * y,
        inverse=lambda x, y: x // y,
        can_apply=lambda x, y: x % y == 0
    ),
]

def ways_to_be_true(value, terms):
    if len(terms) == 1:
        return [str(terms[-1])] if value == terms[-1] else []
    ways = []
    for operator in OPERATORS:
        ways += [way + operator.symbol + str(terms[-1]) for way in ways_to_be_true(operator.inverse(value, terms[-1]), terms[:-1])] if operator.can_apply(value, terms[-1]) else []
    return ways

values = []
terms_list = []
for line in data:
    values.append(int(line.split(': ')[0]))
    terms_list.append(list(map(int, line.split(': ')[1].split(' '))))

possible_count = 0
possible_values = []
for value, terms in zip(values, terms_list):
    ways = ways_to_be_true(value, terms)
    print(value, terms, ways)
    if len(ways) > 0:
        possible_count += 1
        possible_values.append(value)

print(sum(possible_values))
