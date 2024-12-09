INPUT = 'input'

class File:
    def __init__(self, id, size):
        self.id = id
        self.size = size

    def __repr__(self):
        return f'F{self.id}:{self.size}'

class Section:
    def __init__(self, initial_files, free_space):
        self.files = initial_files
        self.free_space = free_space

    def add(self, file):
        if self.free_space >= file.size:
            self.files.append(file)
            self.free_space -= file.size
            return True
        return False

    def remove(self, file):
        self.files.remove(file)
        self.free_space += file.size

    def to_map(self):
        map = []
        for file in self.files[0:-1]:
            map += [file.size, 0]
        map += [self.files[-1].size, self.free_space]
        return map

    def __repr__(self):
        return f'{self.files}_{self.free_space}'

def main():
    map = read()
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

    sections = init_sections(map)
    file_count = len(map) // 2
    for file_id in range(file_count, -1, -1):
        move_file(sections, file_id)

    disk2 = []
    for section in sections:
        for file in section.files:
            disk2 += [file.id] * file.size
        disk2 += [None] * section.free_space

    ans2 = checksum(disk2)

    print(f'Part 1: {ans1}')
    print(f'Part 2: {ans2}')

def move_file(sections, file_id):
    left_sections = []
    for (source_idx, source) in enumerate(sections):
        for file in source.files:
            if file.id == file_id:
                for target in left_sections:
                    if target.add(file):
                        # file is right most file in section (including only file in section)
                        if file == source.files[-1]:
                            source.remove(file)
                            if not source.files:
                                sections.remove(source)
                                left_sections[-1].free_space += source.free_space
                        # file is left_most with more files to right
                        elif file == source.files[0]:
                            source.files.remove(file)
                            left_sections[-1].free_space += file.size
                        # removing file from middle of section
                        else:
                            file_idx = source.files.index(file)
                            left_files = source.files[:file_idx]
                            new_section = Section(left_files, file.size)
                            sections.append(new_section, source_idx)
                            for file in left_files:
                                source.files.remove(file)
                        return True

        left_sections.append(source)



def init_sections(map):
    map = [int(digit) for digit in map]
    map.append(0)
    sections = []
    id = 0
    for idx in range(0, len(map), 2):
        file = File(id, map[idx])
        section = Section([file], map[idx+1])
        sections.append(section)
        id += 1
    return sections

def checksum(disk):
    return sum(idx * id for (idx, id) in enumerate(disk) if id != None)

def parse(line):
    return line

def init_disk(map):
    map = [int(digit) for digit in map]
    if len(map) % 2 == 0:
        raise ValueError('Exepected odd map length')
    map.append(0)
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