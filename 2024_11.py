import aocd
import itertools
import functools
from typing import Iterable

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
def multi_steps(steps: int, stones: Iterable[int]) -> dict[int, int]:
    stone_counts: dict[int, int] = {}

    def decrement(stone: int, num: int) -> None:
        if stone not in stone_counts:
            raise "Can't remove stone that hasn't been counted yet..."
        elif stone_counts[stone] < num:
            raise "Can't remove stone more times than it has been counted so far..."
        else:
            stone_counts[stone] -= num

    def increment(stone: int, num: int) -> None:
        if stone not in stone_counts:
            stone_counts[stone] = num
        else:
            stone_counts[stone] += num

    for stone in stones:
        increment(stone, 1)

    def single_step(stone: int, num: int) -> None:
        decrement(stone, num)
        if stone == 0:
            increment(1, num)
        elif len(str(stone)) % 2 == 0:
            stone_str = str(stone)
            half_len = len(stone_str) // 2
            increment(int(stone_str[:half_len]), num)
            increment(int(stone_str[half_len:]), num)
        else:
            increment(stone * 2024, num)

    for _ in range(steps):
        old_counts = stone_counts.copy()
        for stone, num in old_counts.items():
            single_step(stone, num)
    return stone_counts


after_75_steps = multi_steps(75, stones)
print(f"Problem 2: {sum(after_75_steps.values())}")
