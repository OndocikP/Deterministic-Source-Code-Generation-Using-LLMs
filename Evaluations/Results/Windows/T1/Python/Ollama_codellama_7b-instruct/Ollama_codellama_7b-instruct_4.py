def calculate(expression):
    # Remove whitespace from the expression
    expression = expression.replace(" ", "")

    # Evaluate the expression using the Shunting Yard algorithm
    output = []
    operator_stack = []
    for token in expression:
        if token.isdigit():
            output.append(token)
        elif token == "(":
            operator_stack.append(token)
        elif token == ")":
            while operator_stack and operator_stack[-1] != "(":
                output.append(operator_stack.pop())
            if operator_stack and operator_stack[-1] == "(":
                operator_stack.pop()
        else:
            while operator_stack and precedence(token) <= precedence(operator_stack[-1]):
                output.append(operator_stack.pop())
            operator_stack.append(token)

    # Evaluate the remaining operators in the stack
    while operator_stack:
        output.append(operator_stack.pop())

    # Convert the output to a float
    result = float(output[0])
    for i in range(1, len(output)):
        result = eval_operator(output[i], result)

    return result

def precedence(operator):
    if operator == "+":
        return 2
    elif operator == "-":
        return 2
    elif operator == "*":
        return 3
    elif operator == "/":
        return 3
    else:
        raise ValueError(f"Invalid operator: {operator}")

def eval_operator(operator, operand1, operand2=None):
    if operator == "+":
        return operand1 + operand2
    elif operator == "-":
        return operand1 - operand2
    elif operator == "*":
        return operand1 * operand2
    elif operator == "/":
        return operand1 / operand2
    else:
        raise ValueError(f"Invalid operator: {operator}")