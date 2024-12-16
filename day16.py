from stocking import clockit
from collections import deque

INPUT = 'input'


def reindeer_maze():
    maze = Maze(lines())
    start = maze.find('S')
    end = maze.find('E')

    deer = Deer(start)
    history = {deer.history_key(): deer.score}
    future = deque(find_next_herd(maze, deer))

    finishers = navigate(maze, end, history, future)
    best_score = min(deer.score for deer in finishers)
    print(f'Part 1: {best_score}')

    best_seats = {
        coord
        for winner in finishers if winner.score == best_score
        for coord in winner.tracks}
    print(f'Part 2: {len(best_seats)}')


def navigate(maze, end, history, future_herd):
    finishers = []
    while future_herd:
        deer = future_herd.popleft()
        while len(next_herd := find_next_herd(maze, deer)) == 1:
            deer = next_herd[0]
            if deer.coord == end:
                finishers.append(deer)
            break
        if not next_herd:
            continue
        for next_deer in next_herd:
            if deer.coord == end:
                finishers.append(deer)
                continue
            key = next_deer.history_key()
            if key not in history or next_deer.score <= history[key]:
                history[key] = next_deer.score
                future_herd.append(next_deer)
    return finishers


def find_next_herd(maze, deer):
    herd = []
    if maze.is_free(deer.ahead()):
        herd.append(deer.advance_ahead())
    if maze.is_free(deer.left()):
        herd.append(deer.advance_left())
    if maze.is_free(deer.right()):
        herd.append(deer.advance_right())
    return herd


def lines():
    return open(f'./input/2024/day16/{INPUT}.txt').read().strip().splitlines()


class Deer:
    directions = (0, -1), (1, 0), (0, 1), (-1, 0)

    def __init__(self, coord, heading=1, score=0, tracks=None):
        tracks = tracks or []
        self.coord = coord
        self.heading = heading
        self.score = score
        self.tracks = tracks + [coord]

    def ahead(self):
        (x, y), (dx, dy) = self.coord, Deer.directions[self.heading]
        return x + dx, y + dy

    def left(self):
        (x, y), (dx, dy) = self.coord, Deer.directions[(self.heading - 1) % 4]
        return x + dx, y + dy

    def right(self):
        (x, y), (dx, dy) = self.coord, Deer.directions[(self.heading + 1) % 4]
        return x + dx, y + dy

    def advance_ahead(self):
        return Deer(self.ahead(), self.heading, self.score + 1, self.tracks)

    def advance_left(self):
        return Deer(self.left(), (self.heading - 1) % 4, self.score + 1001, self.tracks)

    def advance_right(self):
        return Deer(self.right(), (self.heading + 1) % 4, self.score + 1001, self.tracks)

    def history_key(self):
        return self.coord, self.heading

    def __repr__(self):
        dir_names = ['UP', 'RIGHT', 'DOWN', 'LEFT']
        return f'𐂂 {self.coord} heading {dir_names[self.heading]} with score {self.score:,} having trekked {len(self.tracks)} 🦌'


class Maze:
    def __init__(self, rows):
        self.rows = rows
        self.height = len(rows)
        self.width = len(rows[0])

    def __getitem__(self, coord):
        return self.rows[coord[1]][coord[0]]

    def is_free(self, coord):
        return self[coord] != '#'

    def find(self, target):
        for coord, val in self:
            if val == target:
                return coord

    def __iter__(self):
        return (
            ((x, y), item)
            for (y, row) in enumerate(self.rows)
            for (x, item) in enumerate(row))


clockit(reindeer_maze)
