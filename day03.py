import re

def read():
    return open(f'./input/2024/day03/{input_name}.txt').read().strip()

def lex(text):
    return [match.group() for match in
            re.finditer(r'mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\)', text)]

def parse(tokens):
    for token in tokens:
        match token:
            case 'do()': yield True
            case 'don\'t()': yield False
            case _: yield [int(digits.group()) for digits in
                           re.finditer(r'\d+', token)]

def run(objs, part1):
    result = 0
    do = True
    for obj in objs:
        if obj == True: do = True
        elif obj == False: do = False
        elif part1 or do:
            result += obj[0] * obj[1]
    return result

input_name = 'input'

ans1 = run(parse(lex(read())), True)
ans2 = run(parse(lex(read())), False)

print(f'Part 1: {ans1}')
print(f'Part 2: {ans2}')