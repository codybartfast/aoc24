from stocking import clockit

DIRECTIONS = (0, -1), (1, 0), (0, 1), (-1, 0)
[_, RIGHT, _, LEFT] = DIRECTIONS

INPUT = 'input'


def solve():
    house1, house2, moves = parse(lines())
    print(f'Part 1: {cure_woes(house1, moves)}')
    print(f'Part 2: {cure_woes(house2, moves)}')


def cure_woes(house, moves):
    robot = house.find('@')
    for move in moves:
        robot = apply_move(house, robot, move)
    return sum(x + 100 * y for (x, y), val in house if val in 'O[')


def apply_move(house, robot, direction):
    pressured = [{robot}]
    while prev_line := pressured[-1]:
        line = set()
        for coord in prev_line:
            pressured_coords = find_pressured(house, coord, direction)
            if pressured_coords is False:
                return robot
            line.update(pressured_coords)
        pressured.append(line)

    for line in pressured[::-1]:
        for coord in line:
            target, _ = house.next(coord, direction)
            house[target] = house[coord]
            house[coord] = '.'
    return house.next(robot, direction)[0]


def find_pressured(house, coord, direction):
    next_coord, next_item = house.next(coord, direction)
    match next_item:
        case '#':
            return False
        case 'O':
            return (next_coord,)
        case '[':
            if direction in [LEFT, RIGHT]:
                return (next_coord,)
            else:
                return (next_coord, house.next(next_coord, RIGHT)[0])
        case ']':
            if direction in [LEFT, RIGHT]:
                return (next_coord,)
            else:
                return (next_coord, house.next(next_coord, LEFT)[0])
        case _:
            return ()


def parse(lines):
    gap = lines.index('')
    map1 = lines[:gap]
    map2 = [line.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')
            for line in map1]
    house1 = Warehouse([list(line) for line in map1])
    house2 = Warehouse([list(line) for line in map2])

    arrows = '^>v<'
    moves = [DIRECTIONS[arrows.index(arrow)]
             for arrow in ''.join(lines[gap + 1:])]

    return house1, house2, moves


def lines():
    return open(f'./input/2024/day15/{INPUT}.txt').read().strip().splitlines()


class Warehouse:
    def __init__(self, rows):
        self.rows = rows
        self.height = len(rows)
        self.width = len(rows[0])

    def __getitem__(self, coord):
        return self.rows[coord[1]][coord[0]]

    def __setitem__(self, key, value):
        self.rows[key[1]][key[0]] = value

    def next(self, coord, direction):
        x, y = coord
        dx, dy = direction
        return (x := x + dx, y := y + dy), self[(x, y)]

    def find(self, target):
        for coord, val in self:
            if val == target:
                return coord

    def __iter__(self):
        return (
            ((x, y), item)
            for (y, row) in enumerate(self.rows)
            for (x, item) in enumerate(row))

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.rows])


clockit(solve)
