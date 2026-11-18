import re
from typing import Union

class Calculator:
    def __init__(self):
        self.operators = {'+': self.add, '-': self.subtract, '*': self.multiply, '/': self.divide}
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

    def calculate(self, expression: str) -> float:
        expression = re.sub(r'\s+', '', expression)
        return self.evaluate(expression)

    def evaluate(self, expression: str) -> float:
        tokens = self.tokenize(expression)
        return self.parse(tokens)

    def tokenize(self, expression: str) -> list:
        tokens = []
        i = 0
        while i < len(expression):
            if expression[i] in self.operators:
                tokens.append(expression[i])
                i += 1
            elif expression[i] == '(':
                j = self.find_matching_parenthesis(expression, i)
                tokens.append(self.evaluate(expression[i+1:j]))
                i = j + 1
            else:
                j = i
                while j < len(expression) and expression[j].isdigit() or expression[j] == '.':
                    j += 1
                tokens.append(float(expression[i:j]))
                i = j
        return tokens

    def find_matching_parenthesis(self, expression: str, start: int) -> int:
        count = 1
        i = start + 1
        while count > 0:
            if expression[i] == '(':
                count += 1
            elif expression[i] == ')':
                count -= 1
            i += 1
        return i - 1

    def parse(self, tokens: list) -> float:
        values = []
        ops = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if isinstance(token, float):
                values.append(token)
            elif token in self.operators:
                while ops and self.precedence[ops[-1]] >= self.precedence[token]:
                    values.append(self.operators[ops.pop()](values.pop(), values.pop()))
                ops.append(token)
            i += 1
        while ops:
            values.append(self.operators[ops.pop()](values.pop(), values.pop()))
        return values[0]

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero")
        return a / b

# Example usage:
calc = Calculator()
print(calc.calculate("18-9"))  # Output: 9.0
print(calc.calculate("2*4"))   # Output: 8.0
print(calc.calculate("(1+2)*3"))  # Output: 9.0