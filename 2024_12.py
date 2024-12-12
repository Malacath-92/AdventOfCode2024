import aocd
import re
import operator
import functools
import itertools
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
regions: list[list[Coordinate]] = []


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
