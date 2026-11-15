def evaluate_expression(expression: str) -> float:
    def get_precedence(op):
        if op in ('+', '-'): return 1
        if op in ('*', '/'): return 2
        return 0

    def apply_op(ops, values):
        op = ops.pop()
        right = values.pop()
        left = values.pop() if values else 0.0
        if op == '+': values.append(left + right)
        elif op == '-': values.append(left - right)
        elif op == '*': values.append(left * right)
        elif op == '/': values.append(left / right)

    ops = []
    values = []
    i = 0
    expect_unary = True
    
    while i < len(expression):
        char = expression[i]
        if char.isspace():
            i += 1
            continue
        
        if char == '(':
            ops.append('(')
            expect_unary = True
            i += 1
        elif char == ')':
            while ops and ops[-1] != '(':
                apply_op(ops, values)
            ops.pop()
            expect_unary = False
            i += 1
        elif char in "+-*/":
            if expect_unary and char == '-':
                values.append(0.0)
            while ops and ops[-1] != '(' and get_precedence(ops[-1]) >= get_precedence(char):
                apply_op(ops, values)
            ops.append(char)
            expect_unary = True
            i += 1
        else:
            j = i
            while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                j += 1
            values.append(float(expression[i:j]))
            i = j
            expect_unary = False
            
    while ops:
        apply_op(ops, values)
        
    return float(values[0])