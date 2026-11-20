import re

def calcute(expression):
    def parse_expression(expr):
        expr = expr.replace(' ', '')
        while '(' in expr:
            inner_expr = ''
            close_idx = len(expr)
            open_count = 0
            for i, char in enumerate(expr):
                if char == '(':
                    open_count += 1
                elif char == ')':
                    open_count -= 1
                    if open_count == 0:
                        close_idx = i
                        break
            inner_expr = expr[expr.find('(') + 1:close_idx]
            expr = expr.replace(f'({inner_expr})', str(parse_expression(inner_expr)))
        tokens = re.findall(r'\d+\.\d+|\d+|[+\-*/]', expr)
        stack = []
        for token in tokens:
            if token.isdigit() or '.' in token:
                stack.append(float(token))
            elif token == '+':
                stack.append(stack.pop() + stack.pop())
            elif token == '-':
                stack.append(-(stack.pop() - stack.pop()))
            elif token == '*':
                stack.append(stack.pop() * stack.pop())
            elif token == '/':
                b = stack.pop()
                a = stack.pop()
                if b == 0:
                    raise ValueError("Division by zero")
                stack.append(a / b)
        return stack[0]
    
    try:
        return parse_expression(expression)
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")

# Example usage:
# print(calcute("2 + 3 * 4"))  # Output: 14.0
# print(calcute("2 * (1 + 3) / 4"))  # Output: 2.0