from stocking import clockit
from collections import deque

# INPUT, MAX_IDX, FIRST_DROP_COUNT = 'test1', 6, 12
INPUT, MAX_IDX, FIRST_DROP_COUNT = 'input', 70, 1024
size = MAX_IDX + 1


def ram_run():
    incoming = [parse(line) for line in lines()]
    ram = Ram(size)
    end = (MAX_IDX, MAX_IDX)
    for coord in incoming[:FIRST_DROP_COUNT]:
        ram[coord] = '#'
    history = navigate(ram)
    ans1 = history[end]
    print(f'Part 1: {ans1}')

    low, high = FIRST_DROP_COUNT, len(incoming)
    while low < high:
        mid = (low + high) // 2
        ram = Ram(size)
        for coord in incoming[:mid]:
            ram[coord] = '#'
        history = navigate(ram)
        if end in history:
            low = mid + 1
        else:
            high = mid
    ans2 = ','.join(str(n) for n in incoming[mid - 1])
    print(f'Part 2: {ans2}')


def navigate(ram):
    history = {(0, 0): 0}
    explore_around = deque([((0, 0), 0)])
    while explore_around:
        pos, steps = explore_around.popleft()
        steps += 1
        for coord, value in ram.adjacent(pos):
            if value != '#' and (coord not in history or steps < history[coord]):
                history[coord] = steps
                explore_around.append((coord, steps))
    return history


def parse(line):
    parts = line.split(',')
    return int(parts[0]), int(parts[1])


def lines():
    return open(f'./input/2024/day18/{INPUT}.txt').read().strip().splitlines()


class Ram:
    adjacent_directions = (0, -1), (1, 0), (0, 1), (-1, 0)

    def __init__(self, size):
        self.rows = [['.'] * size for _ in range(size)]
        self.height = size
        self.width = size

    def __setitem__(self, key, value):
        self.rows[key[1]][key[0]] = value

    def get(self, coord):
        x, y = coord
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.rows[y][x]
        else:
            return '#'

    def next(self, coord, direction):
        x, y = coord
        dx, dy = direction
        return (x := x + dx, y := y + dy), self.get((x, y))

    def adjacent(self, coord):
        x, y = coord
        return [
            coord_item
            for direction in self.adjacent_directions
            if (coord_item := self.next(coord, direction))
               is not None]


clockit(ram_run)
