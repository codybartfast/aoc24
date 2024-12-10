INPUT = 'input'

DIRECTIONS = ((0, -1), (1, 0), (0, 1), (-1, 0))


def main():
    start_pos, lab = read_lab_map()
    visited = watch_guard_leave(lab, start_pos)
    print(f'Part 1: {len(visited)}')

    ans2 = 0
    for pos in visited:
        lab.blocks.add(pos)
        lab.free.remove(pos)
        if not watch_guard_leave(lab, start_pos):
            ans2 += 1
        lab.blocks.remove(pos)
        lab.free.add(pos)
    print(f'Part 2: {ans2}')


def watch_guard_leave(lab, pos):
    dir = 0
    visited = {(pos, dir)}
    while True:
        while (next := next_in_dir(pos, dir)) in lab.free:
            if (next, dir) in visited:
                return None
            visited.add((next, dir))
            pos = next
        if next not in lab.blocks:
            return set(pos for pos, _ in visited)
        dir = (dir + 1) % 4
        while (next_in_dir(pos, dir) in lab.blocks):
            dir = (dir + 1) % 4


def next_in_dir(pos, dir):
    dx, dy = DIRECTIONS[dir]
    return pos[0] + dx, pos[1] + dy


def read_lab_map():
    rows = read().splitlines()
    blocks = set()
    free = set()
    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            if char == '#':
                blocks.add((x, y))
            else:
                free.add((x, y))
                if char == '^':
                    start = (x, y)

    return start, type('', (), {
        'blocks': blocks,
        'free': free
    })()


def read():
    return open(f'./input/2024/day06/{INPUT}.txt').read().strip()


main()
