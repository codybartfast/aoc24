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

    while source_item:
        if target_item := find_space(file_list, source_item):
            source = source_item.value
            target = target_item.value
            source_prev_item = file_list.remove(source_item)
            source_prev = source_prev_item.value

            source_prev.space += source.size + source.space
            source.space = target.space - source.size
            target.space = 0
            file_list.insert_after(source, target_item)
            source_item = source_prev_item
        else:
            source_item = source_item.prev
    return expand_files(file_list)


def expand_files(disk):
    blocks = []
    for item in disk:
        file = item.value
        blocks += [file.id] * file.size
        blocks += [None] * file.space
        item = item.next
    return blocks


def find_space(disk, item_to_move):
    item = disk.head
    while item and item != item_to_move:
        if item.value.space >= item_to_move.value.size:
            return item
        item = item.next


def defrag_blocks(disk_map):
    disk = expand_map(disk_map)
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
    return disk


def checksum(disk):
    return sum(idx * id for (idx, id) in enumerate(disk) if id != None)


def expand_map(disk_map):
    disk = []
    id = 0
    for idx in range(0, len(disk_map), 2):
        disk += [id] * disk_map[idx]
        disk += [None] * disk_map[idx + 1]
        id += 1
    return disk


def read():
    return open(f'./input/2024/day09/{INPUT}.txt').read().strip()


class File:
    def __init__(self, id, size, space):
        self.id = id
        self.size = size
        self.space = space

    def __repr__(self):
        return f'{self.id}x{self.size}[.{self.space}.]'


class DoublyLinkedList:
    class Item:
        def __init__(self, value, prev, next):
            self.value = value
            self.prev = prev
            self.next = next

        def __repr__(self):
            prev_id = self.prev.value.id if self.prev else None
            next_id = self.next.value.id if self.next else None
            return f'{prev_id}<-{self.value}->{next_id}'

    def __init__(self, values=[]):
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
        next = prev.next
        item = DoublyLinkedList.Item(value, prev, next)
        prev.next = item
        if next:
            next.prev = item
        if prev == self.tail:
            self.tail = item
        self.len += 1
        return item

    def remove(self, item):
        prev = item.prev
        next = item.next
        if prev:
            prev.next = next
        if next:
            next.prev = prev
        if item == self.head:
            self.head = next
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


main()
