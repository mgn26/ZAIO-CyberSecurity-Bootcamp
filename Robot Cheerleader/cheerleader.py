"""
Robot Cheerleader — a program that takes a word from the user and cheers it
out, letter by letter and then delivers the grand finale.
"""

# Ask user for input
fav_word = input("Enter your favourite word: ")

fav_word = fav_word.upper()

# Loop through input string and perform the main action.
for char in fav_word:
    if char in ['A', 'E', 'I', 'O', 'U']:
        print(f"Give me an {char}!")
    else:
        print(f"Give me a {char}!")
else:
    print(f"What does it say????? {fav_word}!!!!!!")
