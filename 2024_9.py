import aocd
import collections

import cli

sample_data = """\
2333133121414131402"""
data = sample_data if cli.sample else aocd.data


def checksum(blocks):
    chk = 0
    for i, block in enumerate(blocks):
        if block != ".":
            chk += int(block) * i
    return chk


################################################################################################
# Problem 1
def get_next_non_empty_block(blocks, start):
    while blocks[start] == ".":
        start -= 1
    return start


blocks = [
    str(id // 2) if id % 2 == 0 else "."
    for id, block_size in enumerate(data)
    for _ in range(int(block_size))
]
num_empty_blocks = blocks.count(".")

blocks = blocks.copy()
last_non_empty_block = len(blocks) - 1
while blocks[-num_empty_blocks:].count(".") < num_empty_blocks:
    first_empty_block = blocks.index(".")
    last_non_empty_block = get_next_non_empty_block(blocks, last_non_empty_block)
    blocks[first_empty_block] = blocks[last_non_empty_block]
    blocks[last_non_empty_block] = "."

print(f"Problem 1: {checksum(blocks)}")


################################################################################################
# Problem 2
def make_entry(size, idx):
    class Entry:
        def __init__(self, size, idx):
            self.size = size
            self.id = idx // 2 if idx % 2 == 0 else -1

        def __str__(self):
            return str(self.id) if self.id >= 0 else "."

    return Entry(size, idx)


disk = [make_entry(int(f), i) for i, f in enumerate(data)]
file_idx = len(disk) - 1 if len(disk) % 2 != 0 else len(disk) - 2
while file_idx > 0:
    # Find index of empty block range that fits this file
    empty_idx = 1
    while empty_idx < file_idx and disk[empty_idx].size < disk[file_idx].size:
        empty_idx += 2

    # Move file if we found an index
    if empty_idx < file_idx:
        # Insert file entry in the new position
        disk[empty_idx : empty_idx + 1] = [
            make_entry(0, -1),
            disk[file_idx],
            make_entry(disk[empty_idx].size - disk[file_idx].size, -1),
        ]
        file_idx += 2

        # Remove file entry
        disk[file_idx - 1].size += disk[file_idx].size
        del disk[file_idx]

        # Compact adjacent empty entries
        if file_idx < len(disk) - 1:
            disk[file_idx - 1].size += disk[file_idx].size
            del disk[file_idx]

        # Remove zero-length entries at the back of the list
        if disk[-1] == 0:
            del disk[-1]

    file_idx -= 2

defragmented_blocks = [str(block) for block in disk for _ in range(block.size)]
print(f"Problem 2: {checksum(defragmented_blocks)}")
