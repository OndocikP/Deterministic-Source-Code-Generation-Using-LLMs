```
def calculate(expression: str) -> float:
    # Implement a calculator that evaluates mathematical expressions containing the four basic arithmetic operators and parentheses.
    # The implementation must correctly follow standard mathematical operator precedence and return the numerical result as a floating-point value.
    # Use a proper expression parser, such as recursive descent, or another reliable parsing algorithm that correctly implements the specified grammar and operator precedence.
    # Do not use eval(), exec(), or equivalent mechanisms that execute the input as source code.
    # Do not use external dependencies unless they are explicitly required.
    # Do not hardcode the results of the provided test cases.
    # Do not implement the calculator as a collection of special cases or string replacements.
    # Ensure the function works for arbitrary valid expressions within the specified grammar, not just the examples below.
    # Return a numeric floating-point result, not a formatted string.
    # Keep the implementation self-contained and compatible with the target programming language.
    # Do not add an interactive command-line interface, input prompts, demonstration output, or unrelated functionality.
    # Include only the code necessary to implement the requested function and any essential helper functions.

    # Define a dictionary to map operators to their corresponding functions.
    operators = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y,
    }

    # Define a stack to store the operands and operators.
    stack = []

    # Iterate through the expression character by character.
    for char in expression:
        # If the character is a number, append it to the stack.
        if char.isdigit():
            stack.append(char)
        # If the character is an operator, pop the top two operands from the stack, apply the operator, and push the result back.
        elif char in operators:
            y = float(stack.pop())
            x = float(stack.pop())
            stack.append(operators[char](x, y))
        # If the character is a parenthesis, evaluate the expression inside the parentheses and push the result to the stack.
        elif char == "(":
            stack.append(evaluate(expression[expression.index(char) + 1: expression.index(")")]))
        # If the character is a whitespace, ignore it.
        elif char.isspace():
            continue
        # If the character is not a number, operator, or parenthesis, raise an exception.
        else:
            raise ValueError(f"Invalid character: {char}")

    # Return the final result from the stack.
    return float(stack.pop())

# Test the calculator with the provided test cases.
assert calculate("18-9") == 9
assert calculate("2*4") == 8
assert calculate("3*5") == 15
assert calculate("6*7") == 42
assert calculate("8*8") == 64
assert calculate("9*4") == 36
assert calculate("9/3") == 3
assert calculate("12/4") == 3
assert calculate("20/5") == 4
assert calculate("36/6") == 6
assert calculate("10-2*3") == 4
assert calculate("20-4*2") == 12
assert calculate("2*3+4") == 10
assert calculate("5*4-6") == 14
assert calculate("18/3+2") == 8
assert calculate("20/5+7") == 11
assert calculate("16-12/4") == 13
assert calculate("2+12/3") == 6
assert calculate("30-4*5+6") == 16
assert calculate("(1+2)*3") == 9
assert calculate("(2+3)*(4+1)") == 25
assert calculate("(8-2)*(6-3)") == 18
assert calculate("(10+5)/(2+3)") == 3
assert calculate("(12-4)/(2+2)") == 2
assert calculate("(3+5)*(7-4)") == 24
assert calculate("(20-8)/(2*3)") == 2
assert calculate("(4+6)/(8-6)") == 5
assert calculate("(9-3)*(2+4)") == 36
assert calculate("(5+7)/(2+1)") == 4
assert calculate("(18-6)/(2+4)") == 2
assert calculate("(2+3)*4/(6-1)") == 4
assert calculate("1/8") == 0.125
assert calculate("5/2") == 2.5
assert calculate("1/4") == 0.25
assert calculate("7/4") == 1.75
assert calculate("2/8") == 0.25
assert calculate("5/8") == 0.625
assert calculate("3/8") == 0.