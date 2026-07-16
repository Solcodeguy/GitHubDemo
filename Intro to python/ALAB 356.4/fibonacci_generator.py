# fibonacci_generator.py

def gen_fibonacci(n):
    """Generator that yields the first n Fibonacci numbers."""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# --- Test Code ---
print("Fibonacci Sequence:")
for index, value in enumerate(gen_fibonacci(10)):
    print(f"Fibonacci #{index}: {value}")
