import aocd
import math
from typing import NamedTuple
from heapq import heappop, heappush

import cli
from vector import Vector

sample_data = """\
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""
data = sample_data if cli.sample else aocd.data

flat_maze = data.replace("\n", "")
maze = list(map(list, data.splitlines()))
width = len(maze[0])
height = len(maze)

flat_idx_to_coords = lambda i: Vector(i % width, i // width)
is_in_range = lambda p: p.x >= 0 and p.y >= 0 and p.x < width and p.y < height

start_pos = flat_idx_to_coords(flat_maze.find("S"))
end_pos = flat_idx_to_coords(flat_maze.find("E"))


Maze = list[list[str]]
Path = list[Vector]


class CheatPath(NamedTuple):
    score: int
    path: Path
    cheat_pos: Vector


directions = [
    Vector(-1, 0),
    Vector(+1, 0),
    Vector(0, -1),
    Vector(0, +1),
]


def print_maze(maze: Maze):
    maze_str = "\n".join(map(lambda x: "".join(x), maze))
    print(f"{maze_str}\n")


def print_maze_with_solution(
    maze: Maze, solution: Path, cheat_pos: Vector | None = None
):
    maze_with_solution = list(map(list, maze))
    for x, y in solution:
        maze_with_solution[y][x] = "o"

    if cheat_pos is not None:
        prev = maze_with_solution[cheat_pos.y][cheat_pos.x]
        maze_with_solution[cheat_pos.y][cheat_pos.x] = "C"
        print_maze(maze_with_solution)
        maze_with_solution[cheat_pos.y][cheat_pos.x] = prev
    else:
        print_maze(maze_with_solution)


################################################################################################
# Problem 1
def dfs(
    maze: Maze,
    start_pos: Vector,
    end_pos: Vector,
    allow_cheats: bool = False,
    partial_paths: dict[Path] = {},
    max_score: float = 0,
) -> Path | list[CheatPath]:
    class SearchNode(NamedTuple):
        pos: Vector

    class QueueElem(NamedTuple):
        score: int
        pos: Vector
        path: Path

    paths: list[CheatPath] = []

    visited: dict[SearchNode, int] = {}
    target_score: float = math.inf

    queue: list[QueueElem] = [QueueElem(0, start_pos, [])]
    while queue:
        # arrived at only nodes that are too expensive, call it quits
        score, pos, path = heappop(queue)
        if score > target_score:
            break

        # remember this node
        node = SearchNode(pos)
        if node in visited and visited[node] < score:
            continue
        visited[node] = score

        # if we arrived at the end, store this as a path or return it
        # and remember its score to quit when we get past it
        if pos == end_pos:
            target_score = score
            if not allow_cheats:
                valid_path = path + [end_pos]
                return valid_path

        # push all directions
        for dir in directions:
            next = pos + dir
            if is_in_range(next):
                next_tile = maze[next.y][next.x]
                if next_tile != "#":
                    heappush(queue, QueueElem(score + 1, next, path + [pos]))
                elif allow_cheats:
                    for cheat_dir in directions:
                        cheat_next = next + cheat_dir
                        if cheat_next != pos and cheat_next in partial_paths:
                            partial_path = partial_paths[cheat_next]
                            cheated_path = path + [pos, next] + partial_path
                            cheated_score = len(cheated_path) - 1
                            if max_score > cheated_score:
                                cheat_pos = next
                                cheated_path = CheatPath(
                                    cheated_score, cheated_path, cheat_pos
                                )
                                paths.append(cheated_path)

    return paths if allow_cheats else None


regular_path = dfs(maze, start_pos, end_pos)
regular_score = len(regular_path) - 1

partial_paths = {pos: regular_path[i:] for i, pos in enumerate(regular_path)}

if cli.sample:
    print_maze_with_solution(maze, regular_path)
    cheated_paths = dfs(
        maze,
        start_pos,
        end_pos,
        allow_cheats=True,
        partial_paths=partial_paths,
        max_score=regular_score,
    )
    for score, path, cheat_pos in reversed(sorted(cheated_paths)):
        print(cheat_pos, score)
        print_maze_with_solution(maze, path, cheat_pos=cheat_pos)

    print(f"Problem 1: {len(cheated_paths)}")
else:
    cheated_paths = dfs(
        maze,
        start_pos,
        end_pos,
        allow_cheats=True,
        partial_paths=partial_paths,
        max_score=regular_score - 99,
    )
    print(f"Problem 1: {len(cheated_paths)}")


################################################################################################
# Problem 2
num_cheats: int = 0
cheat_margin = 99
for i, pos in enumerate(regular_path):
    # can't cheat more than 100 points unless the target is at least 100 away
    possible_targets = regular_path[i + 100 :]

    for target_pos in possible_targets:
        # if we are further than 20 steps away we can't reach this via cheating
        dist = pos.manhattan_dist(target_pos)
        if dist > 20:
            continue

        # the score of this cheated path can be computed from the partial paths
        cheated_score = i + dist + len(partial_paths[target_pos])
        if cheated_score > regular_score - cheat_margin:
            continue

        # found a cheat that is fast enough  🙌
        num_cheats += 1

print(f"Problem 2: {num_cheats}")
