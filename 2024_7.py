import aocd
import operator

import cli

sample_data = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""
data = sample_data if cli.sample else aocd.data


class Calibration:
    def __init__(self, data):
        [self.result, self.values] = data.split(":")
        self.result = int(self.result)
        self.values = list(map(int, self.values.split()))

    def solve(self):
        operators = [
            operator.add,
            operator.mul,
        ]

        def solve_impl(result, values, partial_attempt, partial_operators):
            if len(values) == 0:
                if result == partial_attempt:
                    return partial_operators
                return None

            for operator in operators:
                next_attempt = operator(partial_attempt, values[0])
                next_values = values[1:]
                next_operators = partial_operators + [operator]
                if solution := solve_impl(
                    result, next_values, next_attempt, next_operators
                ):
                    return solution

            return None

        return solve_impl(self.result, self.values, 0, [])


calibrations = list(map(Calibration, data.splitlines()))
solved_calibrations = list(map(Calibration.solve, calibrations))
solved_calibrations_results = [
    c.result for c, s in zip(calibrations, solved_calibrations) if s is not None
]

print(f"Problem 1: {sum(solved_calibrations_results)}")
