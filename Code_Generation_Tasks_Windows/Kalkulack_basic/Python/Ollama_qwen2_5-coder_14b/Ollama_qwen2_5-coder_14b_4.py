def calcute(expression):
    def apply_operator(operators, values):
        operator = operators.pop()
        right = values.pop()
        left = values.pop()
        if operator == '+':
            values.append(left + right)
        elif operator == '-':
            values.append(left - right)
        elif operator == '*':
            values.append(left * right)
        elif operator == '/':
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            values.append(left / right)

    def greater_precedence(op1, op2):
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        return precedence[op1] > precedence[op2]

    def parse_expression(expression):
        tokens = []
        i = 0
        while i < len(expression):
            if expression[i].isdigit() or expression[i] == '.':
                j = i
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                tokens.append(float(expression[i:j]))
                i = j
            elif expression[i] in "+-*/()":
                tokens.append(expression[i])
                i += 1
            else:
                i += 1
        return tokens

    def evaluate(tokens):
        values = []
        operators = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if isinstance(token, float):
                values.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    apply_operator(operators, values)
                operators.pop()  # pop '('
            else:
                while (operators and operators[-1] != '(' and
                       greater_precedence(operators[-1], token)):
                    apply_operator(operators, values)
                operators.append(token)
            i += 1

        while operators:
            apply_operator(operators, values)

        return values[0]

    expression = expression.replace(" ", "")
    tokens = parse_expression(expression)
    return evaluate(tokens)