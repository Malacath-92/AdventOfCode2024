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


def is_report_safe(report):
    def sliding_window(iterable, n):
        iterator = iter(iterable)
        window = collections.deque(itertools.islice(iterator, n - 1), maxlen=n)
        for x in iterator:
            window.append(x)
            yield tuple(window)

    last_diff = 0
    for [lhs, rhs] in sliding_window(report, 2):
        diff = rhs - lhs
        if abs(diff) < 1 or abs(diff) > 3:
            return False
        if last_diff != 0 and last_diff / diff < 0:
            return False
        last_diff = diff
    return True


safe_reports = [report for report in reports if is_report_safe(report)]
print(f"Problem 1: {len(safe_reports)}")

