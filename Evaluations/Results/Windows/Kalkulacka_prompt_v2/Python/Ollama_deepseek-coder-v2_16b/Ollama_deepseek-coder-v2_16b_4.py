import re

def calculate(expression: str) -> float:
    def parse_expression(expression):
        expression = expression.replace(' ', '')
        tokens = re.findall(r'\d+\.\d+|\d+|[+\-*/()]', expression)
        return tokens

    def parse_term(tokens, index):
        left = parse_factor(tokens, index)
        while index < len(tokens) and tokens[index] in ['*', '/']:
            op = tokens[index]
            index += 1
            right = parse_factor(tokens, index)
            if op == '*':
                left *= right
            else:
                left /= right
        return left, index

    def parse_factor(tokens, index):
        if tokens[index].isdigit() or '.' in tokens[index]:
            return float(tokens[index])
        elif tokens[index] == '(':
            index += 1
            value, index = parse_expression(tokens[index:])
            if tokens[index] == ')':
                index += 1
            return value
        elif tokens[index] == '-':
            index += 1
            return -parse_factor(tokens, index)
        elif tokens[index] == '+':
            index += 1
            return parse_factor(tokens, index)
        else:
            raise ValueError("Invalid token: " + tokens[index])

    tokens = parse_expression(expression)
    result, _ = parse_term(tokens, 0)
    return result

# Test cases
print(calculate("18-9"))  # 9
print(calculate("2*4"))  # 8
print(calculate("3*5"))  # 15
print(calculate("6*7"))  # 42
print(calculate("8*8"))  # 64
print(calculate("9*4"))  # 36
print(calculate("9/3"))  # 3
print(calculate("12/4"))  # 3
print(calculate("20/5"))  # 4
print(calculate("36/6"))  # 6
print(calculate("10-2*3"))  # 4
print(calculate("20-4*2"))  # 12
print(calculate("2*3+4"))  # 10
print(calculate("5*4-6"))  # 14
print(calculate("18/3+2"))  # 8
print(calculate("20/5+7"))  # 11
print(calculate("16-12/4"))  # 13
print(calculate("2+12/3"))  # 6
print(calculate("30-20/5"))  # 26
print(calculate("4*5+3"))  # 23
print(calculate("7+8/2"))  # 11
print(calculate("6*6-10"))  # 26
print(calculate("3+4*2-5"))  # 6
print(calculate("30-4*5+6"))  # 16
print(calculate("(1+2)*3"))  # 9
print(calculate("(2+3)*(4+1)"))  # 25
print(calculate("(8-2)*(6-3)"))  # 18
print(calculate("(10+5)/(2+3)"))  # 3
print(calculate("(12-4)/(2+2)"))  # 2
print(calculate("(3+5)*(7-4)"))  # 24
print(calculate("(20-8)/(2*3)"))  # 2
print(calculate("(4+6)/(8-6)"))  # 5
print(calculate("(9-3)*(2+4)"))  # 36
print(calculate("(5+7)/(2+1)"))  # 4
print(calculate("(18-6)/(2+4)"))  # 2
print(calculate("(2+3)*4/(6-1)"))  # 4
print(calculate("1/8"))  # 0.125
print(calculate("5/2"))  # 2.5
print(calculate("1/4"))  # 0.25
print(calculate("7/4"))  # 1.75
print(calculate("2/8"))  # 0.25
print(calculate("5/8"))  # 0.625
print(calculate("3/8"))  # 0.375
print(calculate("9/4"))  # 2.25
print(calculate("1/20"))  # 0.05
print(calculate("3/20"))  # 0.15
print(calculate("7/20"))  # 0.35