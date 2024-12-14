import aocd
import re
import functools
from typing import NamedTuple
from tqdm import tqdm as progress

import cli

sample_data = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
data = sample_data if cli.sample else aocd.data
width = 11 if cli.sample else 101
height = 7 if cli.sample else 103


class Vector(NamedTuple):
    x: int
    y: int

    def __add__(lhs, rhs):
        return Vector(lhs.x + rhs.x, lhs.y + rhs.y)

    def __sub__(lhs, rhs):
        return Vector(lhs.x - rhs.x, lhs.y - rhs.y)

    def __mul__(lhs, rhs: int):
        return Vector(lhs.x * rhs, lhs.y * rhs)


class Robot(NamedTuple):
    pos: Vector
    vel: Vector

    def move(self, steps: int):
        (nx, ny) = self.pos + self.vel * steps
        nx = ((nx % width) + width) % width
        ny = ((ny % height) + height) % height
        return Robot(Vector(nx, ny), self.vel)


def make_robot(setup: str):
    (px, py, vx, vy) = re.match(r"p=(.+)\,(.+) v=(.+)\,(.+)", setup).groups()

    return Robot(Vector(int(px), int(py)), Vector(int(vx), int(vy)))


robots = list(map(make_robot, data.split("\n")))


################################################################################################
# Problem 1
moved_robots = list(map(functools.partial(Robot.move, steps=100), progress(robots)))
tl_quadrant = list(
    filter(lambda r: r.pos.x < width // 2 and r.pos.y < height // 2, moved_robots)
)
tr_quadrant = list(
    filter(lambda r: r.pos.x > width // 2 and r.pos.y < height // 2, moved_robots)
)
br_quadrant = list(
    filter(lambda r: r.pos.x > width // 2 and r.pos.y > height // 2, moved_robots)
)
bl_quadrant = list(
    filter(lambda r: r.pos.x < width // 2 and r.pos.y > height // 2, moved_robots)
)
solution = len(tl_quadrant) * len(tr_quadrant) * len(br_quadrant) * len(bl_quadrant)
print(f"Problem 1: {solution}")

################################################################################################
# Problem 2
