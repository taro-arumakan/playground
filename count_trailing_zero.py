import re

def prime_occurrences(number, prime=5):
    if not number % prime:
        return 1 + prime_occurrences(number / prime)
    return 0

res = 1
for i in range(100, 201):
    res *= i
    n = prime_occurrences(i)
    if n:
        m = re.match(".*?(0*)$", str(res))
        print(i, n, m.groups()[0])

print(res)
print(len(m.groups()[0]))


res = 1
for i in range(100, 201):
    res *= i
    if not res % 5:
        print(i, res)
