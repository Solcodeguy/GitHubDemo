# -----------------------------------------
# Age Verification with Error Handling
# -----------------------------------------

user_input = input("Enter your age: ")

try:
    age = int(user_input)
    print("Success! Your age is:", age)

except ValueError:
    print("Error: That is not a valid number!")
