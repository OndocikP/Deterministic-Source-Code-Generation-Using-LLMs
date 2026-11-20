def calculate(expression):
    # Remove whitespace from the expression
    expression = expression.replace(" ", "")
    
    # Evaluate the expression using the Shunting Yard algorithm
    stack = []
    for token in expression.split(""):
        if token in ["+", "-", "*", "/"]:
            op2 = stack.pop()
            op1 = stack.pop()
            stack.append((op1, op2))
        else:
            stack.append(float(token))
    
    # Evaluate the expression
    result = stack.pop()
    while len(stack) > 0:
        result = stack.pop()
    
    return result