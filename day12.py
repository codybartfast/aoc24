from stocking import clockit

INPUT = 'input'

NEIGHBOUR_DELTAS = {
    (0, -1): [(-1, 0), (1, 0)],
    (1, 0): [(0, -1), (0, 1)],
    (0, 1): [(-1, 0), (1, 0)],
    (-1, 0): [(0, -1), (0, 1)], }


def solve():
    ans1, ans2 = 0, 0

    for region in find_regions(Grid(lines())):
        perimeter = set(find_perimeter(region))
        ans1 += len(region) * len(perimeter)
        ans2 += len(region) * count_edges(perimeter)

    print(f'Part 1: {ans1}')
    print(f'Part 2: {ans2}')


def count_edges(perimeter):
    count = 0
    while perimeter:
        count += 1
        pos, direction = perimeter.pop()
        for dx, dy in NEIGHBOUR_DELTAS[direction]:
            x, y = pos
            while ((neighbour := ((x := x + dx, y := y + dy), direction))
                   in perimeter):
                perimeter.remove(neighbour)
    return count


def find_perimeter(region):
    return (
        ((x, y), (dx, dy))
        for x, y in region
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]
        if (x + dx, y + dy) not in region)


def find_regions(garden):
    unexplored = set(garden)
    while unexplored:
        pos, plant = unexplored.pop()
        region = {pos}
        unexpanded = [pos]
        while unexpanded:
            pos = unexpanded.pop()
            for adj_pos, adj_plant in garden.adjacent(pos):
                if adj_plant == plant and adj_pos not in region:
                    region.add(adj_pos)
                    unexpanded.append(adj_pos)
                    unexplored.remove((adj_pos, plant))
        yield region


def lines():
    return open(f'./input/2024/day12/{INPUT}.txt').read().strip().splitlines()


class Grid:
    adjacent_directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def __init__(self, rows):
        self.rows = rows
        self.height = len(rows)
        self.width = len(rows[0])

    def get(self, x, y):
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.rows[y][x]

    def adjacent(self, pos):
        x, y = pos
        return [
            ((adj_x, adj_y), value)
            for dx, dy in self.adjacent_directions
            if (value := self.get((adj_x := x + dx), (adj_y := y + dy)))
               is not None]

    def __iter__(self):
        return (
            ((x, y), self.rows[y][x])
            for y in range(self.height)
            for x in range(self.width))


clockit(solve)
