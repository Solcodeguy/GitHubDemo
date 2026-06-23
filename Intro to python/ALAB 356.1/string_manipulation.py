# string_manipulation.py

# Prompt the user for a sentence
sentence = input("Enter a sentence: ")

# 1. Convert to uppercase
print("Uppercase:", sentence.upper())

# 2. Reverse the sentence
print("Reversed:", sentence[::-1])

# 3. Count vowels (case-insensitive)
vowels = "aeiou"
count = sum(1 for char in sentence.lower() if char in vowels)
print("Vowel Count:", count)

# 4. Replace spaces with hyphens
print("Hyphens:", sentence.replace(" ", "-"))
