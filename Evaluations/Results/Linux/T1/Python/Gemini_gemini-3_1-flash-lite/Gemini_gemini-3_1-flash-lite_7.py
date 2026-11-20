import re

def calculate(expression):
    expression = expression.replace(" ", "")
    tokens = re.findall(r'\d+\.\d+|\d+|[+\-*/()]', expression)
    
    def precedence(op):
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
            operators.pop()
        else:
            while operators and precedence(operators[-1]) >= precedence(token):
                apply_op(operators, values)
            operators.append(token)
        i += 1
    
    while operators:
        apply_op(operators, values)
        
    return float(values[0])