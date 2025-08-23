a, b = map(int, input().split())

# Intentionally slow: unnecessary nested loops O(n²) where n=50000
# This should definitely exceed time limits calibrated for O(1)
for i in range(50000):
    for j in range(50000):
        # Waste CPU time with meaningless computation
        x = (i * j + a * b) % 1000000

# Still produce correct output
print(a + b)
print(a - b)
print(a * b)

if b != 0:
    print(a // b)
else:
    print(0)
