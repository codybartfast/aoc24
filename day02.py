
def text():
    with open(f'./input/2024/day00/{input_name}.txt', 'r') as file:
        return file.read().strip()

def lines(): return text().splitlines()

def parse(line):
    return line

input_name = 'test1'

parsed = [parse(line) for line in lines()]

answer1 = ', '.join(parsed)
answer2 = ', '.join(open(f'./input/2024/day00/input.txt', 'r').read().splitlines())

print(f'Part 1: {answer1}')
print(f'Part 2: {answer2}')