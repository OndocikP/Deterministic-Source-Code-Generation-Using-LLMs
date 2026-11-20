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
                        # Look back further if there was whitespace
                        k = i - 1
                        while k >= 0 and expression[k].isspace():
                            k -= 1
                        if k < 0:
                            is_unary = True
                        else:
                            prev_char = expression[k]
                            if prev_char in '+-*/(':
                                is_unary = True
                            else:
                                is_unary = False
                    elif prev_char in '+-*/(':
                        is_unary = True
                    else:
                        is_unary = False

                if is_unary:
                    # Check if the next character is a digit or a decimal point
                    j = i + 1
                    while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                        j += 1
                    
                    if j > i + 1:
                        # It's a number starting with a sign
                        tokens.append(expression[i:j])
                        i = j
                        continue
                    else:
                        # It's a standalone unary operator (e.g., just '-' or '+')
                        # We treat it as a special token for now, which will be handled in parsing
                        tokens.append(char)
                        i += 1
                        continue
                else:
                    # Binary operator
                    tokens.append(char)
                    i += 1
                    continue
            
            i += 1 # Should not happen if input is valid

        return tokens

    def shunting_yard(tokens):
        output_queue = []
        operator_stack = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            if token.replace('.', '', 1).isdigit() or (token.startswith('-') and token[1:].replace('.', '', 1).isdigit()):
                # Number (including signed numbers parsed as one token)
                output_queue.append(float(token))
            elif token in '()':
                if token == '(':
                    operator_stack.append(token)
                elif token == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        output_queue.append(operator_stack.pop())
                    if operator_stack and operator_stack[-1] == '(':
                        operator_stack.pop() # Discard '('
                    else:
                        raise ValueError("Mismatched parentheses")
            elif token in '+-*/':
                # Handle unary minus/plus if it was tokenized separately
                if token == '-' and (not output_queue or isinstance(output_queue[-1], float) and output_queue[-1] >= 0):
                    # This logic is complex to handle purely in tokenization for unary minus.
                    # We rely on the fact that if a number starts with '-', it's tokenized as one.
                    # If we encounter '-' here, it must be a binary operator, unless it's the first token.
                    # Since we are using a simplified tokenizer, we assume any '-' here is binary unless it's the first token.
                    pass # Let standard precedence rules handle it for now, relying on the tokenizer to group signed numbers.
                
                while (operator_stack and operator_stack[-1] != '(' and 
                       precedence.get(operator_stack[-1], 0) >= precedence[token]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            else:
                # This handles tokens that might be incorrectly parsed or are complex unary operators
                # For robustness, we assume the tokenizer handled numbers correctly.
                pass

        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses")
            output_queue.append(op)
        
        return output_queue

    def apply_op(op, b, a):
        if op == '+': return a + b
        if op == '-': return a - b
        if op == '*': return a * b
        if op == '/': 
            if b == 0: raise ZeroDivisionError("Division by zero")
            return a / b

    def evaluate_rpn(rpn_tokens):
        stack = []
        for token in rpn_tokens:
            if isinstance(token, float):
                stack.append(token)
            else: # Operator
                op = token
                if len(stack) < 2:
                    raise ValueError("Invalid expression structure")
                b = stack.pop()
                a = stack.pop()
                stack.append(apply_op(op, b, a))
        
        if len(stack) != 1:
            raise ValueError("Invalid expression structure")
        return stack[0]

    # --- Pre-processing for Unary Minus ---
    # The standard Shunting-Yard implementation struggles with implicit unary operators 
    # when they are not explicitly separated (e.g., -3 vs 1 - 3).
    # We modify the tokenization/parsing slightly to handle this by replacing unary '-' with a placeholder.
    
    def preprocess_expression(expression):
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]
            if char.isspace():
                i += 1
                continue

            if char in '+-*/()':
                is_unary = False
                if char == '-' or char == '+':
                    # Check if it's unary: start of string, or preceded by '(', or preceded by another operator
                    if i == 0:
                        is_unary = True
                    else:
                        prev_char = expression[i-1]
                        if prev_char.isspace():
                            k = i - 1
                            while k >= 0 and expression[k].isspace():
                                k -= 1
                            if k < 0:
                                is_unary = True
                            else:
                                prev_char = expression[k]
                                if prev_char in '+-*/(':
                                    is_unary = True
                                else:
                                    is_unary = False
                        elif prev_char in '+-*/(':
                            is_unary = True
                        else:
                            is_unary = False
                
                if is_unary and char == '-':
                    # Replace unary minus with a special token 'UNARY_MINUS'
                    tokens.append('UNARY_MINUS')
                elif char == '-':
                    tokens.append('-')
                elif char == '+':
                    tokens.append('+')
                elif char in '*/()':
                    tokens.append(char)
                else:
                    # Binary operator
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

    def shunting_yard_with_unary(tokens):
        output_queue = []
        operator_stack = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, 'UNARY_MINUS': 3}

        for token in tokens:
            if token.replace('.', '', 1).isdigit():
                output_queue.append(float(token))
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()
                else:
                    raise ValueError("Mismatched parentheses")
            elif token in '+-*/UNARY_MINUS':
                op1 = token
                
                if op1 == 'UNARY_MINUS':
                    # Unary minus is right-associative and has high precedence
                    while (operator_stack and operator_stack[-1] != '(' and 
                           precedence.get(operator_stack[-1], 0) > precedence[op1]):
                        output_queue.append(operator_stack.pop())
                    operator_stack.append(op1)
                else: # Binary operators
                    while (operator_stack and operator_stack[-1] != '(' and 
                           precedence.get(operator_stack[-1], 0) >= precedence[op1]):
                        output_queue.append(operator_stack.pop())
                    operator_stack.append(op1)

        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses")
            output_queue.append(op)
        
        return output_queue

    def apply_op_with_unary(op, b, a):
        if op == '+': return a + b
        if op == '-': return a - b
        if op == '*': return a * b
        if op == '/': 
            if b == 0: raise ZeroDivisionError("Division by zero")
            return a / b
        if op == 'UNARY_MINUS':
            # Unary minus applies to the single operand 'a'
            return -a
        raise ValueError("Unknown operator")

    def evaluate_rpn_with_unary(rpn_tokens):
        stack = []
        for token in rpn_tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in '+-*/UNARY_MINUS':
                if token == 'UNARY_MINUS':
                    if len(stack) < 1:
                        raise ValueError("Invalid expression structure for unary minus")
                    a = stack.pop()
                    stack.append(apply_op_with_unary(token, None, a))
                else: # Binary operators
                    if len(stack) < 2:
                        raise ValueError("Invalid expression structure")
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(apply_op_with_unary(token, b, a))
            else:
                raise ValueError(f"Unknown token in RPN: {token}")
        
        if len(stack) != 1:
            raise ValueError("Invalid expression structure")
        return stack[0]

    tokens = preprocess_expression(expression)
    rpn = shunting_yard_with_unary(tokens)
    return evaluate_rpn_with_unary(rpn)