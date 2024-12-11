from stocking import *

INPUT = 'input'


def solve():
    stones = lines()[0].split()
    ans1 = sum(count_25(stone) for stone in stones)
    ans2 = sum(count_75(stone) for stone in stones)

    print(f'Part 1: {ans1}')
    print(f'Part 2: {ans2}')


def count_75(stone):
    return sum(count_50(stone) for stone in blink_25(stone))


def count_50(stone, counts={}):
    if stone not in counts:
        counts[stone] = sum(count_25(stone) for stone in blink_25(stone))
    return counts[stone]


def count_25(stone, counts={}):
    if stone not in counts:
        counts[stone] = len(list(blink_25(stone)))
    return counts[stone]


def blink_25(stone):
    stones = [stone]
    for _ in range(25):
        stones = (new_stone for stone in stones for new_stone in blink_1(stone))
    return stones


def blink_1(stone):
    if stone == '0': return ['1']
    if len(stone) % 2 == 0:
        half_len = len(stone) // 2
        return [stone[0:half_len].lstrip('0') or '0', stone[half_len:].lstrip('0') or '0']
    else:
        return [str(int(stone) * 2024)]


def parse(line):
    return line


def lines():
    return open(f'./input/2024/day11/{INPUT}.txt').read().strip().splitlines()


solve()
