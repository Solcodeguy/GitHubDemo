# even_sum.py Using a for loop

even_sum = 0

for num in range(1, 51):
    if num % 2 == 0:
        even_sum += num

print(f"The sum of even numbers from 1 to 50 is {even_sum}.")
# even_sum.py Using a while loop

even_sum_while = 0
num = 1

while num <= 50:
    if num % 2 == 0:
        even_sum_while += num
    num += 1

print(f"(While loop) The sum of even numbers from 1 to 50 is {even_sum_while}.")
