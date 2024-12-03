
def text():
    return open(f'./input/2024/day00/{input_name}.txt').read().strip()

def lines(): return text().splitlines()

def parse(line):
    return line

input_name = 'test1'
items = [parse(line) for line in lines()]

ans1 = '\n'.join([str(item) for item in items])
ans2 = ', '.join(open(f'./input/2024/day00/input.txt', 'r').read().splitlines())

print(f'Part 1: {ans1}')
print(f'Part 2: {ans2}')