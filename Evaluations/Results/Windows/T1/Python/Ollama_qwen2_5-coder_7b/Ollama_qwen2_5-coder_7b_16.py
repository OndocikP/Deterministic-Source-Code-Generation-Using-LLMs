import re

def calculate(expression):
    def apply_operator(operators, values):
        operator = operators.pop()
        right = values.pop()
        left = values.pop()
        if operator == '+':
            values.append(left + right)
        elif operator == '-':
            values.append(left - right)
        elif operator == '*':
            values.append(left * right)
        elif operator == '/':
            if right == 0:
                raise ValueError("Division by zero")
            values.append(left / right)

    def greater_precedence(op1, op2):
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        return precedence[op1] > precedence[op2]

    expression = expression.replace(' ', '')
    tokens = re.findall(r'\d+\.\d+|\d+|\+|\-|\*|\/|\(|\)', expression)
    operators = []
    values = []
    i = 0

    while i < len(tokens):
        token = tokens[i]
        if token.isdigit() or '.' in token:
            values.append(float(token))
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                apply_operator(operators, values)
            operators.pop()
        else:
            while (operators and operators[-1] != '(' and
                   greater_precedence(operators[-1], token)):
                apply_operator(operators, values)
            operators.append(token)
        i += 1

    while operators:
        apply_operator(operators, values)

    return values[0]