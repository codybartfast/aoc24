# Original mulled wine + Black Fox cider inspired mess.

# Got answer with a mix of code and head scratching
# so this isn't a general solution

from stocking import clockit

INPUT = 'input'

def crossed_wires():
    base_wires, wires, gates = build_monitor(lines())

    levels = find_levels(base_wires, gates)
    tick(levels)

    ans1 = read_out(wires)
    print(f'Part 1: {ans1}')

    print('Check 1:')
    check_many(wires)
    print('\n')
    print('Check 2:')
    check_many(wires)

    ans2 = ','.join(sorted(swapped))
    print(f'Part 2: {ans2}')


def check_many(wires):
    c = check_0(wires)
    for bit in range(1, 45):
        c = check_n(wires, bit, c)


def check_n(wires, n , c):
    # print(f'checking: {n}, c:{c}')
    x = wires[f'x{n:02}']
    y = wires[f'y{n:02}']
    z = wires[f'z{n:02}']

    xor1, and1 = check_share_adder(x, y, 'first adder')
    result = check_share_adder(c, xor1.wire_out, 'second adder')
    if result is None:
        return
    xor2, and2 = result
    if xor2.wire_out != z:
        print('not right z out of xor:', xor2, 'expected', z)
        # apply_swap(xor2, z.start)
        apply_swap_wires(xor2.wire_out, z)
    or_wire = check_shared_or(and1, and2, n)
    next_types = sorted([ep.kind for ep in  or_wire.endpoints])
    if next_types != ['AND', 'XOR']:
        print(f'OR goes to unexpected types: {next_types}')
    return or_wire


def check_0(wires):
    x = wires['x00']
    y = wires['y00']
    z = wires['z00']

    xor_gate, and_gate = check_share_adder(x, y, 'zero')

    if xor_gate.wire_out != z:
        print('not right z out of xor:', xor_gate)
    return and_gate.wire_out

def check_shared_or(a, b, n):
    if len(a.wire_out.endpoints) != 1:
        print('and1 doesn\'t have one endpoint:', a)
    if len(b.wire_out.endpoints) != 1:
        print('and2 doesn\'t have one endpoint:', a)
    if a.wire_out.endpoints[0] != b.wire_out.endpoints[0]:
        print('and1 and and2 don\'t share endpoint:', a, ',', b)
    or_gate = a.wire_out.endpoints[0]
    if or_gate.kind != 'OR':
        print('Or is not right kind:', or_gate)
    # print(f'{n} -> carry out:{or_gate.wire_out.name}')
    return or_gate.wire_out

def check_share_adder(a, b, source):
    a_eps = set(a.endpoints)
    b_eps = set(b.endpoints)
    abc_eps = a_eps | b_eps
    if not (2 == len(a_eps) == len(b_eps) == len (abc_eps)):
        print('Not shared adder:', source)

        # This isn't general logic,
        # it's the result of manual poking around ...
        xor_gate, and_gate = a.endpoints
        rss = xor_gate.wire_b
        x31 = rss.start.wire_a
        fst_and = x31.endpoints[0]
        fst_xor = x31.endpoints[1]
        apply_swap(fst_xor, fst_and)


    [xor_gate, and_gate] = a.endpoints
    if xor_gate.kind != 'XOR':
        [xor_gate, and_gate] = [and_gate, xor_gate]
    if xor_gate.kind != 'XOR' or and_gate.kind != 'AND':
        print('not right types:', xor_gate, and_gate)
        return None
    return xor_gate, and_gate


def apply_swap_wires(w1, w2):
    print(f'SWAPPING {w1.name} and {w2.name}')
    apply_swap(w1.start, w2.start)

swapped = []
def apply_swap(gate_a, gate_b):
    swapped.append(gate_a.wire_out.name)
    swapped.append(gate_b.wire_out.name)
    out_a = gate_a.wire_out
    gate_a.wire_out = gate_b.wire_out
    gate_b.wire_out = out_a

def test_numbers(length):
    return [to_binary(2 ** n - 1, length) for n in range(length + 1)]

def set_inputs(wires, n1, n2):
    size = len([name for name in wires if name[0] == 'x'])
    for idx, bit in enumerate(to_binary(n1, size)):
        set_x(wires, idx, bit)
    for idx, bit in enumerate(to_binary(n2, size)):
        set_y(wires, idx, bit)

def set_x(wires, idx, value):
    wires[f'x{idx:02}'].value = value

def set_y(wires, idx, value):
    wires[f'y{idx:02}'].value = value

def get_z(wires, idx):
    return wires[f'z{idx:02}'].value

def to_binary(n, length):
    bits = []
    while n:
        bits.append(n & 1)
        n >>= 1
        length -= 1
    while length > 0:
        bits.append(0)
        length -= 1
    return bits

def read_out(wires):
    return to_decimal(
        z_values(wires)
    )

def to_decimal(z_values):
    n = 0
    for z in reversed(z_values):
        n <<= 1
        n |= z
    return n

def z_values(wires):
    return tuple(wires[wire].value for wire in sorted(wire for wire in wires if wire[0] == 'z'))

def tick(levels):
    for level in levels:
        for gate in level:
            gate.update()

def find_levels(base_wires, gates):
    known_wires = set(base_wires)
    unknown_gates = set(gates)
    known_gates = set()
    levels = []
    while unknown_gates:
        level = []
        for gate in unknown_gates.copy():
            if gate.wire_a in known_wires and gate.wire_b in known_wires:
                known_gates.add(gate)
                known_wires.add(gate.wire_out)
                level.append(gate)
                unknown_gates.remove(gate)
        levels.append(tuple(level))
    return tuple(levels)


def build_monitor(lines):
    gap = lines.index('')

    base_wires = tuple(Wire((parts := wire.split(': '))[0], int(parts[1])) for wire in lines[:gap])
    wires = {wire.name: wire for wire in base_wires}
    gates = []
    for gate_info in lines[gap+1:]:
        [wire_a, kind, wire_b, _, wire_out] = gate_info.split()
        for wire in [wire_a, wire_b, wire_out]:
            if wire not in wires:
                wires[wire] = Wire(wire, 0)
        gates.append(gate := Gate(wires[wire_a], kind, wires[wire_b], wires[wire_out]))
        if wires[wire_out].start:
            raise AssertionError('Tried to set wire start twice')
        wires[wire_out].start = gate
        wires[wire_a].endpoints.append(gate)
        wires[wire_b].endpoints.append(gate)
    return base_wires, wires, tuple(gates)

def lines():
    return open(f'./input/2024/day24/{INPUT}.txt').read().strip().splitlines()

class Wire:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.start = None
        self.endpoints = []

    def __repr__(self):
        return f'<{self.name}: {self.value} (-> {len(self.endpoints)})>'


class Gate:

    def __init__(self, wire_a, kind, wire_b, wire_out):
        self.wire_a = wire_a
        self.wire_b = wire_b
        self.wire_out = wire_out
        self.kind = kind
        match kind:
            case 'AND': self.calc = lambda a, b: a & b
            case 'OR': self.calc = lambda a, b: a | b
            case 'XOR': self.calc = lambda a, b: a ^ b
            case _: raise Exception(f'Unknown kind: {kind}')

    def update(self):
        self.wire_out.value = self.calc(self.wire_a.value, self.wire_b.value)

    def __repr__(self):
        return f'{self.wire_a.name} {self.kind} {self.wire_b.name} -> {self.wire_out.name}'
clockit(crossed_wires)