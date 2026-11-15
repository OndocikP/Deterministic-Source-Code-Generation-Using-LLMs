import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.tokens = []

    def tokenize(self):
        while self.pos < len(self.text):
            char = self.text[self.pos]

            if char.isspace():
                self.pos += 1
                continue

            if char.isdigit() or char == '.':
                self.tokens.append(self._number())
                continue

            if char in '+-*/()':
                self.tokens.append(self._operator_or_paren(char))
                self.pos += 1
                continue

            raise ValueError(f"Lexer error: Unexpected character '{char}' at position {self.pos}")

    def _number(self):
        start = self.pos
        while self.pos < len(self.text) and (self.text[self.pos].isdigit() or self.text[self.pos] == '.'):
            self.pos += 1
        value_str = self.text[start:self.pos]
        try:
            return Token('NUMBER', float(value_str))
        except ValueError:
            raise ValueError(f"Lexer error: Invalid number format '{value_str}'")

    def _operator_or_paren(self, char):
        if char in '+-*/()':
            return Token(char, char)
        raise ValueError("Should not happen")

def tokenize_expression(expression: str) -> list[Token]:
    lexer = Lexer(expression)
    return lexer.tokenize()

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected_type=None, expected_value=None):
        token = self.peek()
        if token is None:
            raise SyntaxError("Unexpected end of expression")
        if expected_type and token.type != expected_type:
            raise SyntaxError(f"Expected token type {expected_type}, got {token.type}")
        if expected_value and token.value != expected_value:
            raise SyntaxError(f"Expected token value '{expected_value}', got '{token.value}'")
        self.pos += 1
        return token

    def parse(self):
        result = self._expression()
        if self.pos != len(self.tokens):
            raise SyntaxError("Extra tokens found after expression completion")
        return result

    # Grammar implementation based on precedence:
    # expression -> term { ('+' | '-') term }
    def _expression(self):
        node = self._term()
        while self.peek() and self.peek().type in ('+', '-'):
            op_token = self.consume()
            right = self._term()
            node = BinaryOp(node, op_token.value, right)
        return node

    # term -> factor { ('*' | '/') factor }
    def _term(self):
        node = self._factor()
        while self.peek() and self.peek().type in ('*', '/'):
            op_token = self.consume()
            right = self._factor()
            node = BinaryOp(node, op_token.value, right)
        return node

    # factor -> NUMBER | '(' expression ')' | '-' factor | '+' factor
    def _factor(self):
        token = self.peek()
        if token is None:
            raise SyntaxError("Unexpected end of expression while expecting factor")

        if token.type == 'NUMBER':
            self.consume()
            return Literal(token.value)
        elif token.value == '(':
            self.consume('(')
            node = self._expression()
            self.consume(')')
            return node
        elif token.value in ('+', '-'):
            op_token = self.consume()
            # Handle unary plus/minus
            right = self._factor()
            if op_token.value == '-':
                return UnaryOp(op_token.value, right)
            elif op_token.value == '+':
                return right # Unary plus is identity
            else:
                # This case should not be reached if logic is correct, but for safety:
                raise SyntaxError("Invalid unary operator")
        else:
            raise SyntaxError(f"Unexpected token in factor: {token}")

class Literal:
    def __init__(self, value):
        self.value = value
    def evaluate(self):
        return self.value

class BinaryOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def evaluate(self):
        left_val = self.left.evaluate()
        right_val = self.right.evaluate()