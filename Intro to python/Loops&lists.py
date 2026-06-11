# Create a list of numbers from 1 to 20
numbers = list(range(1, 21))

# Create an empty list
multipliesOf3 = []

# Loop through numbers and collect those divisible by 3
for i in numbers:
    if i % 3 == 0:
        multipliesOf3.append(i)

# Print the final list
print(multipliesOf3)
