import numpy as np
import copy
from tqdm import tqdm

with open("input.txt") as f:
    data = f.read().splitlines()

possible_directions = ['>', 'v', '<', '^']
class Lab:
    def __init__(self, map):
        self.map = map
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] in possible_directions:
                    self.position = (i, j)
                    self.direction = self.map[i][j]
                    break
        self.visited_positions = set()
        self.finished = False
        self.loop = False

    def is_leaving_area(self):
        i, j = self.position
        if self.direction == 'v' and i == len(self.map) - 1:
            return True
        elif self.direction == '^' and i == 0:
            return True
        elif self.direction == '>' and j == len(self.map[i]) - 1:
           return True
        elif self.direction == '<' and j == 0:
            return True
        return False

    def next_position(self):
        i, j = self.position
        if self.direction == 'v':
            return (i+1, j)
        elif self.direction == '^':
            return (i-1, j)
        elif self.direction == '>':
            return (i, j+1)
        elif self.direction == '<':
            return (i, j-1)
        else:
            raise ValueError("Invalid direction")

    def is_path_free(self):
        i, j = self.position
        next_i, next_j = self.next_position()
        if self.map[next_i][next_j] in ['.', 'X']:
            return True
        return False

    def step(self):
        if self.is_leaving_area():
            self.finished = True
            return
        i, j = self.position
        if self.is_path_free():
            next_i, next_j = self.next_position()
            current_state = (self.position, self.direction)
            if current_state in self.visited_positions:
                self.finished = True
                self.loop = True
                return
            self.visited_positions.add((self.position, self.direction))
            self.map[next_i][next_j] = self.direction
            self.map[i][j] = 'X'
            self.position = (next_i, next_j)
        else:
            self.direction = possible_directions[(possible_directions.index(self.direction) + 1) % 4]
            self.map[i][j] = self.direction

    def count_visited(self):
        count = 0
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] in possible_directions + ['X']:
                    count += 1
        return count

    def process(self):
        while not self.finished:
            self.step()
        return self.count_visited()

initial_map = [list(line) for line in data]
test_initial_map = copy.deepcopy(initial_map)
test_lab = Lab(test_initial_map)
test_lab.process()
# it only does make sense to put obstacle somewhere at the original route
possible_obstacle_positions = set()
for i in range(len(test_lab.map)):
    for j in range(len(test_lab.map[i])):
        if test_lab.map[i][j] in possible_directions + ['X']:
            possible_obstacle_positions.add((i, j))

possible_new_obstacles_count = 0
for (i, j) in tqdm(possible_obstacle_positions):
    if initial_map[i][j] in possible_directions + ['#']:
        continue
    attempt_map = copy.deepcopy(initial_map)
    attempt_map[i][j] = '#'
    lab = Lab(attempt_map)
    lab.process()
    if lab.loop:
        possible_new_obstacles_count += 1
print(possible_new_obstacles_count)
