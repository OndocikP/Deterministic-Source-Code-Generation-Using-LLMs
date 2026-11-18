def calculate(expression: str) -> float:
    # Implement a calculator that evaluates mathematical expressions containing the four basic arithmetic operators and parentheses.
    # The implementation must correctly follow standard mathematical operator precedence and return the numerical result as a floating-point value.

    # Use a proper expression parser, such as recursive descent, or another reliable parsing algorithm that correctly implements the specified grammar and operator precedence.
    # Do not use `eval()`, `exec()`, or equivalent mechanisms that execute the input as source code.
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

    # Iterate through the expression and evaluate each token.
    for token in expression.split():
        # If the token is a number, push it to the stack.
        if token.isdigit():
            stack.append(float(token))
        # If the token is an operator, evaluate the expression and push the result to the stack.
        elif token in operators:
            right = stack.pop()
            left = stack.pop()
            stack.append(operators[token](left, right))
        # If the token is a parenthesis, evaluate the expression inside the parenthesis and push the result to the stack.
        elif token == "(":
            stack.append(evaluate_expression(stack.pop()))
        elif token == ")":
            stack.append(evaluate_expression(stack.pop()))

    # Return the final result from the stack.
    return stack.pop()

def evaluate_expression(expression: str) -> float:
    # Implement a function to evaluate an expression inside parentheses.
    # The function should take an expression as a string and return the numerical result as a floating-point value.

    # Use the same implementation as the `calculate` function, but with a smaller scope.
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

    # Iterate through the expression and evaluate each token.
    for token in expression.split():
        # If the token is a number, push it to the stack.
        if token.isdigit():
            stack.append(float(token))
        # If the token is an operator, evaluate the expression and push the result to the stack.
        elif token in operators:
            right = stack.pop()
            left = stack.pop()
            stack.append(operators[token](left, right))
        # If the token is a parenthesis, evaluate the expression inside the parenthesis and push the result to the stack.
        elif token == "(":
            stack.append(evaluate_expression(stack.pop()))
        elif token == ")":
            stack.append(evaluate_expression(stack.pop()))

    # Return the final result from the stack.
    return stack.pop()