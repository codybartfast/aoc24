INPUT = 'input'


def main():
    equations = [parse(line) for line in read().splitlines()]

    ans1 = sum(
        result
        for result, operands in equations
        if any(result == value for value in variations(operands, False)))

    ans2 = sum(
        result
        for result, operands in equations
        if any(result == value for value in variations(operands, True)))

    print(f'Part 1: {ans1}\nPart 2: {ans2}')


def concatenate(a, b):
    factor = 10
    while b // factor:
        factor *= 10
    return a * factor + b


def variations(operands, include_concatenate=False):
    [*rest, operand] = operands
    if not rest:
        yield operand
    else:
        yield from (
            result
            for variation in variations(rest, include_concatenate)
            for result in ((variation + operand, variation * operand, concatenate(variation, operand))
                           if include_concatenate
                           else (variation + operand, variation * operand))
        )


def parse(line):
    (test_value, *operands) = [int(part.strip(':')) for part in line.split(' ')]
    return test_value, operands


def read():
    return open(f'./input/2024/day07/{INPUT}.txt').read().strip()


main()
