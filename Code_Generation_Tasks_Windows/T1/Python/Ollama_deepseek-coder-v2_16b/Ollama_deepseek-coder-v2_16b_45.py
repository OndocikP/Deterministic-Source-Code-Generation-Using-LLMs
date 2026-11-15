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
            inner_expr = expr[1:close_idx]
            expr = expr[:expr.index('(')] + str(parse_expression(inner_expr)) + expr[close_idx+1:]
        
        values = []
        operators = []
        i = 0
        while i < len(expr):
            if expr[i].isdigit() or expr[i] == '.':
                j = i
                while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                    j += 1
                values.append(float(expr[i:j]))
                i = j
            elif expr[i] in '+-':
                while operators and operators[-1] in '+-':
                    op = operators.pop()
                    val2 = values.pop()
                    val1 = values.pop()
                    if op == '+':
                        values.append(val1 + val2)
                    elif op == '-':
                        values.append(val1 - val2)
                operators.append(expr[i])
                i += 1
            elif expr[i] in '*/':
                while operators and operators[-1] in '*/':
                    op = operators.pop()
                    val2 = values.pop()
                    val1 = values.pop()
                    if op == '*':
                        values.append(val1 * val2)
                    elif op == '/':
                        if val2 == 0:
                            raise ValueError("Division by zero")
                        values.append(val1 / val2)
                operators.append(expr[i])
                i += 1
            else:
                i += 1
        
        while operators:
            op = operators.pop()
            val2 = values.pop()
            val1 = values.pop()
            if op == '+':
                values.append(val1 + val2)
            elif op == '-':
                values.append(val1 - val2)
            elif op == '*':
                values.append(val1 * val2)
            elif op == '/':
                if val2 == 0:
                    raise ValueError("Division by zero")
                values.append(val1 / val2)
        
        return values[0]
    
    return parse_expression(expression)

# Example usage:
# print(calcute("2 + 3 * 4"))  # Output: 14.0
# print(calcute("2 * (1 + 3) / 4"))  # Output: 2.0