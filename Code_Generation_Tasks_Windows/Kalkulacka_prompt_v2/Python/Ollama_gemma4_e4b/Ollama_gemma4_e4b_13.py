import re

def calculate(expression: str) -> float:
    def tokenize(expression: str):
        tokens = []
        # Regex to capture numbers (including decimals), operators, parentheses, and potential unary signs
        # We treat unary signs as part of the number token initially, or handle them during parsing.
        # For simplicity and robustness against complex unary cases, we'll use a state-machine/regex approach
        # that tokenizes numbers, operators, and parentheses first.
        
        # Pattern breakdown:
        # \s* : Skip whitespace
        # (?:[0-9]*\.[0-9]+|[0-9]+) : Matches numbers (e.g., 12, 3.14)
        # | : OR
        # ([\+\-\*/\(\)]) : Matches single characters: +, -, *, /, (, )
        
        token_specification = [
            ('NUMBER', r'\d+(\.\d*)?'),
            ('OP', r'[\+\-\*/\(\)]'),
            ('SKIP', r'\s+'),
        ]
        
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        
        tokens = []
        for mo in re.finditer(tok_regex, expression):
            kind = mo.lastgroup
            value = mo.group(0)
            if kind == 'SKIP':
                continue
            elif kind == 'NUMBER':
                tokens.append(float(value))
            elif kind == 'OP':
                tokens.append(value)
        return tokens

    tokens = tokenize(expression)
    
    # --- Shunting-Yard / Recursive Descent Implementation ---
    
    # Pre-process tokens to handle unary minus/plus
    processed_tokens = []
    is_expecting_operand = True
    
    for i, token in enumerate(tokens):
        if isinstance(token, float):
            processed_tokens.append(token)
            is_expecting_operand = False
        elif token in ('(', '+', '-'):
            if is_expecting_operand:
                # Check for unary sign: If it's the first token, or follows '(', or follows another operator
                if token == '-' or token == '+':
                    # Replace unary sign with a placeholder or adjust the number token logic.
                    # A common technique is to treat unary minus as 0 - X or unary plus as 0 + X.
                    # Since we are parsing tokens sequentially, we'll modify the token stream:
                    if token == '-':
                        processed_tokens.append('UNARY_MINUS')
                    elif token == '+':
                        processed_tokens.append('UNARY_PLUS')
                    is_expecting_operand = True
                    continue
            
            # Binary operator case
            processed_tokens.append(token)
            is_expecting_operand = True
        elif token in ('*', '/', ')'):
            processed_tokens.append(token)
            is_expecting_operand = False
        else:
            # Should not happen if tokenization is correct
            pass

    # Final pass to convert UNARY_MINUS/UNARY_PLUS into actual operations relative to the next number/parenthesis
    final_tokens = []
    i = 0
    while i < len(processed_tokens):
        token = processed_tokens[i]
        if token == 'UNARY_MINUS':
            if i + 1 < len(processed_tokens) and (isinstance(processed_tokens[i+1], float) or processed_tokens[i+1] == '('):
                # Unary minus applied to a number or an expression
                final_tokens.append(token) # Keep it as a marker for the parser
            else:
                # Should not happen in valid input, but treat as binary operator if it does
                final_tokens.append(token)
        elif token == 'UNARY_PLUS':
            if i + 1 < len(processed_tokens) and (isinstance(processed_tokens[i+1], float) or processed_tokens[i+1] == '('):
                # Unary plus is usually redundant, but we keep it for structural consistency if needed.
                final_tokens.append(token)
            else:
                final_tokens.append(token)
        else:
            final_tokens.append(token)
        i += 1

    # --- Recursive Descent Parser ---
    
    tokens_iter = iter(final_tokens)

    def peek():
        try:
            # Peek at the next token without consuming it
            return next(tokens_iter)
        except StopIteration:
            return None

    def consume(expected_type=None):
        try:
            token = next(tokens_iter)
            if expected_type and not isinstance(token, type(expected_type)):
                raise ValueError(f"Expected {expected_type}, but found {token}")
            return token
        except StopIteration:
            raise ValueError("Unexpected end of expression.")

    def parse_primary():
        token = peek()
        if token is None:
            raise ValueError("Unexpected end of expression while expecting primary factor.")

        if isinstance(token, float):
            return consume()
        elif token == '(':
            consume('(')
            result =