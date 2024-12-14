import re
from collections import Counter
from stocking import clockit

# INPUT, WIDTH, HEIGHT = 'test1', 11, 7
INPUT, WIDTH, HEIGHT = 'input', 101, 103

MID_X = WIDTH // 2
MID_Y = HEIGHT // 2


def visit_bathroom():
    robots = [robot(line) for line in lines()]
    positions = [rob[0] for rob in robots]
    vectors = [rob[1] for rob in robots]

    seconds = 0
    while len(set(positions)) < len(positions):
        if seconds == 100:
            print(f'Part 1: {safety_score(positions)}')
        seconds += 1
        for idx in range(len(positions)):
            positions[idx] = (
                (positions[idx][0] + vectors[idx][0]) % WIDTH,
                (positions[idx][1] + vectors[idx][1]) % HEIGHT)
    print(f'Part 1: {seconds}')


def safety_score(positions):
    score = 1
    for count in Counter(
        (x_comp, y_comp)
        for (x, y) in positions
        if (x_comp := compare(x, MID_X)) and (y_comp := compare(y, MID_Y))
    ).values():
        score *= count
    return score

def compare(a, b):
    return (a > b) - (a < b)


def robot(line):
    [x, y, dx, dy] = [int(digits) for digits in re.findall(r'-?\d+', line)]
    return (x, y), (dx, dy)


def lines():
    return open(f'./input/2024/day14/{INPUT}.txt').read().strip().splitlines()


clockit(visit_bathroom)
