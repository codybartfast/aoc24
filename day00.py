INPUT = 'test1'

def main():
    items = [parse(line) for line in lines()]

    # check if seq
    ans1 = '\n'.join([str(item) for item in items])
    ans2 = ', '.join(open(f'./input/2024/day00/input.txt', 'r').read().splitlines())

    print(f'Part 1: {ans1}\nPart 2: {ans2}')

def parse(line):
    return line

def lines(): return read().splitlines()

def read():
    return open(f'./input/2024/day00/{INPUT}.txt').read().strip()

main()