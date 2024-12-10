class Grid:
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
