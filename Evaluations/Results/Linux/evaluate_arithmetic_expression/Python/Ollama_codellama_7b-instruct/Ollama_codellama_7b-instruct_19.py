def evaluate_expression(expression: str) -> float:
    # Initialize a stack to store the operators and operands
    stack = []

    # Iterate through the expression string
    for char in expression:
        # If the character is a number, append it to the stack
        if char.isdigit():
            stack.append(char)
        # If the character is an operator, pop the top two operands from the stack, perform the operation, and push the result back
        elif char in "+-*/":
            op2 = float(stack.pop())
            op1 = float(stack.pop())
            result = eval(f"{op1} {char} {op2}")
            stack.append(result)
        # If the character is a left parenthesis, push it to the stack
        elif char == "(":
            stack.append(char)
        # If the character is a right parenthesis, pop the top operand from the stack and discard it
        elif char == ")":
            stack.pop()

    # Return the final result
    return float(stack.pop())