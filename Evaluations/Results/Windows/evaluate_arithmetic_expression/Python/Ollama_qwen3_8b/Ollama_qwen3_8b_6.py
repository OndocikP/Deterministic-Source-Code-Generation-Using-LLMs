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

    def parse_expression(tokens):
        def parse_term(tokens):
            def parse_factor(tokens):
                if tokens[0] == '(':
                    tokens.pop(0)
                    result = parse_expression(tokens)
                    if tokens[0] != ')':
                        raise ValueError("Mismatched parentheses")
                    tokens.pop(0)
                    return result
                else:
                    num = float(tokens.pop(0))
                    return num

            left = parse_factor(tokens)
            while tokens and tokens[0] in '*/':
                op = tokens.pop(0)
                right = parse_factor(tokens)
                if op == '*':
                    left *= right
                elif op == '/':
                    if right == 0:
                        raise ValueError("Division by zero")
                    left /= right
            return left

        left = parse_term(tokens)
        while tokens and tokens[0] in '+-':
            op = tokens.pop(0)
            right = parse_term(tokens)
            if op == '+':
                left += right
            elif op == '-':
                left -= right
        return left

    tokens = tokenize(expression)
    return parse_expression(tokens)