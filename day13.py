import re
from stocking import *

INPUT = 'input'


def The_Claw():
    machines = [parse(block) for block in blocks()]

    ans1 = 0
    for machine in machines:
        if ab := I_Have_Been_Chosen(*machine):
            ans1 += ab[0] * 3 + ab[1]
    print(f'Part 1: {ans1}')

    ans2 = 0
    for machine in machines:
        machine[4] += 10000000000000
        machine[5] += 10000000000000
        if ab := I_Have_Been_Chosen(*machine):
            ans2 += ab[0] * 3 + ab[1]
    print(f'Part 2: {ans2}')


def I_Have_Been_Chosen(ax, ay, bx, by, px, py):
    a_grad, b_grad, p_grad = ay / ax, by / bx, py / px
    if sorted([a_grad, b_grad, p_grad])[1] != p_grad:
        return None

    if a_grad < b_grad:
        return Ooooh(ax, ay, bx, by, px, py)
    else:
        ab = Ooooh(bx, by, ax, ay, px, py)
        return ab[::-1] if ab else None


def Ooooh(ax, ay, bx, by, px, py):
    low = 0
    high = 1 + px // ax
    while low < high:
        a = (low + high) // 2
        b = (px - a * ax) // bx
        b_float = (px - a * ax) / bx
        ydiff = a * ay + b_float * by - py
        if not ydiff and a * ax + b * bx == px:
            return a, b
        if ydiff >= 0:
            low = a + 1
        else:
            high = a


def parse(block):
    return [int(digits)
            for line in block.splitlines()
            for digits in re.findall(r'\d+', line)]


def blocks():
    return open(f'./input/2024/day13/{INPUT}.txt').read().strip().split('\n\n')


clockit(The_Claw)
