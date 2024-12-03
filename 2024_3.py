import aocd
import re
from functools import reduce
from operator import mul

import cli

sample_data = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
data = sample_data if cli.sample else aocd.data

instructions = [map(int, inst) for inst in re.findall(r"mul\((\d+),(\d+)\)", data)]
multiplications = [reduce(mul, instruction) for instruction in instructions]
print(f"Problem 1: {sum(multiplications)}")

sample_data = (
    "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
)
data = sample_data if cli.sample else aocd.data

data = re.sub("(don't\(\)).*?(do\(\))", "", "".join(data.splitlines()))
data = data.split("don't")[0]
instructions = [map(int, inst) for inst in re.findall(r"mul\((\d+),(\d+)\)", data)]
multiplications = [reduce(mul, instruction) for instruction in instructions]
print(f"Problem 2: {sum(multiplications)}")
