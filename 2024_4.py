import aocd
import enum
from functools import reduce
from operator import mul

import cli

sample_data = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
data = sample_data if cli.sample else aocd.data


word_puzzle = data.splitlines()
width, height = len(word_puzzle[0]), len(word_puzzle)

directions = [
    (-1, 0),
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, -1),
    (1, -1),
    (1, 1),
    (-1, 1),
]
num_xmas = 0
for x in range(width):
    for y in range(height):
        if word_puzzle[y][x] != "X":
            continue
        for dir in directions:
            w = "X"
            for i in range(1, 4):
                x2 = x + dir[0] * i
                y2 = y + dir[1] * i
                if x2 < 0 or y2 < 0 or x2 >= width or y2 >= height:
                    break
                w += word_puzzle[y2][x2]
            if w == "XMAS":
                num_xmas += 1
print(f"Problem 1: {num_xmas}")

valid_mas = ("MAS", "SAM")
num_cross_mas = 0
for x in range(1, width - 1):
    for y in range(1, height - 1):
        if word_puzzle[y][x] != "A":
            continue
        mas_1 = word_puzzle[y - 1][x - 1] + "A" + word_puzzle[y + 1][x + 1]
        mas_2 = word_puzzle[y - 1][x + 1] + "A" + word_puzzle[y + 1][x - 1]
        if mas_1 in valid_mas and mas_2 in valid_mas:
            num_cross_mas += 1
print(f"Problem 2: {num_cross_mas}")
