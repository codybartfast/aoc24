
def text():
    with open(f'./input/2024/day02/{input_name}.txt', 'r') as file:
        return file.read().strip()

def lines(): return text().splitlines()

def parse(line):
    return [int(level) for level in line.split()]

def is_safe(record, can_remove):
    if any(level < record[0] for level in record):
        record.reverse()
    if all(level2 - level1 in [1, 2, 3] for (level1, level2) in zip(record, record[1:])):
        return True
    elif can_remove:
        return any(is_safe(record[:idx] + record[idx + 1:], False) for idx in range(len(record)))

input_name = 'input'
records = [parse(line) for line in lines()]

answer1 = sum(1 for record in records if is_safe(record, False))
answer2 = sum(1 for record in records if is_safe(record, True))

print(f'Part 1: {answer1}')
print(f'Part 2: {answer2}')