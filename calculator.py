"""A simple interactive calculator. Run with: python calculator.py"""

import math


def calculate(first: float, operator: str, second: float) -> float:
    """Calculate a result without evaluating arbitrary Python code."""
    if not math.isfinite(first) or not math.isfinite(second):
        raise ValueError("Please enter finite numbers.")

    if operator == "+":
        result = first + second
    elif operator == "-":
        result = first - second
    elif operator == "*":
        result = first * second
    elif operator == "/":
        if second == 0:
            raise ValueError("Cannot divide by zero.")
        result = first / second
    else:
        raise ValueError("Choose +, -, *, or /.")

    if not math.isfinite(result):
        raise ValueError("The result is too large.")
    return result


def read_number(prompt: str) -> float:
    while True:
        value = input(prompt).strip()
        if value.lower() in {"q", "quit", "exit"}:
            raise EOFError
        try:
            number = float(value)
            if math.isfinite(number):
                return number
        except ValueError:
            pass
        print("Please enter a valid finite number, such as 12 or -3.5.")


def main() -> None:
    print("Python Calculator")
    print("Operations: +  -  *  / | Type q at any prompt to quit.")
    try:
        while True:
            first = read_number("\nFirst number: ")
            while True:
                operator = input("Operation (+, -, *, /): ").strip()
                if operator.lower() in {"q", "quit", "exit"}:
                    raise EOFError
                if operator in {"+", "-", "*", "/"}:
                    break
                print("Choose +, -, *, or /.")
            second = read_number("Second number: ")
            try:
                result = calculate(first, operator, second)
                print(f"Result: {first:g} {operator} {second:g} = {result:g}")
            except ValueError as error:
                print(f"Error: {error}")
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
