def evaluate_expression(expression: str) -> float:
    # Initialize the result to 0
    result = 0

    # Iterate through the characters in the expression
    for char in expression:
        # If the character is a number, add it to the result
        if char.isdigit():
            result = result * 10 + int(char)
        # If the character is an operator, perform the operation and update the result
        elif char in "+-*/":
            if char == "+":
                result += result
            elif char == "-":
                result -= result
            elif char == "*":
                result *= result
            elif char == "/":
                result /= result
        # If the character is a parenthesis, handle it appropriately
        elif char == "(":
            result = evaluate_expression(expression[expression.index(char) + 1: expression.index(char) + 1])
        # If the character is a decimal point, handle it appropriately
        elif char == ".":
            result = result * 10 + int(char)

    return result