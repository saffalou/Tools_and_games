# scripts for calculating various lengths and areas

import math

ask_shape = input('What shape do you want to measure? (S)quare, (Rectangle), (T)riangle, (H)ypotenuse?: ').lower()

response = ask_shape



def square():
    ask_length_square = int(input("How long is one side of the square?: "))
    print("The area of your square is", ((ask_length_square * 4)))

def rectangle():
    ask_length_rectangle_short = int(input("What is the length of the short retangle side?: "))
        
    ask_length_rectangle_long = int(input("What is the length of the long retangle side?: "))
        
    print("The area of your rectangle is", (ask_length_rectangle_short * ask_length_rectangle_long))



def triangle_hypotenuse():
        ask_triangle_side_1 = int(input('What is the length of one side of your right angled traingle?: '))

        ask_triangle_side_2 = int(input('What is the length of the other side of your right angled traingle?: '))

        add_sides = (ask_triangle_side_1 ** 2) + (ask_triangle_side_2 ** 2)

        hypotenuse = math.sqrt(add_sides)

        print(f"Your hypotenuse length is {hypotenuse:.4f}")

   
        
        



if response == "s":
    square()
elif response == 'r':
    rectangle()
elif response == 'h':
    triangle_hypotenuse()

    
