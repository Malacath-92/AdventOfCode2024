import aocd
import itertools

import cli

sample_data = """\
2333133121414131402"""
data = sample_data if cli.sample else aocd.data

blocks = [
    str(id // 2) if id % 2 == 0 else "."
    for id, block_size in enumerate(data)
    for _ in range(int(block_size))
]
num_empty_blocks = blocks.count(".")


def get_next_non_empty_block(blocks, start):
    while blocks[start] == ".":
        start -= 1
    return start


def checksum(blocks):
    chk = 0
    for i, block in enumerate(blocks):
        if block != ".":
            chk += int(block) * i
    return chk


p1_blocks = blocks.copy()
last_non_empty_block = len(blocks) - 1
while p1_blocks[-num_empty_blocks:].count(".") < num_empty_blocks:
    first_empty_block = p1_blocks.index(".")
    last_non_empty_block = get_next_non_empty_block(p1_blocks, last_non_empty_block)
    p1_blocks[first_empty_block] = p1_blocks[last_non_empty_block]
    p1_blocks[last_non_empty_block] = "."


print(f"Problem 1: {checksum(blocks)}")
