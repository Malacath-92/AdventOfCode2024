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


################################################################################################
# Problem 1
@functools.cache
def find_towel_combination(towels: tuple[str], pattern: str) -> bool:
    eligible_towels = tuple(
        filter(lambda t: all(map(lambda s: s in pattern, t)), towels)
    )

    @functools.cache
    def find_towel_combination_impl(towels: tuple[str], pattern: str) -> bool:
        if not pattern:
            return True

        for towel in towels:
            if pattern.startswith(towel) and find_towel_combination_impl(
                towels, pattern.removeprefix(towel)
            ):
                return True
        return False

    return find_towel_combination_impl(eligible_towels, pattern)


possible_patterns = list(
    map(functools.partial(find_towel_combination, towels), progress(patterns))
)
possible_patterns = list(filter(None, possible_patterns))
print(f"Problem 1: {len(possible_patterns)}")


################################################################################################
# Problem 2
@functools.cache
def find_towel_combination(towels: tuple[str], pattern: str) -> int:
    eligible_towels = tuple(
        filter(lambda t: all(map(lambda s: s in pattern, t)), towels)
    )

    @functools.cache
    def find_towel_combination_impl(towels: tuple[str], pattern: str) -> int:
        if not pattern:
            return 1

        num = 0
        for towel in towels:
            if pattern.startswith(towel):
                num += find_towel_combination_impl(towels, pattern.removeprefix(towel))
        return num

    return find_towel_combination_impl(eligible_towels, pattern)


possible_patterns = list(
    map(functools.partial(find_towel_combination, towels), progress(patterns))
)
print(f"Problem 1: {sum(possible_patterns)}")
