import aocd
import functools

import cli

sample_data = """\
1
10
100
2024"""
data = sample_data if cli.sample else aocd.data

initial_values = list(map(int, data.splitlines()))


@functools.cache
def trans(val: int) -> int:
    val = ((val * 64) ^ val) % 16777216
    val = ((val // 32) ^ val) % 16777216
    val = ((val * 2048) ^ val) % 16777216
    return val


################################################################################################
# Problem 1
@functools.cache
def calculate_nth_trans(val: int, n: int) -> int:
    for _ in range(n):
        val = trans(val)
    return val


values_2000th = list(
    map(functools.partial(calculate_nth_trans, n=2000), initial_values)
)
print(f"Problem 1: {sum(values_2000th)}")


################################################################################################
# Problem 2
