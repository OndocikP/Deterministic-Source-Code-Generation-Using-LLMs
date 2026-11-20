import re

def calculate(expression: str) -> float:
    tokens = re.findall(r'\d+\.?\d*|\+|\-|\*|\/|\(|\)', expression)
    pos = 0

    def parse_expression():
        nonlocal pos
        node = parse_term()
        while pos < len(tokens) and tokens[pos] in ('+', '-'):
            op = tokens[pos]
            pos += 1
            right = parse_term()
            if op == '+':
                node += right
            else:
                node -= right
        return node

    def parse_term():
        nonlocal pos
        node = parse_factor()
        while pos < len(tokens) and tokens[pos] in ('*', '/'):
            op = tokens[pos]
            pos += 1
            right = parse_factor()
            if op == '*':
                node *= right
            else:
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                node /= right
        return node

    def parse_factor():
        nonlocal pos
        token = tokens[pos]
        if token == '(':
            pos += 1
            node = parse_expression()
            if pos >= len(tokens) or tokens[pos] != ')':
                raise ValueError("Mismatched parentheses")
            pos += 1
            return node
        elif token == '-':
            pos += 1
            return -parse_factor()
        elif token == '+':
            pos += 1
            return parse_factor()
        else:
            pos += 1
            return float(token)

    result = parse_expression()
    if pos != len(tokens):
        raise ValueError("Invalid expression")
    return float(result)