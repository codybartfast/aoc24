from functools import cmp_to_key

INPUT = 'input'


def main():
    rules, updates = parse(read())
    ans1, ans2 = 0, 0
    for update in updates:
        ordered = sorted(update,
                         key=cmp_to_key(lambda a, b: compare(rules, a, b)))
        mid = ordered[len(ordered) // 2]
        if ordered == update:
            ans1 += mid
        else:
            ans2 += mid
    print(f'Part 1: {ans1}\nPart 2: {ans2}')


def compare(rules, a, b):
    if [a, b] in rules:
        return -1
    if [b, a] in rules:
        return 1
    return 0


def parse(text):
    part1, part2 = text.split('\n\n')
    return (
        [[int(digits) for digits in line.split('|')] for line in part1.splitlines()],
        [[int(digits) for digits in line.split(',')] for line in part2.splitlines()])


def read():
    return open(f'./input/2024/day05/{INPUT}.txt').read().strip()


main()
