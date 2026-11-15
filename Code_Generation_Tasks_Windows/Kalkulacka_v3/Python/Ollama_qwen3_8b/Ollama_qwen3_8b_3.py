def calculate(expression: str) -> float:
    expression = expression.replace(' ', '')
    tokens = tokenize(expression)
    return evaluate(tokens)

def tokenize(expression):
    tokens = []
    i = 0
    while i < len(expression):
        if expression[i].isdigit() or expression[i] == '.':
            num = ''
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                num += expression[i]
                i += 1
            tokens.append(('NUMBER', float(num)))
        elif expression[i] in '+-*/()':
            tokens.append(('OPERATOR', expression[i]))
            i += 1
        else:
            i += 1
    return tokens

def evaluate(tokens):
    stack = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token[0] == 'NUMBER':
            stack.append(token[1])
            i += 1
        elif token[1] == '(':
            stack.append('(')
            i += 1
        elif token[1] == ')':
            sub_expr = []
            while stack and stack[-1] != '(':
                sub_expr.append(stack.pop())
            if not stack or stack[-1] != '(':
                raise ValueError("Mismatched parentheses")
            stack.pop()  # Remove '('
            sub_expr.reverse()
            try:
                result = evaluate(sub_expr)
                stack.append(result)
            except Exception as e:
                raise e
            i += 1
        else:
            if not stack or stack[-1] == '(':
                stack.append(token[1])
            else:
                if token[1] in '*/':
                    right = stack.pop()
                    left = stack.pop()
                    if token[1] == '*':
                        stack.append(left * right)
                    else:
                        if right == 0:
                            raise ZeroDivisionError("Division by zero")
                        stack.append(left / right)
            i += 1
    while len(stack) > 1:
        right = stack.pop()
        left = stack.pop()
        if stack[-1] == '+':
            stack.append(left + right)
        elif stack[-1] == '-':
            stack.append(left - right)
    if not stack:
        raise ValueError("Invalid expression")
    return stack[0]