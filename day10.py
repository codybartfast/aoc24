INPUT = 'input'


def solve():
    rows = [[int(char) for char in line] for line in read().splitlines()]
    trailheads = find_trailheads(rows)
    map = Map(rows)

    ans1, ans2 = 0, 0
    for head in trailheads:
        paths = find_paths(map, head)
        ans1 += len({path[-1] for path in paths})
        ans2 += len(paths)

    print(f'Part 1: {ans1}')
    print(f'Part 2: {ans2}')


def find_paths(map, head):
    paths = [[head]]
    for height in range(1, 10):
        paths = [
            new_path
            for path in paths
            for new_path in extend_path(map, path, height)]
    return paths


def extend_path(map, path, height):
    for pos, val in map.adjacent(*path[-1]):
        if val == height:
            yield path + [pos]


def find_trailheads(rows):
    return [
        (x, y)
        for y, row in enumerate(rows)
        for x, char in enumerate(row)
        if char == 0]


def read():
    return open(f'./input/2024/day10/{INPUT}.txt').read().strip()


class Map:
    adjacent_directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def __init__(self, rows):
        self.rows = rows
        self.height = len(rows)
        self.width = len(rows[0])

    def value(self, x, y):
        if y >= 0 and y < self.height and x >= 0 and x < self.width:
            return self.rows[y][x]

    def adjacent(self, x, y):
        return [
            ((adj_x, adj_y), value)
            for dx, dy in self.adjacent_directions
            if (value := self.value((adj_x := x + dx), (adj_y := y + dy)))
               is not None]


solve()
