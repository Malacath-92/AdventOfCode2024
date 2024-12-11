import aocd
import itertools
import functools
from tqdm import tqdm as progress
from typing import Iterable, DefaultDict

import cli

sample_data = """\
125 17"""
data = sample_data if cli.sample else aocd.data

stones = list(map(int, data.split()))


################################################################################################
# Problem 1
def single_step(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        stone_str = str(stone)
        half_len = len(stone_str) // 2
        return [int(stone_str[:half_len]), int(stone_str[half_len:])]
    else:
        return [stone * 2024]


def multi_steps(steps: int, stones: Iterable[int]) -> Iterable[int]:
    if steps == 0:
        return stones

    return itertools.chain.from_iterable(
        map(
            functools.partial(multi_steps, steps - 1),
            map(single_step, stones),
        )
    )


after_25_steps = multi_steps(25, stones)
print(f"Problem 1: {len(list(after_25_steps))}")


################################################################################################
# Problem 2
def multi_steps(steps: int, stones: Iterable[int]) -> DefaultDict[int, int]:
    stone_counts = DefaultDict[int, int](lambda: 0)

    for stone in stones:
        stone_counts[stone] += 1

    def single_step(stone: int, num: int) -> None:
        stone_counts[stone] -= num
        if stone == 0:
            stone_counts[1] += num
        elif len(str(stone)) % 2 == 0:
            stone_str = str(stone)
            half_len = len(stone_str) // 2
            stone_counts[int(stone_str[:half_len])] += num
            stone_counts[int(stone_str[half_len:])] += num
        else:
            stone_counts[stone * 2024] += num

    for _ in progress(range(steps)):
        old_counts = stone_counts.copy()
        for stone, num in old_counts.items():
            single_step(stone, num)
    return stone_counts


after_75_steps = multi_steps(75, stones)
print(f"Problem 2: {sum(after_75_steps.values())}")
