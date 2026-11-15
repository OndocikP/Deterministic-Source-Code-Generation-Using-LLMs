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
        # (?:[0-9]+\.[0-9]*|[0-9]+) : Matches numbers (e.g., 12, 12.34)
        # | : OR
        # [+\-*/()] : Matches single operators or parentheses
        
        token_pattern = r"([0-9]+\.[0-9]*|[0-9]+)|([+\-*/()])"
        
        # Find all matches, filtering out None results from the group structure
        raw_tokens = re.findall(token_pattern, expression)
        
        for match in raw_tokens:
            # match is a tuple where one element is non-empty
            token = "".join(match)
            if token:
                tokens.append(token)
        return tokens

    def parse_expression(tokens):
        # This implementation uses the Shunting-Yard algorithm concept implicitly via recursive descent
        # to handle precedence correctly, adapted for direct evaluation.

        # --- Helper Functions for Grammar ---

        def parse_primary(tokens, start_index):
            if start_index >= len(tokens):
                raise ValueError("Unexpected end of expression.")

            token = tokens[start_index]
            
            # Handle numbers
            try:
                if '.' in token or token.isdigit():
                    return float(token), start_index + 1
            except ValueError:
                pass

            # Handle parentheses
            if token == '(':
                # Recursively parse the content inside the parentheses
                result, next_index = parse_expression(tokens, start_index + 1)
                
                # Expect closing parenthesis
                if next_index >= len(tokens) or tokens[next_index] != ')':
                    raise ValueError("Mismatched parentheses: Expected ')'")
                
                return result, next_index + 1

            # Handle unary signs at the start of a factor (e.g., -5, -(2+3))
            # This is the trickiest part. We check if the current token is a sign 
            # and if it's followed by a number or an opening parenthesis.
            if token in ('+', '-') and (start_index + 1 < len(tokens) and (tokens[start_index+1].replace('.', '', 1).isdigit() or tokens[start_index+1] == '(')):
                sign = token
                next_token = tokens[start_index + 1]
                
                if next_token == '(':
                    # Unary minus/plus before a parenthesized expression: e.g., -(2+3)
                    # We treat this as multiplying the result of the inner expression by -1 or 1.
                    result, next_index = parse_expression(tokens, start_index + 1)
                    if sign == '-':
                        return -result, next_index
                    else: # sign == '+'
                        return result, next_index
                else:
                    # Unary minus/plus before a number: e.g., -5, +3.14
                    try:
                        num = float(next_token)
                        if sign == '-':
                            return -num, start_index + 2
                        else: # sign == '+'
                            return num, start_index + 2
                    except ValueError:
                        # If it's not followed by a number, it's likely an error or a binary operator
                        pass
            
            # If none of the above, it's an unrecognized token at this position
            raise ValueError(f"Invalid token sequence starting at index {start_index}: {token}")
            
        def parse_term(tokens, start_index):
            # Handles * and / (Higher Precedence)
            
            # Start by parsing the first factor
            value, next_index = parse_primary(tokens, start_index)
            
            current_index = next_index
            
            while current_index < len(tokens) and tokens[current_index] in ('*', '/'):
                op = tokens[current_index]
                
                # Parse the next factor
                next_value, next_next_index = parse_primary(tokens, current_index + 1)
                
                if op == '*':
                    value *= next_value
                elif op == '/':
                    if next_value == 0.0:
                        raise ZeroDivisionError("Division by zero")
                    value /= next_value
                
                # Update state
                value = value
                current_index = next_next_index
            
            return value, current_index

        def parse_expression(tokens, start_index):
            # Handles + and - (Lower Precedence)
            
            # Start by parsing the first term
            value, next_index = parse_term(tokens, start_index)
            
            current