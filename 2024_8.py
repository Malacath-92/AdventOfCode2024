import aocd
import re
import itertools

import cli

sample_data = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""
data = sample_data if cli.sample else aocd.data
flat_data = "".join(data.splitlines())

city = data.splitlines()
width = len(city[0])
height = len(city)
flat_idx_to_coords = lambda i: (i % width, i // width)
is_in_range = lambda p: p[0] >= 0 and p[1] >= 0 and p[0] < width and p[1] < height

antenna_types = set(re.findall(r"[^\.]", flat_data))
antenna_positions = {
    antenna_type: list(
        map(
            lambda x: flat_idx_to_coords(x.regs[0][0]),
            re.finditer(antenna_type, flat_data),
        )
    )
    for antenna_type in antenna_types
}

anti_nodes = [[set() for _ in range(width)] for _ in range(height)]

for antenna_type, positions in antenna_positions.items():
    pairwise_positions = itertools.product(positions, positions)
    for l, r in pairwise_positions:
        if l == r:
            continue

        d = (l[0] - r[0], l[1] - r[1])
        anti_node_l = (l[0] + d[0], l[1] + d[1])
        if is_in_range(anti_node_l):
            anti_nodes[anti_node_l[1]][anti_node_l[0]].add(antenna_type)
        anti_node_r = (r[0] - d[0], r[1] - d[1])
        if is_in_range(anti_node_r):
            anti_nodes[anti_node_r[1]][anti_node_r[0]].add(antenna_type)

anti_nodes_flat = list(itertools.chain.from_iterable(anti_nodes))
num_positions_with_anti_nodes = len(anti_nodes_flat) - anti_nodes_flat.count(set())
print(f"Problem 1: {num_positions_with_anti_nodes}")


real_anti_nodes = [[set() for _ in range(width)] for _ in range(height)]

for antenna_type, positions in antenna_positions.items():
    pairwise_positions = itertools.product(positions, positions)
    for l, r in pairwise_positions:
        if l == r:
            continue

        d = (l[0] - r[0], l[1] - r[1])
        while d[0] % 2 == 0 and d[1] % 2 == 0:
            d = (d[0] // 2, d[1] // 2)

        anti_node_l = l
        while is_in_range(anti_node_l):
            real_anti_nodes[anti_node_l[1]][anti_node_l[0]].add(antenna_type)
            anti_node_l = (anti_node_l[0] + d[0], anti_node_l[1] + d[1])

        anti_node_r = (l[0] - d[0], l[1] - d[1])
        while is_in_range(anti_node_r):
            real_anti_nodes[anti_node_r[1]][anti_node_r[0]].add(antenna_type)
            anti_node_r = (anti_node_r[0] - d[0], anti_node_r[1] - d[1])

real_anti_nodes_flat = list(itertools.chain.from_iterable(real_anti_nodes))
num_positions_with_real_anti_nodes = len(
    real_anti_nodes_flat
) - real_anti_nodes_flat.count(set())
print(f"Problem 1: {num_positions_with_real_anti_nodes}")
