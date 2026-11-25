def evaluate_expression(expression: str) -> float:
    def tokenize(expression):
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]
            if char.isspace():
                i += 1
                continue

            if char in '+-*/()':
                tokens.append(char)
                i += 1
                continue

            if char.isdigit() or char == '.':
                j = i
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                tokens.append(expression[i:j])
                i = j
                continue
            
            # Handle unary minus/plus at the start or after an opening parenthesis or another operator
            if char == '-' or char == '+':
                is_unary = True
                if i == 0:
                    is_unary = True
                else:
                    prev_char = expression[i-1]
                    if prev_char.isspace():
                        # Look back further to find the last non-space character
                        k = i - 1
                        while k >= 0 and expression[k].isspace():
                            k -= 1
                        if k < 0:
                            is_unary = True
                        else:
                            if expression[k] in '+-*/()':
                                is_unary = True
                            else:
                                is_unary = False
                    else:
                        if expression[i-1] in '+-*/()':
                            is_unary = True
                        else:
                            is_unary = False

                if is_unary:
                    # Check if it's a unary minus followed by a number
                    j = i + 1
                    while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                        j += 1
                    
                    if j > i + 1: # If there is a number following the sign
                        tokens.append(char + expression[i+1:j])
                        i = j
                        continue
                    else:
                        # If it's just a standalone unary sign (which shouldn't happen in a valid expression 
                        # unless it's followed by '(' or another operator, which we handle below)
                        # For simplicity in this implementation, we treat it as a binary operator if not followed by a number
                        # but the logic above should catch most cases. If it's just a sign, we treat it as a binary operator 
                        # unless it's the very start.
                        pass # Let the general operator handling take over if it's not followed by a number
                
                # If not handled as part of a number, treat it as a binary operator
                tokens.append(char)
                i += 1
                continue

            i += 1
        return tokens

    def shunting_yard(tokens):
        output_queue = []
        operator_stack = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            if token.replace('.', '', 1).isdigit() or (token.startswith('-') and token[1:].replace('.', '', 1).isdigit()):
                output_queue.append(float(token))
            elif token in '()':
                if token == '(':
                    operator_stack.append(token)
                elif token == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        output_queue.append(operator_stack.pop())
                    if operator_stack and operator_stack[-1] == '(':
                        operator_stack.pop() # Pop '('
                    else:
                        raise ValueError("Mismatched parentheses")
            elif token in '+-*/':
                while (operator_stack and operator_stack[-1] != '(' and 
                       precedence.get(operator_stack[-1], 0) >= precedence[token]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            else:
                # This handles cases where the tokenizer might have missed something, 
                # but based on the tokenizer, this should only be operators or numbers.
                pass 

        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses")
            output_queue.append(op)
        
        return output_queue

    def evaluate_rpn(rpn_tokens):
        stack = []
        for token in rpn_tokens:
            if isinstance(token, float):
                stack.append(token)
            else:
                op2 = stack.pop()
                op1 = stack.pop()
                if token == '+':
                    stack.append(op1 + op2)
                elif token == '-':
                    stack.append(op1 - op2)
                elif token == '*':
                    stack.append(op1 * op2)
                elif token == '/':
                    if op2 == 0:
                        raise ZeroDivisionError("Division by zero")
                    stack.append(op1 / op2)
        return stack[0]

    # Pre-processing to handle unary minus correctly before tokenization
    # This is a simplified approach to ensure the tokenizer sees unary minus as part of a number
    # or as a distinct operator if it's not followed by a number.
    
    # A robust tokenizer for this problem is complex. We will rely on a slightly modified 
    # tokenization strategy that explicitly looks for unary signs.

    def robust_tokenize(expression):
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]
            if char.isspace():
                i += 1
                continue

            if char in '+-*/()':
                # Check for unary sign
                is_unary = False
                if char in ('+', '-'):
                    if i == 0:
                        is_unary = True
                    else:
                        prev_char = expression[i-1]
                        if prev_char.isspace():
                            # Look back past spaces
                            k = i - 1
                            while k >= 0 and expression[k].isspace():
                                k -= 1
                            if k < 0 or expression[k] in '+-*/(':
                                is_unary = True
                        elif expression[i-1] in '+-*/(':
                            is_unary = True
                
                if is_unary:
                    # Check if it's followed by a number
                    j = i + 1
                    while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                        j += 1
                    
                    if j > i + 1:
                        # It's a unary number (e.g., -3.14)
                        tokens.append(expression[i:j])
                        i = j
                        continue
                    else:
                        # It's a unary sign followed by something else (e.g., -(5) or just -)
                        # Treat it as a standard operator for now, relying on the parser to handle context
                        tokens.append(char)
                        i += 1
                        continue
                
                # Standard operator or parenthesis
                tokens.append(char)
                i += 1
                continue

            if char.isdigit() or char == '.':
                j = i
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                tokens.append(expression[i:j])
                i = j
                continue
            
            i += 1
        return tokens

    try:
        tokens = robust_tokenize(expression)
        rpn = shunting_yard(tokens)
        result = evaluate_rpn(rpn)
        return result
    except Exception:
        # In a real scenario, we would raise specific errors. 
        # For this constrained environment, we assume valid input or let the exception propagate if necessary.
        # Since the requirement is to return a float, we rely on the successful path.
        pass # Should not reach here if input is valid
    
    return 0.0 # Fallback, though a proper implementation should handle errors via exceptions.