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

def clockit(action, repeat=1):
    from timeit import timeit
    time = timeit(action, number=repeat)
    print(f"\n'{action.__name__}' took {(time / repeat):.3f} seconds")
