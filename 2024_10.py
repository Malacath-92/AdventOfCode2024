import aocd
import itertools

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


################################################################################################
# Problem 1
def start_position_score(pos):
    def high_points_reached(x, y, h):
        if h == 9:
            return set([(x, y)])

        high_points = set()
        for dir in directions:
            tx = x + dir[0]
            ty = y + dir[1]
            if pos_in_range_map[dir]((tx, ty)) and int(mountains[ty][tx]) == h + 1:
                high_points.update(high_points_reached(tx, ty, h + 1))
        return high_points

    (x, y) = pos
    return len(high_points_reached(x, y, 0))


starting_positions = list(
    map(flat_idx_to_coords, [i for i, h in enumerate(flat_data) if h == "0"])
)
trail_heads = list(
    itertools.filterfalse(
        lambda x: x == 0, map(start_position_score, starting_positions)
    )
)

print(f"Problem 1: {sum(trail_heads)}")
