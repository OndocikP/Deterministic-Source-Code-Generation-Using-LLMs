def evaluate_expression(expression: str) -> float:
    def tokenize(expr):
        tokens = []
        i = 0
        while i < len(expr):
            if expr[i].isspace():
                i += 1
            elif expr[i] in '+-*/()':
                tokens.append(expr[i])
                i += 1
            elif expr[i].isdigit() or expr[i] == '.':
                j = i
                while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                    j += 1
                tokens.append(expr[i:j])
                i = j
            else:
                i += 1
        return tokens

    def parse_number(token):
        if '.' in token:
            return float(token)
        return int(token)

    def apply_operator(operand_stack, operator_stack):
        if not operand_stack:
            return
        op2 = operand_stack.pop()
        op1 = operand_stack.pop()
        op = operator_stack.pop()
        if op == '+':
            operand_stack.append(op1 + op2)
        elif op == '-':
            operand_stack.append(op1 - op2)
        elif op == '*':
            operand_stack.append(op1 * op2)
        elif op == '/':
            operand_stack.append(op1 / op2)

    tokens = tokenize(expression)
    operand_stack = []
    operator_stack = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '(':
            operator_stack.append(token)
            i += 1
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                apply_operator(operand_stack, operator_stack)
            if operator_stack and operator_stack[-1] == '(':
                operator_stack.pop()
            i += 1
        elif token in '+-*/':
            while operator_stack and operator_stack[-1] != '(' and precedence(token) <= precedence(operator_stack[-1]):
                apply_operator(operand_stack, operator_stack)
            operator_stack.append(token)
            i += 1
        else:
            operand_stack.append(parse_number(token))
            i += 1
    while operator_stack:
        apply_operator(operand_stack, operator_stack)
    return operand_stack[0]

def precedence(op):
    if op in '+-':
        return 1
    elif op in '*/':
        return 2
    return 0