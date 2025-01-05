from stocking import clockit

INPUT = 'input'


def chronospatial_computer():
    initial_state = parse(lines())
    computer = Computer(*initial_state)
    ans1 = ','.join(str(n) for n in computer.run().output)
    print(f'Part 1: {ans1}')
    ans2 = aquine(computer.program)
    print(f'Part 2: {ans2}')


def run(A, program):
    return Computer(A, 0, 0, program).run().output


def aquine(program):
    length = len(program)
    zeros = [0] * length

    candidates = {(0, tuple(zeros))}
    good_starts = []
    while candidates:
        idx, octals_tup = candidates.pop()
        octals = list(octals_tup)
        if idx == length - 3:
            good_starts.append(octals)
        else:
            for i in range(8):
                octals[idx] = i
                key_octals = octals.copy()
                key_octals[idx + 1] = 0
                key_octals[idx + 2] = 0
                future = idx + 1, tuple(key_octals)
                for j in range(8):
                    octals[idx + 1] = j
                    for k in range(8):
                        octals[idx + 2] = k
                        out = list(run(octals_value(octals), program))
                        if out[-(idx + 1):] == program[-(idx + 1):]:
                            candidates.add(future)

    good_starts.sort()
    for octals in good_starts:
        for i in range(8):
            octals[length - 3] = i
            for j in range(8):
                octals[length - 2] = j
                for k in range(8):
                    octals[length - 1] = k
                    if list(run(octals_value(octals), program)) == program:
                        return octals_value(octals)


def octals_value(octals):
    length = len(octals)
    val = 0
    for idx in range(length):
        val += octals[idx] * (8 ** (length - 1 - idx))
    return val


def parse(lines):
    return (
        int(lines[0].split()[2]),
        int(lines[1].split()[2]),
        int(lines[2].split()[2]),
        [int(digit) for digit in lines[4].split()[1].split(',')])


def lines():
    return open(f'./input/2024/day17/{INPUT}.txt').read().strip().splitlines()


class Computer:
    def __init__(self, a=0, b=0, c=0, program=None):
        if not program:
            raise ValueError('program please')
        self.a = a
        self.b = b
        self.c = c
        self.program = program
        self.pointer = 0
        self.output = []

    def tick(self):
        def combo(operand):
            match operand:
                case 0 | 1 | 2 | 3:
                    return operand
                case 4:
                    return self.a
                case 5:
                    return self.b
                case 6:
                    return self.c
                case _:
                    raise ValueError(f'Invalid operand: {operand}')

        if self.pointer >= len(self.program):
            return False

        opcode = self.program[self.pointer]
        operand = self.program[self.pointer + 1]

        match opcode:
            case 0:  # adv
                # print(f'0: {self.a} -> ', end='')
                self.a = self.a // (2 ** combo(operand))
                # print(f'{self.a}')
            case 1:  # bxl
                self.b = self.b ^ operand
            case 2:  # bst
                self.b = combo(operand) % 8
            case 3:  # jnz
                if self.a != 0:
                    self.pointer = operand - 2
            case 4:  # bxc
                self.b = self.b ^ self.c
            case 5:  # out
                self.output.append(combo(operand) % 8)
            case 6:  # bdv
                self.b = self.a // (2 ** combo(operand))
            case 7:  # cdv
                self.c = self.a // (2 ** combo(operand))
        self.pointer += 2
        return True

    def run(self):
        while self.tick():
            pass
        return self

    def __repr__(self):
        return f'[{self.a}, {self.b}, {self.c}, p={self.pointer} {self.program}, {self.output}]'


clockit(chronospatial_computer)
