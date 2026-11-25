def evaluate_expression(expression: str) -> float:
    def precedence(op):
        if op in ('+', '-'):
            return 1
        if op in ('*', '/'):
            return 2
        return 0

    def apply_operator(operators, values):
        right = values.pop()
        left = values.pop()
        op = operators.pop()
        if op == '+':
            values.append(left + right)
        elif op == '-':
            values.append(left - right)
        elif op == '*':
            values.append(left * right)
        elif op == '/':
            values.append(left / right)

    def greater_precedence(op1, op2):
        return precedence(op1) > precedence(op2)

    operators = []
    values = []
    i = 0
    while i < len(expression):
        if expression[i] == ' ':
            i += 1
            continue
        if expression[i].isdigit() or (expression[i] == '.' and i + 1 < len(expression) and expression[i + 1].isdigit()):
            val = 0
            decimal = False
            decimal_factor = 0.1
            while i < len(expression) and (expression[i].isdigit() or (expression[i] == '.' and not decimal)):
                if expression[i] == '.':
                    decimal = True
                else:
                    if decimal:
                        val += int(expression[i]) * decimal_factor
                        decimal_factor *= 0.1
                    else:
                        val = val * 10 + int(expression[i])
                i += 1
            values.append(val)
            continue
        if expression[i] == '(':
            operators.append(expression[i])
        elif expression[i] == ')':
            while operators and operators[-1] != '(':
                apply_operator(operators, values)
            operators.pop()  # pop '('
        elif expression[i] in "+-*/":
            while (operators and operators[-1] != '(' and
                   greater_precedence(operators[-1], expression[i])):
                apply_operator(operators, values)
            operators.append(expression[i])
        elif expression[i] == '-':
            if i == 0 or expression[i - 1] in "+-*/(":
                values.append(0)
                operators.append('-')
        i += 1

    while operators:
        apply_operator(operators, values)

    return values[0]