from stocking import *

INPUT = 'test1'

def solve():
    x = [parse(line) for line in lines()]

    ans1 = ('\n'.join([str(item) for item in x])
            if hasattr(x, '__iter__') and not isinstance(x, str) else x)
    print(f'Part 1: {ans1}')

    ans2 = ', '.join(open(f'./input/2024/day00/input.txt', 'r').read().splitlines())
    print(f'Part 2: {ans2}')

def parse(line):
    return line

def lines():
    return open(f'./input/2024/day00/{INPUT}.txt').read().strip().splitlines()

clockit(solve)