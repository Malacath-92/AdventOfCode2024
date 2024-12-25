import aocd
import itertools
import functools
from typing import Iterable
from tqdm import tqdm as progress

import cli


sample_data = """\
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""
data = sample_data if cli.sample else aocd.data

keys_and_locks = list(map(str.splitlines, data.split("\n\n")))
height = len(keys_and_locks[0])
width = len(keys_and_locks[0][0])

keys = list(filter(lambda s: all(t == "." for t in s[0]), keys_and_locks))
locks = list(filter(lambda s: all(t == "#" for t in s[0]), keys_and_locks))


def to_height_field(key_or_lock: list[str], key: bool):
    search = "#" if key else "."
    height_field = []
    for x in range(width):
        for y in range(height):
            if key_or_lock[y + 1][x] == search:
                height_field.append(height - y - 2 if key else y)
                break
    return height_field


keys = list(map(functools.partial(to_height_field, key=True), keys))
locks = list(map(functools.partial(to_height_field, key=False), locks))


################################################################################################
# Problem 1
def vec_add(lhs: Iterable, rhs: Iterable) -> Iterable:
    return itertools.starmap(lambda x, y: x + y, zip(lhs, rhs))


matching_pairs = list(
    filter(
        lambda l: all(x < height - 1 for x in l),
        itertools.starmap(vec_add, itertools.product(keys, locks)),
    )
)
print(f"Problem 1: {len(matching_pairs)}")

################################################################################################
# Problem 2
print("Problem 2: I'm freeee")
