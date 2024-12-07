import aocd

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
        [result, values] = data.split(":")
        self.result = int(result)
        self.values = list(map(int, values.split()))
        self.operators = ["+", "*"]

    def solve(self):
        num_values = len(self.values)

        def solve_impl(result, values_handled, partial_attempt):
            if values_handled == num_values:
                if result == partial_attempt:
                    return True
                return False
            elif partial_attempt >= result:
                return None

            for operator in self.operators:
                match operator:
                    case "+":
                        next_attempt = partial_attempt + self.values[values_handled]
                    case "*":
                        next_attempt = partial_attempt * self.values[values_handled]
                    case "|":
                        next_attempt = int(
                            str(partial_attempt) + str(self.values[values_handled])
                        )
                next_values_handled = values_handled + 1
                if solution := solve_impl(result, next_values_handled, next_attempt):
                    return solution

            return False

        return solve_impl(self.result, 0, 0)


class ExtendedCalibration(Calibration):
    def __init__(self, data):
        super().__init__(data)
        self.operators += ["|"]


calibrations = list(map(Calibration, data.splitlines()))
solvable_calibrations = list(map(Calibration.solve, calibrations))
solvable_calibrations_results = [
    c.result for c, s in zip(calibrations, solvable_calibrations) if s
]

print(f"Problem 1: {sum(solvable_calibrations_results)}")


extended_calibrations = list(map(ExtendedCalibration, data.splitlines()))
solvable_extended_calibrations = list(
    map(ExtendedCalibration.solve, extended_calibrations)
)
solvable_extended_calibrations_results = [
    c.result for c, s in zip(extended_calibrations, solvable_extended_calibrations) if s
]

print(f"Problem 2: {sum(solvable_extended_calibrations_results)}")
