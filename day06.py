INPUT = 'input'

DIRECTIONS = ((0, -1), (1, 0), (0, 1), (-1, 0))


def main():
    lab = rows()

    guard = find_guard(lab)
    path = watch_guard(lab, guard)
    path_locs = set(pos for pos, _ in path)
    ans1 = len(path_locs)

    block_locs = []
    for (x, y) in path_locs:
        current = lab[y][x]
        if current == '.':
            lab[y][x] = '#'
            try:
                watch_guard(lab, find_guard(lab))
            except ValueError as e:
                if str(e) == 'LOOP!':
                    block_locs.append((x, y))
                else:
                    print(str(e))
                continue
            finally:
                lab[y][x] = current

    ans2 = len(block_locs)

    print(f'Part 1: {ans1}\nPart 2: {ans2}')


def watch_guard(lab, guard):
    while (in_lab(lab, guard[0])):
        guard = advance_guard(lab, guard)
    return guard[2]


def advance_guard(lab, guard):
    pos, dir, path = guard
    state = pos, dir
    if state in path:
        raise ValueError('LOOP!')
    path.add(state)
    forward_pos = pos_in_dir(pos, dir)
    if check_map(lab, forward_pos):
        next = forward_pos
    else:
        dir = next_dir(dir)
        next = pos_in_dir(pos, dir)
        if not check_map(lab, next):
            dir = next_dir(dir)
            next = pos_in_dir(pos, dir)
            if not check_map(lab, next):
                dir = next_dir(dir)
                next = pos_in_dir(pos, dir)
                if not check_map(lab, next):
                    raise ValueError('Oops')
    return (next, dir, path)


def check_map(lab, pos):
    x, y = pos
    return not in_lab(lab, pos) or lab[y][x] != '#'


def in_lab(lab, pos):
    x, y = pos
    return (
            y >= 0
            and y < len(lab)
            and x >= 0
            and x < len(lab[y]))


def pos_in_dir(pos, dir):
    return pos[0] + dir[0], pos[1] + dir[1]


def next_dir(dir):
    return DIRECTIONS[(DIRECTIONS.index(dir) + 1) % len(DIRECTIONS)]


def find_guard(lab):
    y, row = [(idx, row) for (idx, row) in enumerate(lab) if '^' in row][0]
    x = row.index('^')
    return ((x, y), DIRECTIONS[0], set())


def rows(): return [list(line) for line in read().splitlines()]


def read():
    return open(f'./input/2024/day06/{INPUT}.txt').read().strip()


main()
