from stocking import clockit

INPUT = 'input'


def solve():
    stones = read().split()

    ans1 = sum(count_stones_after(stone, 25) for stone in stones)
    print(f'Part 1: {ans1}')

    ans2 = sum(count_stones_after(stone, 75) for stone in stones)
    print(f'Part 2: {ans2}')


def count_stones_after(stone, blinks, counts={}):
    key = (stone, blinks)
    if key not in counts:
        stones_5 = blink(stone, 5)
        if blinks == 5:
            count = sum(1 for s in stones_5)
        else:
            count = sum(count_stones_after(stone, blinks - 5)
                        for stone in stones_5)
        counts[key] = count
    return counts[key]


def blink(stone, n):
    stones = [stone]
    for _ in range(n):
        stones = (new_stone for stone in stones for new_stone in blink_once(stone))
    return stones


def blink_once(stone):
    if stone == '0': return ['1']
    if len(stone) % 2 == 0:
        half_len = len(stone) // 2
        return [stone[:half_len].lstrip('0') or '0',
                stone[half_len:].lstrip('0') or '0']
    else:
        return [str(int(stone) * 2024)]


def read():
    return open(f'./input/2024/day11/{INPUT}.txt').read().strip()


clockit(solve)
