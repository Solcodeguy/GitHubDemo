# bubble_sort_demo.py

arr = [64, 25, 12, 22, 11]

print("Original list:", arr)

n = len(arr)

for i in range(n):
    # Print progress of each pass
    print(f"Pass {i + 1}: {arr}")

    for j in range(0, n - i - 1):
        if arr[j] > arr[j + 1]:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]

print("Sorted list:", arr)
