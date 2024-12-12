from stocking import *

INPUT = 'input'

NEIGHBOUR_DELTAS = {
    (0, -1): [(-1, 0), (1, 0)],
    (1, 0): [(0, -1), (0, 1)],
    (0, 1): [(-1, 0), (1, 0)],
    (-1, 0): [(0, -1), (0, 1)],
}


def solve():
    garden = Grid(lines())
    x = [r for r in find_regions(garden, {next(iter(garden))})]

    ans1 = 0
    for region in x:
        ans1 += len(region[1]) * perimeter(region)
    print(f'Part 1: {ans1}')

    ans2 = 0
    for region in x:
        plant = region[0]
        boarder_plants = find_boarder_plants(region)
        edge_count = 0
        while boarder_plants:
            edge_count += 1
            (pos, dir) = boarder_plants.pop()
            for delta in NEIGHBOUR_DELTAS[dir]:
                (x, y) = pos
                while (neighbour := ((x := x + delta[0], y := y + delta[1]), dir)) in boarder_plants:
                    boarder_plants.remove(neighbour)

        ans2 += len(region[1]) * edge_count
    print(f'Part 2: {ans2}')


def find_boarder_plants(region):
    (plant, locs) = region
    edge = set()
    for x, y in locs:
        for (dx, dy) in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            adjacent = (x + dx, y + dy)
            if adjacent not in locs:
                edge.add(((x, y), (dx, dy)))
    return edge


def perimeter(region):
    (_, locs) = region
    length = 0
    for x, y in locs:
        adjacents = [(x + dx, y + dy) for (dx, dy) in [(0, -1), (1, 0), (0, 1), (-1, 0)]]
        length += sum(1 for adjacent in adjacents if adjacent not in locs)
    return length


def find_regions(garden, unexplored):
    explored = set()
    while unexplored:
        (pos, plant) = unexplored.pop()
        region = {pos}
        unexpanded = {pos}
        while unexpanded:
            pos = unexpanded.pop()
            for (adj_pos, adj_plant) in garden.adjacent(pos):
                if adj_pos not in region:
                    if adj_plant == plant and adj_pos not in region:
                        region.add(adj_pos)
                        unexpanded.add(adj_pos)
                        unexplored.discard((adj_pos, adj_plant))
                    elif adj_pos not in explored:
                        unexplored.add((adj_pos, adj_plant))
            explored.add(pos)
        yield (plant, region)


def lines():
    return open(f'./input/2024/day12/{INPUT}.txt').read().strip().splitlines()


solve()
