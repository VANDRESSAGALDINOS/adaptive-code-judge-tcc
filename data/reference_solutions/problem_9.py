a, b = map(int, input().split())

# Sum
print(a + b)

# Difference
print(a - b)

# Product
print(a * b)

# Integer division (handle division by zero)
if b != 0:
    print(a // b)
else:
    print(0)
