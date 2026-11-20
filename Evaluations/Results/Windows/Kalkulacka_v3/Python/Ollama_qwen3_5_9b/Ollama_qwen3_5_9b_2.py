def calculate(expression: str) -> float:
    import re
    
    def tokenize(expr):
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
            start = i
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                i += 1
            num_str = expr[start:i]
            if num_str:
                tokens.append(float(num_str))
            else:
                raise ValueError(f"Invalid character at position {i}: {expr[i]}")
        return tokens

    class Parser:
        def __init__(self, tokens):
            self.tokens = tokens
            self.pos = 0
        
        def peek(self):
            if self.pos < len(self.tokens):
                return self.tokens[self.pos]
            return None
        
        def consume(self):
            token = self.peek()
            self.pos += 1
            return token
        
        def parse(self):
            result = self.parse_additive()
            if self.pos < len(self.tokens):
                raise ValueError(f"Unexpected token: {self.peek()}")
            return result
        
        def parse_additive(self):
            left = self.parse_multiplicative()
            while True:
                op = self.peek()
                if op == '+':
                    self.consume()
                    right = self.parse_multiplicative()
                    left += right
                elif op == '-':
                    self.consume()
                    right = self.parse_multiplicative()
                    left -= right
                else:
                    break
            return left
        
        def parse_multiplicative(self):
            left = self.parse_unary()
            while True:
                op = self.peek()
                if op == '*':
                    self.consume()
                    right = self.parse_unary()
                    left *= right
                elif op == '/':
                    self.consume()
                    right = self.parse_unary()
                    if right == 0:
                        raise ZeroDivisionError("division by zero")
                    left /= right
                else:
                    break
            return left
        
        def parse_unary(self):
            token = self.peek()
            if token == '+':
                self.consume()
                return self.parse_unary()
            elif token == '-':
                self.consume()
                value = self.parse_unary()
                return -value
            else:
                return self.parse_primary()
        
        def parse_primary(self):
            token = self.peek()
            if isinstance(token, float):
                self.consume()
                return token
            elif token == '(':
                self.consume()
                value = self.parse_additive()
                if self.peek() != ')':
                    raise ValueError(f"Expected ')' but got {self.peek()}")
                self.consume()
                return value
            else:
                raise ValueError(f"Unexpected token: {token}")

    tokens = tokenize(expression)
    parser = Parser(tokens)
    result = parser.parse()
    return result