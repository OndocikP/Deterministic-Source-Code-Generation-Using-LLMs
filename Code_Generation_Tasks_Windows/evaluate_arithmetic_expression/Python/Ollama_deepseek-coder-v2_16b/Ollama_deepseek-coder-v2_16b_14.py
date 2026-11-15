def evaluate_expression(expression: str) -> float:
    def precedence(op):
        if op == '+' or op == '-':
            return 1
        elif op == '*' or op == '/':
            return 2
        return 0

    def apply_op(vals, ops):
        op = ops.pop()
        val2 = vals.pop()
        val1 = vals.pop()
        if op == '+':
            vals.append(val1 + val2)
        elif op == '-':
            vals.append(val1 - val2)
        elif op == '*':
            vals.append(val1 * val2)
        elif op == '/':
            vals.append(val1 / val2)

    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    vals = []
    ops = []
    i = 0
    while i < len(expression):
        if expression[i] == ' ':
            i += 1
            continue
        if is_number(expression[i]):
            num = 0
            while i < len(expression) and (expression[i] == '.' or expression[i].isdigit()):
                if expression[i] == '.':
                    num = num * 10 + float(expression[i])
                else:
                    num = num * 10 + int(expression[i])
                i += 1
            vals.append(num)
            i -= 1
        elif expression[i] == '(':
            ops.append(expression[i])
        elif expression[i] == ')':
            while len(ops) > 0 and ops[-1] != '(':
                apply_op(vals, ops)
            ops.pop()
        elif expression[i] == '+' or expression[i] == '-' or expression[i] == '*' or expression[i] == '/':
            while len(ops) > 0 and precedence(ops[-1]) >= precedence(expression[i]):
                apply_op(vals, ops)
            ops.append(expression[i])
        i += 1

    while len(ops) > 0:
        apply_op(vals, ops)

    return vals[0]