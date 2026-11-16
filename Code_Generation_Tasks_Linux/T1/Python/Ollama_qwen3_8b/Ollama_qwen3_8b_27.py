def calculate(string):
    def parse_number(s):
        if '.' in s:
            return float(s)
        return int(s)

    def tokenize(s):
        s = s.replace(' ', '')
        tokens = []
        i = 0
        while i < len(s):
            if s[i].isdigit() or s[i] == '.':
                j = i
                while j < len(s) and (s[j].isdigit() or s[j] == '.'):
                    j += 1
                tokens.append(('NUMBER', parse_number(s[i:j])))
                i = j
            elif s[i] in '+-*/()':
                tokens.append(('OPERATOR', s[i]))
                i += 1
            else:
                raise ValueError("Invalid character in expression")
        return tokens

    def parse_expression(tokens):
        def parse_term(tokens):
            left = parse_factor(tokens)
            while tokens and tokens[0][0] == 'OPERATOR' and tokens[0][1] in '*/':
                op, token = tokens.pop(0)
                right = parse_factor(tokens)
                if op == '*':
                    left = left * right
                elif op == '/':
                    if right == 0:
                        raise ZeroDivisionError("Division by zero")
                    left = left / right
            return left

        def parse_factor(tokens):
            if tokens[0][0] == 'NUMBER':
                return tokens.pop(0)[1]
            elif tokens[0][0] == 'OPERATOR' and tokens[0][1] == '(':
                tokens.pop(0)
                result = parse_expression(tokens)
                if tokens and tokens[0][0] == 'OPERATOR' and tokens[0][1] == ')':
                    tokens.pop(0)
                return result
            else:
                raise ValueError("Invalid expression")

        return parse_term(tokens)

    tokens = tokenize(string)
    result = parse_expression(tokens)
    if tokens:
        raise ValueError("Incomplete expression")
    return float(result)