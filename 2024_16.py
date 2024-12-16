import aocd
import math
import functools
import itertools
from typing import NamedTuple
from heapq import heappop, heappush
from tqdm import tqdm as progress

import cli
from vector import Vector

sample_data = """\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""
data = sample_data if cli.sample else aocd.data

flat_maze = data.replace("\n", "")
maze = list(map(list, data.splitlines()))
width = len(maze[0])
height = len(maze)

flat_idx_to_coords = lambda i: Vector(i % width, i // width)
is_in_range = lambda p: p.x >= 0 and p.y >= 0 and p.x < width and p.y < height

start_pos = flat_idx_to_coords(flat_maze.find("S"))
end_pos = flat_idx_to_coords(flat_maze.find("E"))


def print_maze(maze: list[str]):
    maze_str = "\n".join(map(lambda x: "".join(x), maze))
    print(f"{maze_str}\n")


def print_maze_with_solution(maze: list[str], solution: list[Vector]):
    maze_with_solution = list(map(list, maze))
    for x, y in solution:
        maze_with_solution[y][x] = "o"
    print_maze(maze_with_solution)


################################################################################################
# Problem 1
from astar import AStar

directions = [
    Vector(-1, 0),
    Vector(+1, 0),
    Vector(0, -1),
    Vector(0, +1),
]


class Solver(AStar):
    def heuristic_cost_estimate(self, current: Vector, goal: Vector) -> float:
        diff = current - goal
        # manhattan distance
        return abs(diff.x) + abs(diff.y)

    def distance_between(self, n1: Vector, n2: Vector) -> float:
        previous = self.current.came_from
        prev_dir = previous.data - n1 if previous else Vector(1, 0)
        this_dir = n1 - n2
        if prev_dir != this_dir:
            return 1001
        return 1

    def neighbors(_, node: Vector) -> list[Vector]:
        return filter(
            lambda p: maze[p.y][p.x] != "#",
            filter(
                is_in_range, map(functools.partial(Vector.__add__, node), directions)
            ),
        )


(solution, cost) = Solver().astar(start_pos, end_pos)
print_maze_with_solution(maze, solution)
print(f"Problem 1: {int(cost)}")


################################################################################################
# Problem 2
class SearchNode(NamedTuple):
    pos: Vector
    dir: Vector


class QueueElem(NamedTuple):
    score: int
    pos: Vector
    dir: Vector
    path: list[Vector]


target_score = math.inf
paths: list[list[Vector]] = []

visited: dict[SearchNode, int] = {}
queue: list[QueueElem] = [QueueElem(0, start_pos, Vector(1, 0), [])]
while queue:
    # arrived at only nodes that are too expensive, call it quits
    score, pos, dir, path = heappop(queue)
    if score > target_score:
        break

    # remember this node
    node = SearchNode(pos, dir)
    if node in visited and visited[node] < score:
        continue
    visited[node] = score

    # push forward option
    next = pos + dir
    if maze[next.y][next.x] != "#":
        heappush(queue, QueueElem(score + 1, next, dir, path + [pos]))

    # push turn-left option
    left_dir = Vector(dir.y, -dir.x)
    heappush(queue, QueueElem(score + 1000, pos, left_dir, path))

    # push turn-right option
    right_dir = Vector(-dir.y, dir.x)
    heappush(queue, QueueElem(score + 1000, pos, right_dir, path))

    # if we arrived at the end, store this as a path
    # and rememeber its score to quit when we get past it
    if pos == end_pos:
        target_score = score
        paths.append(path + [end_pos])

unique_points = set(itertools.chain.from_iterable(paths))
print(f"Problem 2: {len(unique_points)}")
