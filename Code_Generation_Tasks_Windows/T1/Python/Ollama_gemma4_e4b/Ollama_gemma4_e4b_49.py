def calcute(string):
    def tokenize(expression):
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]
            if char.isspace():
                i += 1
                continue
            elif char.isdigit() or char == '.':
                j = i
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                tokens.append(expression[i:j])
                i = j
                continue
            elif char in '+-*/()':
                tokens.append(char)
                i += 1
                continue
            else:
                raise ValueError("Invalid character in expression")
        return tokens

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
        if op in ('+', '-'):
            return 1
        if op in ('*', '/'):
            return 2
        return 0

    tokens = tokenize(string)

    values = []
    ops = []

    for token in tokens:
        if token.replace('.', '', 1).isdigit():
            values.append(float(token))
        elif token == '(':
            ops.append(token)
        elif token == ')':
            while ops[-1] != '(':
                op = ops.pop()
                val2 = values.pop()
                val1 = values.pop()
                values.append(apply_op(op, val2, val1))
            ops.pop()  # Pop '('
        else:
            op = token
            while (len(ops) != 0 and ops[-1] != '(' and
                   precedence(ops[-1]) >= precedence(op)):
                current_op = ops.pop()
                val2 = values.pop()
                val1 = values.pop()
                values.append(apply_op(current_op, val2, val1))
            ops.append(op)

    while len(ops) != 0:
        op = ops.pop()
        val2 = values.pop()
        val1 = values.pop()
        values.append(apply_op(op, val2, val1))

    if len(values) != 1:
        raise ValueError("Invalid expression format")

    return values[0]