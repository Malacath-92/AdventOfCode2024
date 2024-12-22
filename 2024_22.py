import aocd
import functools

import cli


@functools.cache
def trans(val: int) -> int:
    val = ((val * 64) ^ val) % 16777216
    val = ((val // 32) ^ val) % 16777216
    val = ((val * 2048) ^ val) % 16777216
    return val


################################################################################################
# Problem 1
sample_data = """\
1
10
100
2024"""
data = sample_data if cli.sample else aocd.data
initial_values = list(map(int, data.splitlines()))


@functools.cache
def calculate_nth_trans(val: int, n: int) -> int:
    for _ in range(n):
        val = trans(val)
    return val


values_2000th = list(
    map(functools.partial(calculate_nth_trans, n=2000), initial_values)
)
print(f"Problem 1: {sum(values_2000th)}")


################################################################################################
# Problem 2
sample_data = """\
1
2
3
2024"""
data = sample_data if cli.sample else aocd.data
initial_values = list(map(int, data.splitlines()))


type TransList = list[int]
type DiffList = list[int]
type TransDiffSequence = tuple[int, int, int, int]
type TransDiffSequenceMap = dict[TransDiffSequence, int]


@functools.cache
def calculate_trans_list_to_nth(val: int, n: int) -> TransList:
    trans_list = [val]
    for _ in range(n):
        val = trans(val)
        trans_list.append(val)
    trans_list = list(map(lambda x: x % 10, trans_list))
    return trans_list


def calculate_trans_diffs(trans_list: TransList) -> DiffList:
    trans_diff = list([y - x for x, y in zip(trans_list, trans_list[1:])])
    return trans_diff


def compute_trans_diff_sequence_maps(
    trans_lists: list[TransList],
    diff_lists: list[DiffList],
) -> list[TransDiffSequenceMap]:
    sequence_maps: list[TransDiffSequenceMap] = []
    for trans_list, diffs in zip(trans_lists, diff_lists):
        sequence_map: TransDiffSequenceMap = {}
        for i, trans in enumerate(trans_list):
            if i < 4:
                continue

            trans_diff_sequence = tuple(diffs[i - 4 : i])
            if trans_diff_sequence not in sequence_map:
                sequence_map[trans_diff_sequence] = trans

        sequence_maps.append(sequence_map)
    return sequence_maps


def find_best_trans_diff_sequence(
    sequence_maps: list[TransDiffSequenceMap],
) -> tuple[TransDiffSequence, int]:
    accumulated_trans_diff_sequence_map: TransDiffSequenceMap = {}
    for sequence_map in sequence_maps:
        for trans_diff_sequence, trans in sequence_map.items():
            if trans_diff_sequence not in accumulated_trans_diff_sequence_map:
                accumulated_trans_diff_sequence_map[trans_diff_sequence] = 0
            accumulated_trans_diff_sequence_map[trans_diff_sequence] += trans
    max_key = max(
        accumulated_trans_diff_sequence_map, key=accumulated_trans_diff_sequence_map.get
    )
    return max_key, accumulated_trans_diff_sequence_map[max_key]


trans_2000th = list(
    map(functools.partial(calculate_trans_list_to_nth, n=2000), initial_values)
)
diffs_2000th = list(map(calculate_trans_diffs, trans_2000th))
sequence_maps_200th = compute_trans_diff_sequence_maps(trans_2000th, diffs_2000th)
best_sequence, best_reward = find_best_trans_diff_sequence(sequence_maps_200th)

print(f"Problem 2: {best_reward}")
