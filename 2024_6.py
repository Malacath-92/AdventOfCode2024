import aocd
import itertools

import cli

sample_data = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
data = sample_data if cli.sample else aocd.data

floor = data.splitlines()
width = len(floor[0])
height = len(floor)

pos_in_range_map = {
    (-1, 0): lambda x: x[0] >= 0,
    (+1, 0): lambda x: x[0] < width,
    (0, -1): lambda x: x[1] >= 0,
    (0, +1): lambda x: x[1] < height,
}

start_pos = data.replace("\n", "").find("^")
start_pos = [start_pos % width, start_pos // width]


def find_next_obstruction(floor, pos, dir):
    pos_in_range = pos_in_range_map[dir]

    next_pos = [pos[0] + dir[0], pos[1] + dir[1]]
    while pos_in_range(next_pos) and floor[next_pos[1]][next_pos[0]] != "#":
        next_pos[0] += dir[0]
        next_pos[1] += dir[1]

    if pos_in_range(next_pos):
        next_pos = [next_pos[0] - dir[0], next_pos[1] - dir[1]]
        return {"pos": next_pos, "symbol": "#"}
    else:
        return {"pos": next_pos, "symbol": "~"}


pos = start_pos.copy()
dir = (0, -1)
visited = [list(l.replace(".", " ").replace("^", " ")) for l in floor]
while pos_in_range_map[dir](pos):
    [x, y] = pos
    visited[y][x] = "o"

    pos[0] += dir[0]
    pos[1] += dir[1]
    [x, y] = pos
    if not pos_in_range_map[dir](pos):
        break
    elif floor[y][x] == "#":
        pos[0] -= dir[0]
        pos[1] -= dir[1]
        dir = (-dir[1], dir[0])

print(f"Problem 1: {sum([r.count('o') for r in visited])}")

visited_positions = [
    (x, y)
    for (x, y) in itertools.product(range(0, width), range(0, height))
    if visited[y][x] != " "
]

valid_obstructions = []
for i, (ox, oy) in enumerate(visited_positions):
    print(f"Testing position number {i}")

    def is_loop():
        pos = start_pos.copy()
        dir = (0, -1)
        loop_visited = [[None] * width for _ in range(height)]
        while pos_in_range_map[dir](pos):
            [x, y] = pos
            if vis := loop_visited[y][x]:
                if dir in vis:
                    return True
                vis.append(dir)
            else:
                loop_visited[y][x] = [dir]

            pos[0] += dir[0]
            pos[1] += dir[1]
            [x, y] = pos
            if not pos_in_range_map[dir](pos):
                break
            elif floor[y][x] == "#" or (x, y) == (ox, oy):
                pos[0] -= dir[0]
                pos[1] -= dir[1]
                dir = (-dir[1], dir[0])
        return False

    if is_loop():
        valid_obstructions.append((x, y))

print(f"Problem 2: {len(valid_obstructions)}")
