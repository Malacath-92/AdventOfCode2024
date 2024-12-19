import aocd
import math
import functools
from typing import NamedTuple

# from heapq import heappop, heappush
from sortedcontainers import SortedList
from tqdm import tqdm as progress

import cli
from vector import Vector

sample_data = """\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""
data = sample_data if cli.sample else aocd.data

towels, patterns = data.split("\n\n")
towels = tuple(reversed(sorted(towels.split(", "), key=lambda t: len(t))))
patterns = patterns.splitlines()


@functools.cache
def count_towel_combinations(towels: tuple[str], pattern: str) -> int:
    eligible_towels = tuple(
        filter(lambda t: all(map(lambda s: s in pattern, t)), towels)
    )

    @functools.cache
    def count_towel_combinations(towels: tuple[str], pattern: str) -> int:
        if not pattern:
            return 1

        num = 0
        for towel in towels:
            if pattern.startswith(towel):
                num += count_towel_combinations(towels, pattern.removeprefix(towel))
        return num

    return count_towel_combinations(eligible_towels, pattern)


towel_combinations = list(
    map(functools.partial(count_towel_combinations, towels), progress(patterns))
)
towel_combinations = list(filter(None, towel_combinations))

################################################################################################
# Problem 1
print(f"Problem 1: {len(towel_combinations)}")


################################################################################################
# Problem 2
print(f"Problem 1: {sum(towel_combinations)}")
