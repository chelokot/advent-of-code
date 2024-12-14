with open("input.txt") as f:
    robots = f.read().splitlines()

import re
robot_regex = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
robots = [robot_regex.search(robot) for robot in robots]

class Robot:
    def __init__(self, _robot, space):
        self.position = (int(_robot.group(1)), int(_robot.group(2)))
        self.velocity = (int(_robot.group(3)), int(_robot.group(4)))
        self.space = space

    def move(self, time):
        x, y = self.position
        dx, dy = self.velocity
        sx, sy = self.space
        self.position = ((x + dx*time % sx) + sx ) % sx, ((y + dy*time % sy) + sy) % sy
        return self.position

    def quadrant(self):
        x, y = self.position
        sx, sy = self.space
        if   x < sx//2 and y < sy//2:
            return 0
        elif x > sx//2 and y < sy//2:
            return 1
        elif x > sx//2 and y > sy//2:
            return 2
        elif x < sx//2 and y > sy//2:
            return 3
        else:
            return None

time_to_wait = 100
robots = [Robot(robot, (101, 103)) for robot in robots]
for robot in robots:
    robot.move(time_to_wait)
quadrants = [0 for _ in range(4)]
for robot in robots:
    if robot.quadrant() is not None:
        quadrants[robot.quadrant()] += 1

print(quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3])
