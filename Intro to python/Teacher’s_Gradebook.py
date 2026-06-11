# -----------------------------------------
# Filter Passing Scores with User Input
# -----------------------------------------

# Ask the user to enter scores separated by spaces
user_input = input("Enter exam scores separated by spaces: ")

# Convert the input string into a list of integers
raw_scores = []

for value in user_input.split():
    try:
        raw_scores.append(int(value))
    except ValueError:
        print(f"Warning: '{value}' is not a valid number and will be ignored.")

passing_scores = []

# Loop through each score and filter passing ones
for score in raw_scores:
    if score >= 60:
        passing_scores.append(score)

print("Passing scores:", passing_scores)
