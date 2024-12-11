import aocd
import operator
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
print(f"Problem 1: {sum(1 for _ in after_25_steps)}")


################################################################################################
# Problem 2
