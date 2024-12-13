import aocd
from typing import NamedTuple
from tqdm import tqdm as progress

import cli

sample_data = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""
data = sample_data if cli.sample else aocd.data


class ClawButton:
    def __init__(self, setup: str):
        [name, controls] = setup.split(":")

        self.name = name.split()[1]

        controls = controls.split(",")
        self.delta = (
            int(controls[0].split("+")[1].strip()),
            int(controls[1].split("+")[1].strip()),
        )


class Game:
    def __init__(self, setup: str):
        [a_button, b_button, price] = setup.splitlines()

        self.a_button = ClawButton(a_button)
        self.b_button = ClawButton(b_button)

        price_placement = price.split(":")[1].split(",")
        self.price_placement = (
            int(price_placement[0].split("=")[1].strip()),
            int(price_placement[1].split("=")[1].strip()),
        )


class GameSolution(NamedTuple):
    a_presses: int
    b_presses: int

    def tokens_needed(self) -> int:
        return self.a_presses * 3 + self.b_presses


games = list(map(Game, data.split("\n\n")))


################################################################################################
# Problem 1
def solve_game(game: Game) -> GameSolution | None:
    t = game.price_placement
    da = game.a_button.delta
    db = game.b_button.delta

    # Find solution to the linear equation
    # t[0] = a_presses * da[0] + b_presses * db[0]
    # t[1] = a_presses * da[1] + b_presses * db[1]
    a_presses = (
        (t[1] * db[0] - t[0] * db[1])
        / (db[1] * db[0])
        / (da[1] / db[1] - da[0] / db[0])
    )
    b_presses = (t[0] - a_presses * da[0]) / db[0]

    # Round to nearest integer and see if it solves
    a_presses = int(round(a_presses))
    b_presses = int(round(b_presses))
    t0 = a_presses * da[0] + b_presses * db[0]
    t1 = a_presses * da[1] + b_presses * db[1]
    if t0 != t[0] or t1 != t[1]:
        return None

    return GameSolution(a_presses, b_presses)


solutions = list(filter(None, map(solve_game, games)))
tokens_used = list(map(GameSolution.tokens_needed, solutions))
print(f"Problem 1: {sum(tokens_used)}")

################################################################################################
# Problem 2
