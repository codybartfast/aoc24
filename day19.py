from stocking import clockit

INPUT = 'input'


def solve():
    towels, patterns = parse(lines())
    clean = clean_towels(towels)

    ans1, ans2 = 0, 0
    known = {'': 1}
    for pattern in patterns:
        if possible(clean, pattern):
            ans1 += 1
            ans2 += how_many_ways(towels, pattern, known)
    print(f'Part 1: {ans1}')
    print(f'Part 2: {ans2}')


def how_many_ways(towels, pattern, known):
    if pattern not in known:
        known[pattern] = sum(
            how_many_ways(towels, pattern[len(towel):], known)
            for towel in towels
            if pattern.startswith(towel))
    return known[pattern]


def clean_towels(towels):
    # clean towel = towel that can't be created from other towels
    return [
        towel
        for idx, towel in enumerate(towels)
        if not possible(towels[:idx] + towels[idx + 1:], towel)]


def possible(towels, pattern):
    if pattern == '':
        return True
    for towel in towels:
        if pattern.startswith(towel):
            if possible(towels, pattern[len(towel):]):
                return True


def parse(lines):
    towels = lines[0].split(', ')
    patterns = lines[2:]
    return towels, patterns


def lines():
    return open(f'./input/2024/day19/{INPUT}.txt').read().strip().splitlines()


clockit(solve)
