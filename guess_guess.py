# Import the random module so we can use the function to pick a number from a range
import random

# Set the maximum number of guesses
MAX_GUESSES = 4

# Set the range of numbers to guess from
MIN_NUMBER = 1
MAX_NUMBER = 100

# Get the user's guess
user_guess = int(input(f"Welcome to the guessing game. Enter a number between {MIN_NUMBER} and {MAX_NUMBER}: "))

# Set the target number
target_number = random.randint(MIN_NUMBER, MAX_NUMBER)

# Set the number of guesses made
num_guesses = 0

# Loop until the user guesses correctly or runs out of guesses
while num_guesses < MAX_GUESSES:
    # Check if the user's guess is valid
    if user_guess < MIN_NUMBER or user_guess > MAX_NUMBER:
        print(f"Invalid guess. Please enter a number between {MIN_NUMBER} and {MAX_NUMBER}.")
        user_guess = int(input("Enter a number: "))
    # Check if the user's guess is correct
    elif user_guess == target_number:
        print(f"Congratulations! You guessed the correct number in {num_guesses+1} guesses.")
        break
    # If the user's guess is not correct, increment the number of guesses and ask for another guess
    else:
        num_guesses += 1
        print(f"Incorrect guess. You have {MAX_GUESSES-num_guesses} guesses left.")
        user_guess = int(input("Enter another number: "))

# If the user runs out of guesses, print a message
if num_guesses == MAX_GUESSES:
    print(f"\nYou lose. You're out of guesses. The number I selected was {target_number}.")

