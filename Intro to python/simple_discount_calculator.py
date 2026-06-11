# -----------------------------------------
# Price Calculator with User Input
# -----------------------------------------

def calculate_price(original_price, discount_rate=0.10):
    """
    Calculate the final price after applying a discount.

    Parameters:
        original_price (float): The starting price of the item.
        discount_rate (float): The discount percentage (default = 0.10).

    Returns:
        float: The final price after discount.
    """
    discount_amount = original_price * discount_rate
    final_price = original_price - discount_amount
    return final_price


# -----------------------------------------
# User Input Section
# -----------------------------------------

# Get original price from the user
original_price = float(input("Enter the original price: "))

# Ask user if they want a custom discount
use_custom = input("Do you want to enter a custom discount rate? (yes/no): ").lower()

if use_custom == "yes":
    discount_rate = float(input("Enter discount rate (e.g., 0.20 for 20%): "))
    final = calculate_price(original_price, discount_rate)
else:
    final = calculate_price(original_price)  # uses default 10%

# Print the final price
print("Final price after discount:", final)
