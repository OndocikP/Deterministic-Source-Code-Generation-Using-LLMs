import re

def calculate(expression):
    tokens = re.findall(r'\d+\.\d+|\d+|[+\-*/()]', expression.replace(" ", ""))
    
    def get_precedence(op):
        if op in ('+', '-'): return 1
        if op in ('*', '/'): return 2
        return 0

    def apply_op(operators, values):
        op = operators.pop()
        right = values.pop()
        left = values.pop()
        if op == '+': values.append(left + right)
        elif op == '-': values.append(left - right)
        elif op == '*': values.append(left * right)
        elif op == '/':
            if right == 0: raise ZeroDivisionError("Division by zero")
            values.append(left / right)

    values = []
    operators = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.replace('.', '', 1).isdigit():
            values.append(float(token))
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                apply_op(operators, values)
            if not operators: raise ValueError("Invalid expression")
            operators.pop()
        else:
            while operators and get_precedence(operators[-1]) >= get_precedence(token):
                apply_op(operators, values)
            operators.append(token)
        i += 1
    
    while operators:
        if operators[-1] == '(': raise ValueError("Invalid expression")
        apply_op(operators, values)
        
    if len(values) != 1: raise ValueError("Invalid expression")
    return float(values[0])