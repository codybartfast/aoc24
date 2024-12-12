from stocking import clockit

INPUT = 'input'


def main():
    disk_map = [int(digit) for digit in read()]
    disk_map.append(0)

    ans1 = checksum(defrag_blocks(disk_map))
    print(f'Part 1: {ans1}')
    ans2 = checksum(defrag_files(disk_map))
    print(f'Part 2: {ans2}')


def defrag_files(disk_map):
    files = [File(idx // 2, disk_map[idx - 1], disk_map[idx])
             for idx in range(1, len(disk_map), 2)]
    file_list = DoublyLinkedList(files)
    source_item = file_list.tail
    first_space = find_space(file_list.head, 1, file_list.tail)


    while source_item !=  first_space:
        if target_item := find_space(first_space, source_item.value.size, source_item):
            source = source_item.value
            target = target_item.value
            source_prev_item = file_list.remove(source_item)
            source_prev = source_prev_item.value

            source_prev.space += source.size + source.space
            source.space = target.space - source.size
            target.space = 0
            file_list.insert_after(source, target_item)
            source_item = source_prev_item
            first_space = find_space(first_space, 1, source_item)
        else:
            source_item = source_item.prev
    return expand_files(file_list)


def expand_files(disk):
    blocks = []
    for item in disk:
        file = item.value
        blocks += [file.id] * file.size
        blocks += [None] * file.space
    return blocks


def find_space(start, size, stop):
    while start and start != stop:
        if start.value.space >= size:
            return start
        start = start.next


def defrag_blocks(disk_map):
    disk = expand_map(disk_map)
    fill = 0
    move = len(disk) - 1

    def search():
        nonlocal fill
        nonlocal move
        while disk[fill] is not None:
            fill += 1
        while disk[move] is None:
            move -= 1

    search()
    while fill < move:
        disk[fill] = disk[move]
        disk[move] = None
        search()
    return disk


def checksum(disk):
    return sum(idx * fid for (idx, fid) in enumerate(disk) if fid is not None)


def expand_map(disk_map):
    disk = []
    fid = 0
    for idx in range(0, len(disk_map), 2):
        disk += [fid] * disk_map[idx]
        disk += [None] * disk_map[idx + 1]
        fid += 1
    return disk


def read():
    return open(f'./input/2024/day09/{INPUT}.txt').read().strip()


class File:
    def __init__(self, fid, size, space):
        self.id = fid
        self.size = size
        self.space = space

    def __repr__(self):
        return f'{self.id}x{self.size}[.{self.space}.]'


class DoublyLinkedList:
    class Item:
        def __init__(self, value, prev, next_item):
            self.value = value
            self.prev = prev
            self.next = next_item

        def __repr__(self):
            prev_id = self.prev.value.id if self.prev else None
            next_id = self.next.value.id if self.next else None
            return f'{prev_id}<-{self.value}->{next_id}'

    def __init__(self, values=()):
        self.head = None
        self.tail = None
        self.len = 0
        for value in values:
            self.insert_after(value)

    def insert_after(self, value, prev=None):
        if not self.head:
            self.head = self.Item(value, None, None)
            self.tail = self.head
            self.len += 1
            return self.head
        if not prev:
            prev = self.tail
        next_item = prev.next
        item = DoublyLinkedList.Item(value, prev, next_item)
        prev.next = item
        if next_item:
            next_item.prev = item
        if prev == self.tail:
            self.tail = item
        self.len += 1
        return item

    def remove(self, item):
        prev = item.prev
        next_item = item.next
        if prev:
            prev.next = next_item
        if next_item:
            next_item.prev = prev
        if item == self.head:
            self.head = next_item
        if item == self.tail:
            self.tail = prev
        self.len -= 1
        return prev

    def __iter__(self):
        item = self.head
        while item:
            yield item
            item = item.next

    def __len__(self):
        return self.len

    def __repr__(self):
        item_strings = [str(item) for item in self]
        return ', '.join(item_strings)


clockit(main)
