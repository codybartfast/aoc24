# Original mulled wine inspired mess

from stocking import clockit

INPUT = 'input'


def monkey_market():
    initial_secrets = [int(line) for line in lines()]

    ans1 = 0
    for initial_secret in initial_secrets:
        last = gen_2000(initial_secret)[-1]
        ans1 += last
    print(f'Part 1: {ans1}')

    books = [first_price_for_signal(signal_and_price(secret)) for secret in initial_secrets]
    summary = combine_books(books)

    ans2 = max(summary.values())
    print(f'Part 2: {ans2}')


def combine_books(books):
    summary = {}
    for book in books:
        for signal, price in book.items():
            summary[signal] = summary.get(signal, 0) + price
    return summary


def first_price_for_signal(sap):
    book = {}
    for (signal, price) in sap:
        if signal not in book:
            book[signal] = price
    return book


def signal_and_price(secret):
    prices = unit_digits(gen_2000(secret))
    differences = price_differences(prices)
    histories = difference_histories(differences)
    return list(zip(histories, prices))[4:]


def difference_histories(differences):
    histories = [None] * 4
    for history in zip(differences[1:], differences[2:], differences[3:], differences[4:]):
        histories.append(history)
    return histories


def price_differences(prices):
    differences = [None]
    for price, next_price in zip(prices, prices[1:]):
        differences.append(next_price - price)
    return differences


def unit_digits(secrets):
    return [secret % 10 for secret in secrets]


def gen_2000(secret):
    secrets = [secret]
    for _ in range(2000):
        secret = next_secret(secret)
        secrets.append(secret)
    return secrets


def next_secret(secret):
    secret ^= secret * 64
    secret %= 16777216
    secret ^= (secret // 32)
    secret %= 16777216
    secret ^= secret * 2048
    secret %= 16777216
    return secret


def lines():
    return open(f'./input/2024/day22/{INPUT}.txt').read().strip().splitlines()


clockit(monkey_market)
