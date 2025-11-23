# import random so we can use the function to pick a number from a range
import random
import time

# variables
get_number = input("Welcome to the guessing game. Enter a number between 1 and 100: ")
numbers_list =range(1,100)
target = random.choice(numbers_list)
my_guess = int(get_number)


#code
counter = 0
# set counter for number of maximumgueses
while counter <= 4:
# if somebody enters value above 100, throw an error, ask for another guess
    if  my_guess > 100:
        print('checking the number you entered ...')
        time.sleep(2)
        print ((f"You're number {my_guess} is invalid. Please enter a number between 1 and 100"))
        get_number = input("Enter a number between 1 and 100: ")
# if somebody enters value below 1, throw an error, ask for another guess
    elif my_guess < 1:
         print('checking the number you entered ...')
         time.sleep(2)
         print(f"You're number23, {my_guess} is invalid. Please enter a number between 1 and 100")
         get_number = input("Enter a number between 1 and 100: ")

# if the value entered is valid but not equal to selected value, ask for another guess
    elif my_guess != target:
# increment the counter when we enter this part of the loop
        counter += 1
        print('checking the number you entered ...')
        time.sleep(2)
        print(f"Your guess {my_guess}  is valid but it is not equal to the number I selected")
        print('You can have another guess!')
        print(f'You have {5 - counter } guesses left')
        get_number = input("Enter a number between 1 and 100: ")

# if the value entered is equal to selected value, print out that they guessed correctly and exit the game
    elif my_guess == target: 
        print('checking the number you entered ...')
        time.sleep(2)
        print("Your number is equal to the number I selected")
        print('you win!')
        break

    if counter == 4:
      print('checking the number you entered ...')
      time.sleep(2)
      print('\nYou lose. You\'re out of guesses. The number I selected was ', target)
      break

    

