import aocd
import functools
import itertools
from frozendict import frozendict

import cli
from vector import Vector

sample_data = """\
029A
980A
179A
456A
379A"""
data = sample_data if cli.sample else aocd.data

codes = data.splitlines()

directions = frozendict(
    {
        "<": Vector(-1, 0),
        ">": Vector(+1, 0),
        "^": Vector(0, -1),
        "v": Vector(0, +1),
    }
)

KeyPad = dict[str, Vector]
Code = str

door_pad: KeyPad = frozendict(
    {
        "A": Vector(2, 3),
        "0": Vector(1, 3),
        "1": Vector(0, 2),
        "2": Vector(1, 2),
        "3": Vector(2, 2),
        "4": Vector(0, 1),
        "5": Vector(1, 1),
        "6": Vector(2, 1),
        "7": Vector(0, 0),
        "8": Vector(1, 0),
        "9": Vector(2, 0),
    }
)

robot_pad: KeyPad = frozendict(
    {
        "A": Vector(2, 0),
        "^": Vector(1, 0),
        "<": Vector(0, 1),
        "v": Vector(1, 1),
        ">": Vector(2, 1),
    }
)

robot_start = "A"


@functools.cache
def get_possible_paths(pad: KeyPad, pos: Vector, target: Vector) -> list[Code]:
    if pos == target:
        return ["A"]

    diff = target - pos

    horizontal_moves = ("<" if diff.x < 0 else ">") * abs(diff.x)
    if diff.y == 0:
        return [horizontal_moves + "A"]

    vertical_moves = ("^" if diff.y < 0 else "v") * abs(diff.y)
    if diff.x == 0:
        return [vertical_moves + "A"]

    def is_valid_path(start_pos: Vector, code: Code):
        pos = start_pos
        for c in code:
            pos = pos + directions[c]
            if pos not in pad.values():
                return False
        return True

    basic_moves = vertical_moves + horizontal_moves
    return [
        "".join(moves) + "A"
        for moves in set(itertools.permutations(basic_moves))
        if is_valid_path(pos, moves)
    ]


@functools.cache
def get_cost_for_path(path: Code, depth: int) -> Code:
    if depth == 0:
        return len(path)

    return sum(
        get_best_move_cost(from_key, to_key, depth)
        for from_key, to_key in zip("A" + path[:-1], path)
    )


@functools.cache
def get_best_move_cost(from_key: str, to_key: str, depth: int) -> Code:
    from_pos = robot_pad[from_key]
    to_pos = robot_pad[to_key]
    if depth == 0:
        return from_pos.manhattan_dist(to_pos)

    possible_paths = get_possible_paths(robot_pad, from_pos, to_pos)
    if len(possible_paths) == 1:
        return get_cost_for_path(possible_paths[0], depth - 1)
    return min(get_cost_for_path(path, depth - 1) for path in possible_paths)


def get_best_manual_input_cost(robots: int, code: Code) -> int:
    cost = 0
    for from_key, to_key in zip("A" + code[:-1], code):
        from_pos = door_pad[from_key]
        to_pos = door_pad[to_key]

        possible_paths = get_possible_paths(door_pad, from_pos, to_pos)
        min_cost, min_path = min(
            (get_cost_for_path(path, robots - 1), path) for path in possible_paths
        )
        cost += min_cost

    return cost


def calc_complexity(code: Code, input_cost: int) -> int:
    return int(code[:-1]) * input_cost


################################################################################################
# Problem 1
manual_inputs = list(map(functools.partial(get_best_manual_input_cost, 3), codes))
complexities = list(itertools.starmap(calc_complexity, zip(codes, manual_inputs)))
print(f"Problem 1: {sum(complexities)}")


################################################################################################
# Problem 2
manual_inputs = list(map(functools.partial(get_best_manual_input_cost, 26), codes))
complexities = list(itertools.starmap(calc_complexity, zip(codes, manual_inputs)))
print(f"Problem 1: {sum(complexities)}")
