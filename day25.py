from stocking import clockit

INPUT = 'input'


def code_chronicle():
    locks, keys = parse(lines())
    ans1 = sum(1 for lock in locks for key in keys if fits(key, lock))
    print(f'Part 1: {ans1}')


def fits(key, lock):
    for k, l in zip(key, lock):
        if k + l > 5:
            return False
    return True


def parse(lines):
    blocks = []
    block = []
    for line in lines:
        if line == '':
            blocks.append(block)
            block = []
        else:
            block.append(line)
    blocks.append(block)

    locks, keys = [], []
    for block in blocks:
        (locks if block[0] == '#####' else keys).append(block)
    locks = [[row.index('.') - 1 for row in zip(*lock)] for lock in locks]
    keys = [[6 - row.index('#') for row in zip(*key)] for key in keys]
    return locks, keys


def lines():
    return open(f'./input/2024/day25/{INPUT}.txt').read().strip().splitlines()


clockit(code_chronicle)
