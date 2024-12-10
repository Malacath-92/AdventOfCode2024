import aocd
import operator
import itertools
import functools

import cli

sample_data = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""
data = sample_data if cli.sample else aocd.data
flat_data = "".join(data.splitlines())

mountains = data.splitlines()
width = len(mountains[0])
height = len(mountains)
flat_idx_to_coords = lambda i: (i % width, i // width)
is_in_range = lambda p: p[0] >= 0 and p[1] >= 0 and p[0] < width and p[1] < height
neighbour = lambda pos, dir: (pos[0] + dir[0], pos[1] + dir[1])
is_one_up = lambda h, pos: int(mountains[pos[1]][pos[0]]) == h + 1

directions = [
    (-1, 0),
    (+1, 0),
    (0, -1),
    (0, +1),
]
pos_in_range_map = {
    (-1, 0): lambda x: x[0] >= 0,
    (+1, 0): lambda x: x[0] < width,
    (0, -1): lambda x: x[1] >= 0,
    (0, +1): lambda x: x[1] < height,
}

starting_positions = list(
    map(flat_idx_to_coords, [i for i, h in enumerate(flat_data) if h == "0"])
)


################################################################################################
# Problem 1
def start_position_score(pos):
    def high_points_reached(h, pos):
        if h == 9:
            return [pos]

        return itertools.chain.from_iterable(
            map(
                functools.partial(high_points_reached, h + 1),
                filter(
                    functools.partial(is_one_up, h),
                    filter(
                        is_in_range, map(functools.partial(neighbour, pos), directions)
                    ),
                ),
            )
        )

    return len(set(high_points_reached(0, pos)))


high_points_trail_heads = filter(
    operator.truth, map(start_position_score, starting_positions)
)
print(f"Problem 1: {sum(high_points_trail_heads)}")


################################################################################################
# Problem 2
def start_position_score(pos):
    def num_trails_available(x, y, h):
        if h == 9:
            return 1

        score = 0
        for dir in directions:
            tx = x + dir[0]
            ty = y + dir[1]
            if pos_in_range_map[dir]((tx, ty)) and int(mountains[ty][tx]) == h + 1:
                score += num_trails_available(tx, ty, h + 1)
        return score

    (x, y) = pos
    return num_trails_available(x, y, 0)


trails_reached_trail_heads = list(
    itertools.filterfalse(
        lambda x: x == 0, map(start_position_score, starting_positions)
    )
)
print(f"Problem 2: {sum(trails_reached_trail_heads)}")
