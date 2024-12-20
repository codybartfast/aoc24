from stocking import clockit
from collections import Counter

INPUT = 'input'


def race_condition():
    track = Track(lines())
    start, end = track.find('S'), track.find('E')
    path, distances = find_path(track, start)

    ans1 = count_cheats(track, path, start, 2, distances)
    print(f'Part 1: {ans1}')

    ans2 = count_cheats(track, path, start, 20, distances)
    print(f'Part 2: {ans2}')


def count_cheats(track, path, start, radius, distances):
    counts = Counter(
        cheats
        for idx in range(len(path))
        for cheats in find_cheats(track, path[idx], radius, distances))
    return sum(counts[value] for value in counts if value >= 100)


def find_cheats(track, coord, radius, distances):
    cheats = []
    (ax, ay) = coord
    for bx, by in track.disc_coords((ax, ay), radius):
        if (bx, by) in distances:
            grid_dist = abs(ax - bx) + abs(ay - by)
            path_dist = distances[(bx, by)] - distances[(ax, ay)]
            if path_dist > grid_dist:
                cheats.append(path_dist - grid_dist)
    return cheats


def find_path(track, start):
    path = [(start, 0)]
    dist = 1
    visited = set(path)
    coord = start
    while track[coord][0] != 'E':
        coord = [coord
                 for coord, char in track.adjacent(coord)
                 if char != '#' and coord not in visited][0]
        visited.add(coord)
        path.append((coord, dist))
        dist += 1
    coords = [coord for coord, dist in path]
    distances = {coord: dist for coord, dist in path}
    return coords, distances


def lines():
    return open(f'./input/2024/day20/{INPUT}.txt').read().strip().splitlines()


class Track:
    adjacent_directions = (0, -1), (1, 0), (0, 1), (-1, 0)

    def __init__(self, rows):
        self.rows = rows
        self.height = len(rows)
        self.width = len(rows[0])

    def __getitem__(self, coord):
        # print(coord)
        return self.rows[coord[1]][coord[0]]

    def inbounds(self, coord):
        x, y = coord
        return 0 <= y < self.height and 0 <= x < self.width

    def get(self, coord):
        if self.inbounds(coord):
            x, y = coord
            return self.rows[y][x]

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

    def find(self, target):
        for coord, val in self:
            if val == target:
                return coord

    def disc_coords(self, centre, radius):
        x, y = centre
        return [
            coord
            for dx in range(-radius, radius + 1)
            for dy in range(-radius, radius + 1)
            if abs(dx) + abs(dy) <= radius and self.inbounds(coord := (x + dx, y + dy))]

    def __iter__(self):
        return (
            ((x, y), item)
            for (y, row) in enumerate(self.rows)
            for (x, item) in enumerate(row))


clockit(race_condition)
