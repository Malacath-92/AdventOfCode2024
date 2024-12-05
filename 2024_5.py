import aocd
import collections
import itertools
import functools

import cli

sample_data = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
data = sample_data if cli.sample else aocd.data

order_rules = [list(map(int, l.split("|"))) for l in data.split("\n\n")[0].splitlines()]
productions = [list(map(int, l.split(","))) for l in data.split("\n\n")[1].splitlines()]


def sliding_window(iterable, n):
    iterator = iter(iterable)
    window = collections.deque(itertools.islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


def is_right_order(production):
    for [lhs, rhs] in sliding_window(production, 2):
        rhs_rules = [right for [left, right] in order_rules if left == rhs]
        if lhs in rhs_rules:
            return False
    return True


right_order_productions = [prod for prod in productions if is_right_order(prod)]
right_order_middle_pages = [prod[len(prod) // 2] for prod in right_order_productions]
print(f"Problem 1: {sum(right_order_middle_pages)}")


def fix_order(production):
    def compare(lhs, rhs):
        rhs_rules = [right for [left, right] in order_rules if left == rhs]
        return -1 if lhs in rhs_rules else 1

    return sorted(production, key=functools.cmp_to_key(compare))


fixed_productions = [
    fix_order(prod) for prod in productions if not is_right_order(prod)
]
fixed_middle_pages = [prod[len(prod) // 2] for prod in fixed_productions]
print(f"Problem 2: {sum(fixed_middle_pages)}")
