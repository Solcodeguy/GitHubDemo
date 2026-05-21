# list_operations.py

numbers = [12, 5, 33, 7, 18]

print("Original list:", numbers)

# Sorted copy
print("Sorted list (using sorted()):", sorted(numbers))

# Sort in place
numbers.sort()
print("List after .sort():", numbers)

# Append a new element
numbers.append(42)
print("After appending 42:", numbers)

# Remove an element (remove by value)
numbers.remove(7)
print("After removing 7:", numbers)

# Reverse the list
numbers.reverse()
print("Reversed list:", numbers)
