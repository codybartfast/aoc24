INPUT = 'input'
DIRECTIONS = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))


def main():
    puzzle = lines()
    xmas_count, x_mas_count = 0, 0
    for y in range(len(puzzle)):
        for x in range(len(puzzle[y])):
            for direction in DIRECTIONS:
                if check_xmas(puzzle, 'XMAS', (x, y), direction):
                    xmas_count += 1
            if check_x_mas(puzzle, (x, y)):
                x_mas_count += 1
    print(f'Part 1: {xmas_count}\nPart 2: {x_mas_count}')


def check_x_mas(puzzle, pos):
    points = ''.join(
        letter_at(puzzle, take_step(pos, direction))
        for direction in DIRECTIONS[1::2])

    return letter_at(puzzle, pos) == 'A' and points in ['MMSS', 'SMMS', 'SSMM', 'MSSM']


def check_xmas(puzzle, remaining, pos, direction):
    if not remaining:
        return True
    if letter_at(puzzle, pos) != remaining[0]:
        return False
    return check_xmas(puzzle, remaining[1:], take_step(pos, direction), direction)


def take_step(pos, step):
    col, row = pos
    col_delta, row_delta = step
    return col + col_delta, row + row_delta


def letter_at(puzzle, pos):
    col, row = pos
    if row < 0 or row >= len(puzzle) or col < 0 or col >= len(puzzle[row]):
        return '#'
    return puzzle[row][col]


def lines():
    return open(f'./input/2024/day04/{INPUT}.txt').read().strip().splitlines()


main()
