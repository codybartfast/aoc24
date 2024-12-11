from itertools import combinations

INPUT = 'input'

def main():
    city = [parse(line) for line in lines()]
    height, width = len(city), len(city[0])
    def in_bounds(x, y): return 0 <= x < width and 0 <= y < height
    antennas = find_antennas(city)

    ans1 = len({
        antinode
        for ants in antennas.values()
        for pair in combinations(ants, 2)
        for antinode in calc_antinodes(*pair)
        if in_bounds(*antinode)})

    ans2 = len({
        antinode
        for ants in antennas.values()
        for pair in combinations(ants, 2)
        for antinode in calc_more_antinodes(*pair, in_bounds)})

    print(f'Part 1: {ans1}\nPart 2: {ans2}')

def calc_more_antinodes(antenna1, antenna2, filter):
    x1, y1 = antenna1
    x2, y2 = antenna2
    dx = x2 - x1
    dy = y2 - y1

    x, y = antenna1
    while filter(x, y):
        yield (x, y)
        x += dx
        y += dy

    x, y = antenna1
    while filter(x, y):
        yield (x, y)
        x -= dx
        y -= dy


def calc_antinodes(antenna1, antenna2):
    x1, y1 = antenna1
    x2, y2 = antenna2
    dx = x2 - x1
    dy = y2 - y1
    return  (x2 + dx, y2 + dy), (x1 - dx, y1 - dy)

def find_antennas(map):
    antennas = {}
    for y, row in enumerate(map):
        for x, char in enumerate(row):
            if char != '.':
                antennas[char] = antennas.get(char, []) + [(x, y)]
    return antennas

def parse(line):
    return line

def lines(): return read().splitlines()

def read():
    return open(f'./input/2024/day08/{INPUT}.txt').read().strip()

main()