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


# def bfs(
#     world: World,
#     start_pos: Vector,
#     end_pos: Vector,
#     fixed_time: int | None,
#     find_single_path: bool,
# ) -> list[Path] | Path:
#     # class SearchNode(NamedTuple):
#     #     pos: Vector

#     class QueueElem(NamedTuple):
#         score: int
#         pos: Vector
#         dir: Vector
#         path: Path

#     target_score = math.inf
#     paths: list[Path] = []

#     visited: dict[Vector, int] = {}
#     # visited: dict[SearchNode, int] = {}
#     queue: list[QueueElem] = [QueueElem(0, start_pos, Vector(1, 0), [])]
#     while queue:
#         # arrived at only nodes that are too expensive, call it quits
#         score, pos, dir, path = heappop(queue)
#         if score > target_score:
#             break

#         # remember this node
#         node = pos
#         # node = SearchNode(pos)
#         if node in visited and visited[node] < score:
#             continue
#         visited[node] = score

#         prev = world[pos.y][pos.x]
#         world[pos.y][pos.x] = "X"
#         paths = list(visited.keys())
#         del paths[paths.index(pos)]
#         print_world_with_solution(world, paths, fixed_time)
#         world[pos.y][pos.x] = prev

#         def free_tile(p: Vector, score: int):
#             if not is_in_range(p):
#                 return False

#             tile = world[p.y][p.x]
#             time = fixed_time if fixed_time else score
#             return True if tile is None or tile > time else False

#         # push forward, left, and right options
#         for next_dir in (dir, Vector(dir.y, -dir.x), Vector(-dir.y, dir.x)):
#             next = pos + next_dir
#             if free_tile(next, score):
#                 heappush(queue, QueueElem(score + 1, next, next_dir, path + [pos]))

#         # if we arrived at the end, store this as a path
#         # and remember its score to quit when we get past it
#         if pos == end_pos:
#             target_score = score
#             if find_single_path:
#                 return path + [end_pos]
#             paths.append(path + [end_pos])

#     return paths

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

# binary search the problem space
bot_time = 0
top_time = len(bytes)
while True:
    mid_time = bot_time + (top_time - bot_time) // 2
    if Solver(mid_time).astar(start_pos, end_pos):
        bot_time = mid_time + 1
    else:
        top_time = mid_time - 1

    if bot_time >= top_time:
        break

blocking_time = mid_time + 1 if Solver(mid_time).astar(start_pos, end_pos) else mid_time
blocking_byte = bytes[blocking_time - 1]
blocking_byte = Vector(int(blocking_byte[0]), int(blocking_byte[1]))
print(f"Problem 2: {blocking_byte}")
