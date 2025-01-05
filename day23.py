# Original mulled wine inspired mess

from stocking import clockit

INPUT = 'input'


def lan_party():
    connections = sorted(parse(line) for line in lines())

    ans1 = len(tee_trips(find_triples(connections.copy())))
    print(f'Part 1: {ans1}')

    largest = find_large(connections)
    ans2 = ','.join(sorted(largest))
    print(f'Part 2: {ans2}')


def find_large(connections):
    connections = set(connections)
    computers = sorted({
        connection[i] for i in [0, 1] for connection in connections
    })
    subnets = []
    while computers:
        computer = computers.pop(0)
        for subnet in subnets:
            if all((other, computer) in connections for other in subnet):
                subnets.append(subnet | {computer})
        subnets.append({computer})
    max_size = max(len(subnet) for subnet in subnets)
    [largest] = [subnet for subnet in subnets if len(subnet) == max_size]
    return largest


def tee_trips(triples):
    result = []
    for triple in triples:
        if any(addr.startswith('t') for addr in triple):
            result.append(triple)
    return result


def find_triples(connections):
    conset = set(connections)
    triples = []
    while connections:
        (a, b) = connections.pop(0)
        idx = 0
        while idx < len(connections) and connections[idx][0] != b:
            idx += 1
        while idx < len(connections) and connections[idx][0] == b:
            (_, c) = connections[idx]
            idx += 1
            if (a, c) in conset:
                triples.append((a, b, c))
    return triples


def parse(line):
    a, b = line.split('-')
    return (a, b) if a < b else (b, a)


def lines():
    return open(f'./input/2024/day23/{INPUT}.txt').read().strip().splitlines()


clockit(lan_party)
