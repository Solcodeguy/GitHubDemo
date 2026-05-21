# logic_bits.py

# Logical operators
a = bool(int(input("Enter first boolean (1 or 0): ")))
b = bool(int(input("Enter second boolean (1 or 0): ")))

print("a AND b =", a and b)
print("a OR b  =", a or b)
print("NOT a   =", not a)

# Bitwise operators
x = 5
y = 3

print("\nBitwise operations on 5 and 3:")
print("x in binary:", bin(x))
print("y in binary:", bin(y))

print("x & y =", bin(x & y))
print("x | y =", bin(x | y))
print("x ^ y =", bin(x ^ y))
print("~x    =", bin(~x))
print("x << 1 =", bin(x << 1))
print("x >> 1 =", bin(x >> 1))
