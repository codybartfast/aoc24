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

    def __repr__(self):
        return '\n'.join(self.rows)

def clockit(action, repeat=1):
    from timeit import timeit
    time = timeit(action, number=repeat)
    print(f"\n'{action.__name__}' took {(time / repeat):.3f} seconds")
