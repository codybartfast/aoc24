INPUT = 'input'

class File:
    def __init__(self, id, size, space):
        self.id = id
        self.size = size
        self.space = space
        self.next = None
        self.prev = None

    def __str__(self):
        return f'{self.prev.id if self.prev else self.prev}<-F{self.id}:{self.size}..{self.space}->{self.next.id if self.next else self.next}'


def main():
    map = read()
    map = [int(digit) for digit in map]
    if len(map) % 2 == 0:
        raise ValueError('Exepected odd map length')
    map.append(0)

    disk = init_disk(map)
    fill = 0
    move = len(disk) - 1
    def search():
        nonlocal fill
        nonlocal move
        while disk[fill] != None:
            fill += 1
        while disk[move] == None:
            move -= 1
    search()
    while fill < move:
        disk[fill] = disk[move]
        disk[move] = None
        search()
    ans1 = checksum(disk)

    files = init_files(map)
    for id in range(len(files) - 1, -1, -1):
        try_move_file(files, id)

    # try_move_file(files, 9)
    # try_move_file(files, 8)
    # try_move_file(files, 7)
    # try_move_file(files, 6)
    # try_move_file(files, 5)
    # try_move_file(files, 4)
    # try_move_file(files, 3)
    # try_move_file(files, 2)
    # try_move_file(files, 1)
    # try_move_file(files, 0)

    file = files[0]
    while file:
        print(file)
        file = file.next

    print(checksum_file(files))

    disk2 = []
    file = files[0]
    while file:
        disk2 += [file.id] * file.size
        disk2 += [None] * file.space
        file = file.next

    ans2 = checksum(disk2)
    print(f'Part 1: {ans1}')
    print(f'Part 2: {ans2}')

def checksum_file(files):
    sum = 0
    pos = 0
    file = files[0]
    while file:
        for block in range(0, file.size):
            sum += file.id * pos
            pos += 1
        pos = pos + file.space
        file = file.next
    return sum

def try_move_file(files, id):
    # print(id)
    source = files[id]
    destination = files[0]
    while destination.id != id:
        if destination.space >= source.size:
            if destination.next == source:
                destination.space = 0
                source.space += destination.space
                return True
            source_prev = source.prev
            source_next = source.next
            source_space = source.space
            source.space = destination.space - source.size
            destination.space = 0
            source.next = destination.next
            destination.next.prev = source
            source.prev = destination
            destination.next = source

            source_prev.space += source.size + source_space
            source_prev.next = source_next
            if source_next:
                source_next.prev = source_prev
            return True
        destination = destination.next
    return False


def init_files(map):
    files = {}
    for idx in range(0, len(map), 2):
        file = File(idx // 2, map[idx], map[idx+1])
        files[file.id] = file
    for id in range(0, len(files)-1):
        files[id].next = files[id+1]
        files[id+1].prev = files[id]
    return files


def checksum(disk):
    return sum(idx * id for (idx, id) in enumerate(disk) if id != None)

def parse(line):
    return line

def init_disk(map):
    disk = []
    id = 0
    for idx in range(0, len(map), 2):
        for i in range(map[idx]):
            disk.append(id)
        for i in range(map[idx+1]):
            disk.append(None)
        id += 1
    return disk


def read():
    return open(f'./input/2024/day09/{INPUT}.txt').read().strip()

main()