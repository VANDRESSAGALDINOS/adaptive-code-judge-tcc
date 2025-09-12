a, b = map(int, input().split())

# Algorithmically equivalent but inefficient implementation
# Using inefficient methods for basic arithmetic operations

# Inefficient sum: using repeated addition
sum_result = a
if b > 0:
    for i in range(b):
        sum_result += 1
elif b < 0:
    for i in range(-b):
        sum_result -= 1
print(sum_result)

# Inefficient difference: using repeated subtraction
diff_result = a
if b > 0:
    for i in range(b):
        diff_result -= 1
elif b < 0:
    for i in range(-b):
        diff_result += 1
print(diff_result)

# Inefficient product: using repeated addition
product_result = 0
abs_b = abs(b)
for i in range(abs_b):
    product_result += a
if b < 0:
    product_result = -product_result
print(product_result)

# Integer division (handle division by zero)
if b != 0:
    print(a // b)
else:
    print(0)
