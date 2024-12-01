from collections import Counter

def text():
    with open(f'./input/2024/day01/{input_name}.txt', 'r') as file:
        return file.read().strip()

def parse(line):
    return [int(id) for id in line.split()]

input_name = 'input'

unsorted_pairs = (parse(line) for line in text().splitlines())
left_col, right_col = zip(*unsorted_pairs)
pairs = zip(sorted(left_col), sorted(right_col))
answer1 = sum(abs(left - right) for (left, right) in pairs)

right_counts = dict(Counter(right_col))
answer2 = sum(left * right_counts.get(left, 0) for left in left_col)

print(f'Part 1: {answer1}')
print(f'Part 2: {answer2}')