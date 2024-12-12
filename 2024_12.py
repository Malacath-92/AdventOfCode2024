import aocd
import re
import operator
import functools
import itertools
from typing import NamedTuple
from tqdm import tqdm as progress

import cli

sample_data = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""
data = sample_data if cli.sample else aocd.data

gardens = data.splitlines()
width = len(gardens[0])
height = len(gardens)
flat_idx_to_coords = lambda i: (i % width, i // width)
is_in_range = lambda p: p[0] >= 0 and p[1] >= 0 and p[0] < width and p[1] < height
get_neighbour = lambda pos, dir: (pos[0] + dir[0], pos[1] + dir[1])

directions = [
    (-1, 0),
    (+1, 0),
    (0, -1),
    (0, +1),
]

types = set(re.findall(r"\w", data))

Coordinate = tuple[int, int]
RegionId = int
RegionType = str
Region = list[Coordinate]
RegionsMap = list[list[RegionId | None]]

################################################################################################
# Problem 1
regions_map: RegionsMap = [[None] * width for _ in range(height)]
regions: list[Region] = []


def find_region_at(regions_map: RegionsMap, pos: Coordinate) -> Region | None:
    (x, y) = pos
    if regions_map[y][x] is None:
        region_type = gardens[y][x]

        def flood_fill(
            regions_map: RegionsMap,
            pos: Coordinate,
            id: RegionId,
            region_type: RegionType,
        ) -> Region:
            coordinates: list[Coordinate] = [pos]
            (x, y) = pos
            regions_map[y][x] = id
            for neighbour in filter(
                is_in_range, map(functools.partial(get_neighbour, pos), directions)
            ):
                (nx, ny) = neighbour
                if regions_map[ny][nx] is None and gardens[ny][nx] == region_type:
                    coordinates.extend(
                        flood_fill(regions_map, neighbour, id, region_type)
                    )
            return coordinates

        new_id = len(regions)
        return flood_fill(regions_map, pos, new_id, region_type)


def compute_region_circumference(region: Region):
    circumference = 0
    (x0, y0) = region[0]
    region_type = regions_map[y0][x0]
    for pos in region:
        for neighbour in map(functools.partial(get_neighbour, pos), directions):
            (nx, ny) = neighbour
            if not is_in_range(neighbour) or regions_map[ny][nx] != region_type:
                circumference += 1
    return circumference


print("Finding Regions...")
for i in progress(range(0, width * height)):
    pos = flat_idx_to_coords(i)
    if new_region := find_region_at(regions_map, pos):
        regions.append(new_region)

print("Computing Areas...")
region_areas = [len(region) for region in progress(regions)]

print("Computing Circumferences...")
region_circumferences = [
    compute_region_circumference(region) for region in progress(regions)
]

print(
    f"Problem 1: {sum(itertools.starmap(operator.mul, zip(region_areas, region_circumferences)))}"
)


################################################################################################
# Problem 2
def compute_region_sides(region: Region):
    # Coordinates of edges point to the vertices between cells
    # where the top-left corner of a cell is the same coordinate as the cell
    # and edges always go clock-wise
    class Edge(NamedTuple):
        start: Coordinate
        end: Coordinate

        @property
        def dir(self):
            sign = lambda x: 0 if x == 0 else x / abs(x)
            return (
                sign(self.end[0] - self.start[0]),
                sign(self.end[1] - self.start[1]),
            )

    region_id = regions_map[region[0][1]][region[0][0]]

    edges: list[Edge] = []
    for pos in sorted(region):
        for dir in directions:
            neighbour = get_neighbour(pos, dir)
            (nx, ny) = neighbour
            if not is_in_range(neighbour) or regions_map[ny][nx] != region_id:

                def start_pos(pos, dir):
                    match dir:
                        case (0, -1):
                            return pos
                        case (1, 0):
                            return (pos[0] + 1, pos[1])
                        case (0, 1):
                            return (pos[0] + 1, pos[1] + 1)
                        case (-1, 0):
                            return (pos[0], pos[1] + 1)

                edge_start = start_pos(pos, dir)
                edge_dir = (-dir[1], dir[0])
                edges.append(
                    Edge(
                        edge_start,
                        get_neighbour(edge_start, edge_dir),
                    )
                )

    def combine_adjacent_edges(edges: list[Edge]) -> list[Edge]:
        handled_edges: list[bool] = [False] * len(edges)
        combined_edges: list[Edge] = []

        for i, edge in enumerate(edges):
            if handled_edges[i]:
                continue

            def find_adjacent_edge(edge: Edge) -> Edge | None:
                for i, (handled, other_edge) in enumerate(zip(handled_edges, edges)):
                    if handled or edge == other_edge:
                        continue

                    if edge.dir == other_edge.dir and (
                        edge.start == other_edge.end or edge.end == other_edge.start
                    ):
                        handled_edges[i] = True
                        return other_edge

            combined_edge = edge
            while adjacent_edge := find_adjacent_edge(combined_edge):
                if combined_edge.start == adjacent_edge.end:
                    combined_edge = Edge(
                        adjacent_edge.start,
                        combined_edge.end,
                    )
                elif combined_edge.end == adjacent_edge.start:
                    combined_edge = Edge(
                        combined_edge.start,
                        adjacent_edge.end,
                    )

            combined_edges.append(combined_edge)

        return combined_edges

    edges = combine_adjacent_edges(edges)
    return len(edges)


print("Computing Num Sides...")
region_sides = [compute_region_sides(region) for region in progress(regions)]

print(
    f"Problem 2: {sum(itertools.starmap(operator.mul, zip(region_areas, region_sides)))}"
)
