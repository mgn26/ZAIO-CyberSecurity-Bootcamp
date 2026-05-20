"""
FizzBuzz is one of the most famous programming challenges in the world.

Condition: Output
Divisible by both 3 and 5: {number} - FizzBuzz
Divisible by 3 only: {number} - Fizz
Divisible by 5 only: {number} - Buzz
Divisible by neither: {number}
"""

print("Welcome to FizzBuzz!")

# Ask the user to enter a number

number = int(input("Enter a maximum number: "))

# Iterate through every number from 1 up to the input number
# and print Fizz if it's divisible by 3 or Buzz if it's divisible by 5.

for i in range(1, number + 1):
    if i % 3 == 0 and i % 5 == 0:
        print(f"{i} - FizzBuzz")
    elif i % 3 == 0:
        print(f"{i} - Fizz")
    elif i % 5 == 0:
        print(f"{i} - Buzz")
    else:
        print(f"{i}")

print(f"\nDone! Checked {number} numbers.")
