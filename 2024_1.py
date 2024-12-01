from aocd import data
import re

left_list, right_list = zip(*[[int(n) for n in re.sub(' +', ' ', line).split()] for line in data.splitlines()])

left_list = sorted(left_list)
right_list = sorted(right_list)

distances = [abs(l - r) for (l, r) in zip(left_list, right_list)]
total_distance = sum(distances)

print(f"Problem 1: {total_distance}")

duplicate_numbers = [n for n in left_list if n in right_list]
similarities = [right_list.count(n) * n for n in duplicate_numbers]
total_similarity = sum(similarities)

print(f"Problem 2: {total_similarity}")
