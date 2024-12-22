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

count = 0
STEPS = 2000
for buyer in buyers:
    for i in range(STEPS):
        buyer = next_secret(buyer)
    print(buyer)
    count += buyer
print(count)
