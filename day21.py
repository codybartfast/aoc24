# Original mulled wine mess

import re
from stocking import clockit

INPUT = 'input'

num_coords = {
    char: (x, y)
    for y, line in enumerate(['789', '456', '123', ' 0A'])
    for x, char in enumerate(line)}

remote_coords = {
    char: (x, y)
    for y, line in enumerate([' ^A', '<v>'])
    for x, char in enumerate(line)}


def keypad_conundrum():
    codes = [line for line in lines()]
    num_pair_moves = find_pair_moves(num_coords)
    remote_pair_moves = find_pair_moves(remote_coords)
    ans1 = sum(complexity(num_pair_moves, remote_pair_moves, code) for code in codes)
    print(f'Part 1: {ans1}')

    known = {}
    ans2 = 0
    for code in codes:
        val = int(code[:-1])
        seqs = remote_sequences(num_pair_moves, [code], 'A')
        shorty = min(remote_length_n(remote_pair_moves, seq, 25, {}) for seq in seqs)
        comp = val * shorty
        ans2 += comp
    print(f'Part 2: {ans2}')


def remote_length_n(rpm, sequence, n, known):
    key = (n, 'seq', sequence)
    if key not in known:
        if n == 0 or sequence == '':
            return len(sequence)

        if '<' not in sequence:
            return shortest_remote_n(rpm, sequence, n - 1, known)
        left = match.group(0) if (match := re.search(r'^[^<]*<', sequence)) else ''
        mids = re.findall(r'(?<=<)[^<]*<', sequence)
        right = match.group(0) if (match := re.search(r'(?<=<)[^<]*$', sequence)) else ''

        length = 0

        for mid in mids:
            mid_key = (n, 'mid', mid)
            if mid_key not in known:
                known[mid_key] = shortest_remote_n(rpm, mid, n - 1, known, '<')
            length += known[mid_key]

        remote_left = shortest_remote(rpm, left)
        remote_right = shortest_remote(rpm, right, '<')

        length += shortest_remote_n(rpm, left, n - 1, known)
        length += shortest_remote_n(rpm, right, n - 1, known, '<')
        known[key] = length
    return known[key]


def shortest_remote_n(rpm, sequence, n, known, start = 'A'):
    possible_remote_sequences = remote_sequences(rpm, [sequence], start)
    return min(remote_length_n(rpm, possible, n, known) for possible in possible_remote_sequences)


def shortest_remote(remote_pair_moves, sequence, start = 'A'):
    return shortest(remote_sequences(remote_pair_moves, [sequence], start))


def complexity(num_pair_moves, remote_pair_moves, code):
    code_val = int(code[:-1])
    length = len(shortest(remote_sequence_3(num_pair_moves, remote_pair_moves, code)))
    return code_val * length


def shortest(strings):
    shortest_len = 1_000_000_000
    shortest_string = ''
    for string in strings:
        if len(string) < shortest_len:
            shortest_len = len(string)
            shortest_string = string
    return shortest_string


def remote_sequence_3(num_pair_moves, remote_pair_moves, code):
    r1 = remote_sequences(num_pair_moves, [code], 'A')
    r2 = remote_sequences(remote_pair_moves, r1, 'A')
    r3 = remote_sequences(remote_pair_moves, r2, 'A')
    return r3


def remote_sequences(pair_moves, sequences, start):
    return [
        remote_sequence
        for sequence in sequences
        for remote_sequence in
        expand(pair_moves[pair] for pair in zip(start + sequence, sequence))]


def expand(legs_options):
    if not legs_options:
        yield ''
    else:
        [options, *other_legs_options] = legs_options
        for right in expand(other_legs_options):
            for left in options:
                yield left + right


def find_pair_moves(coords):
    chars = [char for char in coords if char != ' ']
    return {
        (a, b): [var for var in pair_moves_variations(coords, a, b)
                 if not scares_robot(coords, a, var)]
        for a in chars
        for b in chars}


def scares_robot(coords, start, moves):
    scary = coords[' ']
    pos = coords[start]
    for move in moves:
        if move == '^':
            pos = (pos[0], pos[1] - 1)
        elif move == '>':
            pos = (pos[0] + 1, pos[1])
        elif move == 'v':
            pos = (pos[0], pos[1] + 1)
        elif move == '<':
            pos = (pos[0] - 1, pos[1])
        if pos == scary:
            return True
    return False


def pair_moves_variations(coords, a, b):
    return pair_moves_simple(coords, a, b)


def pair_moves_simple(coords, a, b):
    ax, ay = coords[a]
    bx, by = coords[b]
    left = ['<' for _ in range(ax - bx)]
    right = ['>' for _ in range(bx - ax)]
    up = ['^' for _ in range(ay - by)]
    down = ['v' for _ in range(by - ay)]
    return {''.join(left + right + up + down) + 'A', ''.join(up + down + left + right) + 'A'}


def lines():
    return open(f'./input/2024/day21/{INPUT}.txt').read().strip().splitlines()


clockit(keypad_conundrum)
