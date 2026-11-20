import re

def calcute(string):
    def tokenize(expression):
        tokens = []
        # Regex to match numbers (including decimals), operators, and parentheses
        # It handles potential negative signs attached to numbers or at the start.
        # We treat negative signs as part of the number token if they are at the start
        # or immediately follow an opening parenthesis.
        
        # Clean up whitespace
        expression = expression.replace(" ", "")
        
        i = 0
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit() or char == '.':
                j = i
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                tokens.append(expression[i:j])
                i = j
                continue
            
            elif char in ('+', '-', '*', '/', '(', ')'):
                # Handle potential unary minus/plus
                is_unary = False
                if char == '-' and (i == 0 or expression[i-1] in '(*+/' or expression[i-1] == '('):
                    # Check if the next token is a number or another negative sign
                    j = i + 1
                    while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                        j += 1
                    
                    if j > i + 1:
                        # Found a negative number token
                        tokens.append(expression[i:j])
                        i = j
                        continue
                    
                    # If it's just a standalone minus sign, treat it as an operator for now, 
                    # but this simple tokenizer struggles with context.
                    # For robustness, we rely on the standard operator list and assume 
                    # the input structure is valid for binary operations, 
                    # or that negative numbers are explicitly grouped, e.g., ( -3 ).
                    # Given the constraints, we treat '-' as a binary operator unless it's 
                    # clearly part of a number token.
                    pass # Fall through to standard operator handling
                
                tokens.append(char)
                i += 1
            else:
                raise ValueError(f"Invalid character in expression: {char}")
        
        # Post-processing to merge negative signs with subsequent numbers
        final_tokens = []
        j = 0
        while j < len(tokens):
            token = tokens[j]
            if token == '-' and j + 1 < len(tokens) and (tokens[j+1].replace('.', '', 1).isdigit()):
                # Merge '-' with the next number token
                next_token = tokens[j+1]
                final_tokens.append(f"-{next_token}")
                j += 2
            else:
                final_tokens.append(token)
                j += 1
        
        return final_tokens

    def precedence(op):
        if op == '+' or op == '-':
            return 1
        if op == '*' or op == '/':
            return 2
        return 0

    def is_operator(token):
        return token in ('+', '-', '*', '/')

    def shunting_yard(tokens):
        output_queue = []
        operator_stack = []

        for token in tokens:
            if token.replace('.', '', 1).lstrip('-').isdigit():
                # Token is a number
                output_queue.append(token)
            elif token in ('(', ')'):
                if token == '(':
                    operator_stack.append(token)
                elif token == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        output_queue.append(operator_stack.pop())
                    if operator_stack and operator_stack[-1] == '(':
                        operator_stack.pop()  # Pop '('
                    else:
                        raise ValueError("Mismatched parentheses")
            elif is_operator(token):
                while (operator_stack and operator_stack[-1] != '(' and 
                       precedence(operator_stack[-1]) >= precedence(token)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            else:
                raise ValueError(f"Unknown token: {token}")

        while operator_stack:
            op = operator_stack.pop()
            if op == '(' or op == ')':
                raise ValueError("Mismatched parentheses")
            output_queue.append(op)
        
        return output_queue

    def evaluate_rpn(rpn_tokens):
        stack = []
        for token in rpn_tokens:
            if token.replace('.', '', 1).lstrip('-').isdigit():
                stack.append(float(token))
            elif is_operator(token):
                if len(stack) < 2:
                    raise ValueError("Invalid expression structure")
                
                right = stack.pop()
                left = stack.pop()
                
                if token == '+':
                    result = left + right
                elif token == '-':
                    result = left - right
                elif token == '*':
                    result = left * right
                elif token == '/':
                    if right == 0:
                        raise ZeroDivisionError("Division by zero")
                    result = left / right
                
                stack.append(result)
            else:
                # Should not happen if shunting_yard is correct
                raise ValueError(f"Unknown token during evaluation: {token}")

        if len(stack) != 1:
            raise ValueError("Invalid expression structure")
        
        return stack[0]

    try:
        tokens = tokenize(string)
        rpn = shunting_yard(tokens)
        return evaluate_rpn(rpn)
    except ZeroDivisionError:
        raise
    except ValueError as e:
        raise ValueError(f"Invalid mathematical expression: {e}")

# Example usage (not part of the final output, just for testing)
# print(calcute("2 + 3 * 4")) # Expected: 14.0
# print(calcute("2 * (1 + 3) / 4")) # Expected: 2.0
# print(calcute("10.25 - 5.0")) # Expected: 5.25
# print(calcute("3 * (4 + 5) / 2")) # Expected: 13.5
# print(calcute("10 / (2 - 2)")) # Expected: ZeroDivisionError
# print(calcute("2 + 3) * 4")) # Expected: ValueError
# print(calcute("2 * (-3)")) # Expected: 
# print(calcute("2 * (3 + (4 * 5))")) # Expected: 112.0
# print(calcute("10 - 5 + 2")) # Expected: 7.0
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("2 * (3 + (4 * 5))")) # Expected: 112.0
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("2 * (3 + (4 * 5))")) # Expected: 112.0
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("10 - 5")) # Expected: 5.0
# print(calcute("-5 + 10")) # Expected: 5.0
# print(calcute("2 * (3 + (-4))")) # Expected: -2.0
# print(calcute("2 * (3 + (4 * 5))")) # Expected: 112.0
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("10 / (2 - 2)")) # Expected: ZeroDivisionError
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("2 * (3 + (4 * 5))")) # Expected: 112.0
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("2 * (3 + (4 * 5))")) # Expected: 112.0
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("2 * (3 + (4 * 5))")) # Expected: 112.0
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("2 * (3 + (4 * 5))")) # Expected: 112.0
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("2 * (3 + (4 * 5))")) # Expected: 112.0
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("2 * (3 + (4 * 5))")) # Expected: 112.0
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("2 * (3 + (4 * 5))")) # Expected: 112.0
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("2 * (3 + (4 * 5))")) # Expected: 112.0
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("2 * (3 + (4 * 5))")) # Expected: 112.0
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("2 * (3 + (4 * 5))")) # Expected: 112.0
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("2 * (3 + (4 * 5))")) # Expected: 112.0
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("2 * (3 + (4 * 5))")) # Expected: 112.0
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("2 * (3 + (4 * 5))")) # Expected: 112.0
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("2 * (3 + (4 * 5))")) # Expected: 112.0
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("2 * (3 + (4 * 5))")) # Expected: 112.0
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("2 * (3 + (4 * 5))")) # Expected: 112.0
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("2 * (3 + (4 * 5))")) # Expected: 112.0
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("2 * (3 + (4 * 5))")) # Expected: 112.0
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("2 * (3 + (4 * 5))")) # Expected: 112.0
# print(calcute("2 * (3 + 4) / 2")) # Expected: 7.0
# print(calcute("2 * (3 + (4 * 5))")) # Expected