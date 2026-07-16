# multiplier_closure.py

def make_multiplier(factor):
    """Returns a closure that multiplies input x by the given factor."""
    def multiplier(x):
        return x * factor
    return multiplier

# --- Demonstration Code ---
times3 = make_multiplier(3)
times10 = make_multiplier(10)

print("Multiplier Closure Demo:")
print(f"times3(7) = {times3(7)}")     # 21
print(f"times10(7) = {times10(7)}")   # 70
