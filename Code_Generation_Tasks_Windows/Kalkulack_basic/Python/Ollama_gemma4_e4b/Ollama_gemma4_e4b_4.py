import re

def calcute(string):
    def apply_op(op, b, a):
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            return a / b

    def precedence(op):
        if op in ('+', '-'):
            return 1
        if op in ('*', '/'):
            return 2
        return 0

    tokens = []
    i = 0
    while i < len(string):
        char = string[i]
        if char.isspace():
            i += 1
            continue
        elif char.isdigit() or char == '.':
            j = i
            while j < len(string) and (string[j].isdigit() or string[j] == '.'):
                j += 1
            tokens.append(float(string[i:j]))
            i = j
            continue
        elif char in ('+', '-', '*', '/', '(', ')'):
            tokens.append(char)
            i += 1
        else:
            raise ValueError(f"Invalid character in expression: {char}")

    # Shunting-yard algorithm to convert infix to RPN (Reverse Polish Notation)
    output_queue = []
    operator_stack = []

    for token in tokens:
        if isinstance(token, float):
            output_queue.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            if operator_stack and operator_stack[-1] == '(':
                operator_stack.pop()  # Pop '('
            else:
                raise ValueError("Mismatched parentheses")
        else:  # Operator
            while (operator_stack and operator_stack[-1] != '(' and
                   precedence(operator_stack[-1]) >= precedence(token)):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)

    while operator_stack:
        op = operator_stack.pop()
        if op == '(' or op == ')':
            raise ValueError("Mismatched parentheses")

    # Evaluate RPN
    operand_stack = []
    for token in output_queue:
        if isinstance(token, float):
            operand_stack.append(token)
        else:
            if len(operand_stack) < 2:
                raise ValueError("Invalid expression format")
            b = operand_stack.pop()
            a = operand_stack.pop()
            result = apply_op(token, b, a)
            operand_stack.append(result)

    if len(operand_stack) != 1:
        raise ValueError("Invalid expression format")

    return operand_stack[0]