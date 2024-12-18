import aocd
import re
import functools
from typing import NamedTuple
from heapq import heappop, heappush
from tqdm import tqdm as progress

import cli
from vector import Vector
from astar import AStar

sample_data = """\
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""
data = sample_data if cli.sample else aocd.data

width = 7 if cli.sample else 71
height = width
world = [[None] * width for _ in range(height)]

is_in_range = lambda p: p.x >= 0 and p.y >= 0 and p.x < width and p.y < height

start_pos = Vector(0, 0)
end_pos = Vector(width - 1, height - 1)

bytes = list(map(lambda l: re.match(r"(\d+),(\d+)", l).groups(), data.splitlines()))
for i, (x, y) in enumerate(bytes):
    world[int(y)][int(x)] = i + 1

World = list[int | None]
Path = list[Vector]


def print_world(world: World | list[str | None], time: int):
    def elem_to_str(elem: int | str | None) -> str:
        if not elem:
            return "."
        if isinstance(elem, str):
            return elem
        return "#" if elem <= time else "."

    world_str = "\n".join(map(lambda x: "".join(map(elem_to_str, x)), world))
    print(f"{world_str}\n")


def print_world_with_solution(world: World, solution: Path, time: int):
    world_with_solution = list(map(list, world))
    for x, y in solution:
        world_with_solution[y][x] = "O"
    print_world(world_with_solution, time)


directions = [
    Vector(-1, 0),
    Vector(+1, 0),
    Vector(0, -1),
    Vector(0, +1),
]


class Solver(AStar):
    def __init__(self, fixed_time: int | None):
        super().__init__()

        self.fixed_time = fixed_time

    def heuristic_cost_estimate(self, current: Vector, goal: Vector) -> float:
        diff = current - goal
        # manhattan distance
        return abs(diff.x) + abs(diff.y)

    def distance_between(self, _: Vector, __: Vector) -> float:
        return 1

    def neighbors(self, node: Vector) -> list[Vector]:
        time = self.fixed_time if self.fixed_time else int(self.current.gscore)
        return filter(
            lambda p: world[p.y][p.x] > time if world[p.y][p.x] else True,
            filter(
                is_in_range, map(functools.partial(Vector.__add__, node), directions)
            ),
        )


################################################################################################
# Problem 1
fixed_time = 12 if cli.sample else 1024
print_world(world, fixed_time)

(path, cost) = Solver(fixed_time).astar(start_pos, end_pos)
print_world_with_solution(world, path, fixed_time)

# path contains start_pos which we don't count as a step
print(f"Problem 1: {len(path) - 1}")

################################################################################################
# Problem 2
