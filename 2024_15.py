import aocd
import re
from enum import Enum
from typing import NamedTuple
from tqdm import tqdm as progress

import cli

sample_data = """\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""
data = sample_data if cli.sample else aocd.data
[floor_plan, moves] = data.split("\n\n")

flat_floor_plan = floor_plan.replace("\n", "")
floor_plan = list(map(list, floor_plan.splitlines()))
width = len(floor_plan[0])
height = len(floor_plan)

flat_idx_to_coords = lambda i: Vector(i % width, i // width)
is_in_range = lambda p: p.x >= 0 and p.y >= 0 and p.x < width and p.y < height

moves = "".join(moves.splitlines())


class Vector(NamedTuple):
    x: int
    y: int

    def __add__(lhs, rhs):
        return Vector(lhs.x + rhs.x, lhs.y + rhs.y)

    def __sub__(lhs, rhs):
        return Vector(lhs.x - rhs.x, lhs.y - rhs.y)

    def __mul__(lhs, rhs: int):
        return Vector(lhs.x * rhs, lhs.y * rhs)

    def __truediv__(lhs, rhs: int):
        return Vector(lhs.x / rhs, lhs.y / rhs)


directions = {
    ">": Vector(+1, 0),
    "v": Vector(0, +1),
    "<": Vector(-1, 0),
    "^": Vector(0, -1),
}

def print_floor(floor_plan: list[list[str]]):
    print(f"{"\n".join(map(lambda x: "".join(x), floor_plan))}\n")


################################################################################################
# Problem 1
def try_move(floor_plan: list[list[str]], pos: Vector, dir: Vector) -> bool:
    target_pos = pos + dir
    if is_in_range(target_pos):
        target_object = floor_plan[target_pos.y][target_pos.x]
        if target_object == "@":
            raise "Wtf just happened???"
        elif target_object == "#":
            return False
        elif target_object == "O":
            if try_move(floor_plan, target_pos, dir):
                floor_plan[target_pos.y][target_pos.x] = floor_plan[pos.y][pos.x]
                floor_plan[pos.y][pos.x] = "."
                return True
            return False
        elif target_object == ".":
            floor_plan[target_pos.y][target_pos.x] = floor_plan[pos.y][pos.x]
            floor_plan[pos.y][pos.x] = "."
            return True
        else:
            raise "Bruv..."
    return False


robot_pos = flat_idx_to_coords(flat_floor_plan.find("@"))

result_floor_plan = list(map(list.copy, floor_plan))
for op in moves:
    dir = directions[op]
    if try_move(result_floor_plan, robot_pos, dir):
        robot_pos = robot_pos + dir

flat_result_floor_plan = "".join(map(lambda x: "".join(x), result_floor_plan))
box_coordinates = map(lambda x: flat_idx_to_coords(x.regs[0][0]), re.finditer("O", flat_result_floor_plan))
gps_values = map(lambda p: 100 * p.y + p.x, box_coordinates)

print(f"Problem 1: {sum(gps_values)}")


################################################################################################
# Problem 2
def widen_row(row: list[str]):
    orig_len = len(row)

    row = row.copy()
    for i in range(orig_len):
        obj = row[2*i]
        if obj == "@":
            row[2*i + 1:2*i + 1] = "."
        elif obj == "O":
            row[2*i:2*i + 1] = list("[]")
        else:
            row[2*i+1:2*i + 1] = obj
    return row
widened_floor_plan = list(map(widen_row, floor_plan))

width = width * 2
flat_idx_to_coords = lambda i: Vector(i % width, i // width)
is_in_range = lambda p: p.x >= 0 and p.y >= 0 and p.x < width and p.y < height

def try_move(floor_plan: list[list[str]], pos: Vector, dir: Vector, dry: bool = False) -> bool:
    target_pos = pos + dir
    if is_in_range(target_pos):
        target_object = floor_plan[target_pos.y][target_pos.x]
        if target_object == "@":
            raise "Wtf just happened???"
        elif target_object == "#":
            return False
        elif target_object in "[]":
            if dir.y == 0:
                # moving one half into another, treat like normal
                if try_move(floor_plan, target_pos, dir, dry):
                    if not dry:
                        floor_plan[target_pos.y][target_pos.x] = floor_plan[pos.y][pos.x]
                        floor_plan[pos.y][pos.x] = "."
                    return True
            else:
                other_dir = Vector(1 if target_object == "[" else -1, 0)
                other_half = target_pos + other_dir

                # moving only one half up, do a dry run of the other half and if success try moving this half up
                # if all of that succeeds actually move the other half up
                other_can_move = try_move(floor_plan, other_half, dir, True)
                if other_can_move and try_move(floor_plan, target_pos, dir, dry):
                    if not dry:
                        try_move(floor_plan, other_half, dir, False)
                        floor_plan[target_pos.y][target_pos.x] = floor_plan[pos.y][pos.x]
                        floor_plan[pos.y][pos.x] = "."
                    return True
            return False
        elif target_object == ".":
            if not dry:
                floor_plan[target_pos.y][target_pos.x] = floor_plan[pos.y][pos.x]
                floor_plan[pos.y][pos.x] = "."
            return True
        else:
            raise "Bruv..."
    return False

flat_widened_floor_plan = "".join(map(lambda x: "".join(x), widened_floor_plan))
robot_pos = flat_idx_to_coords(flat_widened_floor_plan.find("@"))

for op in moves:
    dir = directions[op]
    if try_move(widened_floor_plan, robot_pos, dir):
        robot_pos = robot_pos + dir

flat_widened_floor_plan = "".join(map(lambda x: "".join(x), widened_floor_plan))
box_coordinates = map(lambda x: flat_idx_to_coords(x.regs[0][0]), re.finditer(r"\[\]", flat_widened_floor_plan))
gps_values = map(lambda p: 100 * p.y + p.x, box_coordinates)

print(f"Problem 2: {sum(gps_values)}")

################################################################################################
# Interactive
if cli.verbose:
    import os
    import getkey

    class Keys(Enum):
        RIGHT = 'àM'
        LEFT  = 'àK'
        UP  = 'àH'
        DOWN  = 'àP'

    widened_floor_plan = list(map(widen_row, floor_plan))
    flat_widened_floor_plan = "".join(map(lambda x: "".join(x), widened_floor_plan))
    robot_pos = flat_idx_to_coords(flat_widened_floor_plan.find("@"))

    print_floor(widened_floor_plan)

    while key := getkey.getkey():
        
        match key:
            case Keys.RIGHT.value:
                op = '>'
            case Keys.LEFT.value:
                op = '<'
            case Keys.UP.value:
                op = '^'
            case Keys.DOWN.value:
                op = 'v'
                
        dir = directions[op]
        if try_move(widened_floor_plan, robot_pos, dir):
            robot_pos = robot_pos + dir
        os.system('cls')
        print_floor(widened_floor_plan)
