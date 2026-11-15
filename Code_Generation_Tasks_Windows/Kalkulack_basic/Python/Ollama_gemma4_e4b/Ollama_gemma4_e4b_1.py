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
        if op in ['+', '-']:
            return 1
        if op in ['*', '/']:
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
        elif char in ['+', '-', '*', '/', '(', ')']:
            tokens.append(char)
            i += 1
        else:
            raise ValueError(f"Invalid character in expression: {char}")

    def evaluate_tokens(tokens):
        values = []
        ops = []

        def process_top_operation():
            op = ops.pop()
            val2 = values.pop()
            val1 = values.pop()
            values.append(apply_op(op, val2, val1))

        for token in tokens:
            if isinstance(token, float):
                values.append(token)
            elif token == '(':
                ops.append(token)
            elif token == ')':
                while ops[-1] != '(':
                    process_top_operation()
                ops.pop()  # Pop '('
            else:
                op = token
                while (ops and ops[-1] != '(' and precedence(ops[-1]) >= precedence(op)):
                    process_top_operation()
                ops.append(op)

        while ops:
            process_top_operation()

        if len(values) != 1:
            raise ValueError("Invalid expression structure")

        return values[0]

    return evaluate_tokens(tokens)