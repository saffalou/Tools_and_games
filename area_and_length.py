import math


class BadResponse(Exception):
    """Exception raised for invalid user responses."""
    pass


class Shapes:
    def square_area(self, side_a: float) -> float:
        """Calculate the area of a square."""
        return side_a ** 2

    def rectangle_area(self, side_a: float, side_b: float) -> float:
        """Calculate the area of a rectangle."""
        return side_a * side_b

    def triangle_hypotenuse(self, side_a: float, side_b: float) -> float:
        """Calculate the hypotenuse of a right-angled triangle."""
        return math.sqrt(side_a ** 2 + side_b ** 2)

    def triangle_area(self, base: float, height: float) -> float:
        """Calculate the area of a triangle."""
        return (base * height) / 2

    def circle_area(self, radius: float) -> float:
        """Calculate the area of a circle."""
        return math.pi * (radius ** 2)

    def circle_diameter(self, radius: float) -> float:
        """Calculate the diameter of a circle."""
        return 2 * radius

    def circle_circumference(self, radius: float) -> float:
        """Calculate the circumference of a circle."""
        return 2 * math.pi * radius


def get_int_input(prompt: str) -> float:
    """Prompt the user for an integer input, retrying until valid."""
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter an integer value.")


def main():
    shape_object = Shapes()

    while True:
        initial_prompt = input(
            'What shape do you want to measure? (S)quare, (R)ectangle, (T)riangle, (H)ypotenuse? Enter Q to exit the program: ').upper()

        if initial_prompt == "Q":
            break

        try:
            if initial_prompt not in ['S', 'R', 'T', 'H']:
                raise BadResponse(
                    "Invalid response. Please enter 'S', 'R', 'T', 'H', or 'Q'.")
        except BadResponse as e:
            print(e)
            continue

        if initial_prompt == "S":
            side_a = get_int_input("How long is one side of the square?: ")
            square_area = shape_object.square_area(side_a)
            print(f"The area of your square is {square_area:.3f} square units")

        elif initial_prompt == "R":
            side_a = get_int_input("Enter the length of side A of the rectangle: ")
            side_b = get_int_input("Enter the length of side B of the rectangle: ")
            rectangle_area = shape_object.rectangle_area(side_a, side_b)
            print(f"The area of your rectangle is {rectangle_area:.3f} square units")

        elif initial_prompt == "T":
            base = get_int_input("Enter the base of the triangle: ")
            height = get_int_input("Enter the height of the triangle: ")
            triangle_area = shape_object.triangle_area(base, height)
            print(f"The area of your triangle is {triangle_area:.3f} square units")

        elif initial_prompt == "H":
            side_a = get_int_input("Enter side A of the triangle: ")
            side_b = get_int_input("Enter side B of the triangle: ")
            hypotenuse = shape_object.triangle_hypotenuse(side_a, side_b)
            print(f"The hypotenuse of your triangle is {hypotenuse:.3f} units")


if __name__ == "__main__":
    main()