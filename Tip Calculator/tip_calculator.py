meal = input("How much was the meal? ")
percent = input("What percentage would you like to tip? ")
# YOUR CODE BELOW
# Step 1: Remove the $ from meal and convert to float

meal = float(meal[1:])

# Step 2: Remove the % from percent, convert to float, then turn into a decimal

percent = float(percent[:-1]) / 100

# Step 3: Calculate the tip

tip = meal * percent

# Step 4: Print the result

print(f"Leave: ${tip:.2f}")
