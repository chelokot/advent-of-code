from collections import defaultdict

with open("input.txt") as f:
    buyers = map(int, f.read().splitlines())

def mix(a, b):
    return a ^ b

def prune(a):
    return a % 16777216

def next_secret(secret):
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    secret = prune(mix(secret, secret * 2048))
    return secret

def price(secret):
    return secret % 10

combination_to_result = defaultdict(int)

count = 0
STEPS = 2000
for buyer in buyers:
    combination_to_monkey_result = defaultdict(int)
    prices = [price(buyer)]
    for i in range(STEPS):
        buyer = next_secret(buyer)
        prices.append(price(buyer))
    changes = []
    for old_price, new_price in zip(prices[:-1], prices[1:]):
        changes.append(new_price - old_price)
    for i in range(4, len(changes)):
        if tuple(changes[i - 4:i]) not in combination_to_monkey_result:
            combination_to_monkey_result[tuple(changes[i - 4:i])] = prices[i]
    for combination, result in combination_to_monkey_result.items():
        combination_to_result[combination] += result

print(max(combination_to_result.items(), key = lambda x: x[1]))
