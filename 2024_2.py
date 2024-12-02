import aocd
import collections
import itertools

import cli

sample_data = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""
data = sample_data if cli.sample else aocd.data

reports = [[int(n) for n in l.split()] for l in data.splitlines()]


def is_report_safe(report, with_dampener=False):
    def sliding_window(iterable, n):
        iterator = iter(iterable)
        window = collections.deque(itertools.islice(iterator, n - 1), maxlen=n)
        for x in iterator:
            window.append(x)
            yield tuple(window)

    def try_dampen(i):
        # strip off left level
        left_stripped = report.copy()
        del left_stripped[i]
        if is_report_safe(left_stripped):
            return True

        # strip off right level
        right_stripped = report.copy()
        del right_stripped[i + 1]
        if is_report_safe(right_stripped):
            return True

        # strip off first level
        first_stripped = report.copy()
        del first_stripped[0]
        if is_report_safe(first_stripped):
            return True

        # strip off second level
        second_stripped = report.copy()
        del second_stripped[1]
        if is_report_safe(second_stripped):
            return True

    last_diff = 0
    for i, [lhs, rhs] in enumerate(sliding_window(report, 2)):
        diff = rhs - lhs
        if abs(diff) < 1 or abs(diff) > 3:
            return try_dampen(i) if with_dampener else False
        if last_diff != 0 and last_diff / diff < 0:
            return try_dampen(i) if with_dampener else False
        last_diff = diff
    return True


safe_reports = [report for report in reports if is_report_safe(report)]
print(f"Problem 1: {len(safe_reports)}")

safe_reports = [report for report in reports if is_report_safe(report, True)]
print(f"Problem 2: {len(safe_reports)}")

