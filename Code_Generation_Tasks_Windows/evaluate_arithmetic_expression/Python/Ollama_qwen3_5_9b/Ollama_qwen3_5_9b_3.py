def evaluate_expression(expression: str) -> float:
    def tokenize(expr: str):
        tokens = []
        i = 0
        while i < len(expr):
            if expr[i].isspace():
                i += 1
                continue
            if expr[i] in '+-*/()':
                tokens.append(expr[i])
                i += 1
                continue
            if expr[i].isdigit() or expr[i] == '.':
                j = i
                while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                    j += 1
                tokens.append(expr[i:j])
                i = j
                continue
            raise ValueError(f"Invalid character: {expr[i]}")
        return tokens

    def apply_operator(op, left, right):
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            if right == 0:
                raise ZeroDivisionError("division by zero")
            return left / right
        else:
            raise ValueError(f"Unknown operator: {op}")

    def parse(tokens):
        values = []
        operators = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        associativity = {'+': 'left', '-': 'left', '*': 'left', '/': 'left'}

        i = 0
        while i < len(tokens):
            token = tokens[i]

            if isinstance(token, str) and token in '+-*/()':
                if token == '(':
                    operators.append(token)
                elif token == ')':
                    while operators and operators[-1] != '(':
                        op = operators.pop()
                        right = values.pop()
                        left = values.pop()
                        values.append(apply_operator(op, left, right))
                    if not operators or operators[-1] != '(':
                        raise ValueError("Mismatched parentheses")
                    operators.pop()  # Remove '('
                else:
                    while (operators and operators[-1] in precedence and
                           precedence[operators[-1]] >= precedence[token]):
                        op = operators.pop()
                        right = values.pop()
                        left = values.pop()
                        values.append(apply_operator(op, left, right))
                    operators.append(token)
                i += 1
            elif isinstance(token, str):
                # Unary minus: check if previous token is operator or start of expression
                if token == '-':
                    if not operators and not values:
                        # Unary minus at start
                        values.append(0.0)
                        operators.append('-')
                    elif operators and operators[-1] in '+-*/()':
                        # After an operator, treat as unary minus (negation)
                        right = values.pop()
                        values.append(-right)
                        i += 1
                        continue
                    else:
                        raise ValueError("Invalid expression")
                elif token == '+':
                    if not operators and not values:
                        # Unary plus at start (no-op, but we keep it for consistency)
                        pass
                    elif operators and operators[-1] in '+-*/()':
                        # After an operator, treat as unary plus (no-op)
                        i += 1
                        continue
                    else:
                        raise ValueError("Invalid expression")
                else:
                    raise ValueError(f"Unexpected token: {token}")
            elif isinstance(token, str):
                values.append(float(token))
                i += 1
            else:
                raise ValueError(f"Unexpected token type: {type(token)}")

        while operators:
            if operators[-1] == '(':
                raise ValueError("Mismatched parentheses")
            op = operators.pop()
            right = values.pop()
            left = values.pop()
            values.append(apply_operator(op, left, right))

        if len(values) != 1:
            raise ValueError("Invalid expression")

        return values[0]

    tokens = tokenize(expression)
    return parse(tokens)