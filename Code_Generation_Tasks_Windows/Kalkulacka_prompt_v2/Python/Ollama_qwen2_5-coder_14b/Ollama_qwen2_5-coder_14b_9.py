def calculate(expression: str) -> float:
    def parse_expression(tokens):
        def parse_term():
            result = parse_factor()
            while tokens and tokens[0] in ('*', '/'):
                op = tokens.pop(0)
                if op == '*':
                    result *= parse_factor()
                elif op == '/':
                    result /= parse_factor()
            return result

        def parse_factor():
            if tokens[0] == '(':
                tokens.pop(0)
                result = parse_expression(tokens)
                tokens.pop(0)  # consume ')'
                return result
            else:
                return float(tokens.pop(0))

        result = parse_term()
        while tokens and tokens[0] in ('+', '-'):
            op = tokens.pop(0)
            if op == '+':
                result += parse_term()
            elif op == '-':
                result -= parse_term()
        return result

    def tokenize(expression):
        import re
        return re.findall(r'\d+\.\d+|\d+|[()+\-*/]', expression.replace(' ', ''))

    tokens = tokenize(expression)
    return parse_expression(tokens)