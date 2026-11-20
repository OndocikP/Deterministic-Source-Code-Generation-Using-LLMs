def calculate(string):
    def parse_expression(s):
        s = s.replace(' ', '')
        tokens = []
        i = 0
        while i < len(s):
            if s[i] in '+-*/()':
                tokens.append(s[i])
                i += 1
            elif s[i].isdigit() or s[i] == '.':
                j = i
                while j < len(s) and (s[j].isdigit() or s[j] == '.'):
                    j += 1
                tokens.append(s[i:j])
                i = j
            else:
                raise ValueError("Invalid character in expression")
        return tokens

    def evaluate(tokens):
        def parse_number(token):
            if '.' in token:
                return float(token)
            else:
                return int(token)

        def parse_factor(tokens):
            if tokens[0] == '(':
                tokens.pop(0)
                result = parse_expression(tokens)
                if tokens and tokens[0] == ')':
                    tokens.pop(0)
                return result
            else:
                return parse_number(tokens.pop(0))

        def parse_term(tokens):
            left = parse_factor(tokens)
            while tokens and tokens[0] in '*/':
                op = tokens.pop(0)
                right = parse_factor(tokens)
                if op == '*':
                    left *= right
                elif op == '/':
                    if right == 0:
                        raise ZeroDivisionError("Division by zero")
                    left /= right
            return left

        def parse_expression(tokens):
            left = parse_term(tokens)
            while tokens and tokens[0] in '+-':
                op = tokens.pop(0)
                right = parse_term(tokens)
                if op == '+':
                    left += right
                elif op == '-':
                    left -= right
            return left

        tokens = parse_expression(tokens)
        return tokens

    try:
        tokens = parse_expression(string)
        result = evaluate(tokens)
        return float(result)
    except ZeroDivisionError as e:
        raise e
    except Exception as e:
        raise ValueError("Invalid expression") from e