def calcute(expression):
    import re
    
    expression = expression.replace(" ", "")
    
    if not expression:
        raise ValueError("Empty expression")
    
    token_pattern = r'\d+(\.\d+)?|[+\-*/()]'
    tokens = re.findall(token_pattern, expression)
    
    if not tokens:
        raise ValueError("No valid tokens found")
    
    def parse_expression(tokens):
        pos = [0]
        
        def peek():
            return tokens[pos[0]] if pos[0] < len(tokens) else None
        
        def consume():
            val = tokens[pos[0]]
            pos[0] += 1
            return val
        
        def parse_primary():
            token = peek()
            if token == '(':
                consume()
                result = parse_expression()
                if peek() != ')':
                    raise ValueError("Missing closing parenthesis")
                consume()
                return result
            elif token is None:
                raise ValueError("Unexpected end of expression")
            else:
                try:
                    num = float(token)
                    consume()
                    return num
                except ValueError:
                    raise ValueError(f"Invalid token: {token}")
        
        def parse_term():
            left = parse_primary()
            
            while peek() in ['*', '/']:
                op = consume()
                right = parse_primary()
                
                if op == '*':
                    left = left * right
                elif op == '/':
                    if right == 0:
                        raise ZeroDivisionError("Division by zero")
                    left = left / right
            
            return left
        
        def parse_sum():
            left = parse_term()
            
            while peek() in ['+', '-']:
                op = consume()
                right = parse_term()
                
                if op == '+':
                    left = left + right
                elif op == '-':
                    left = left - right
            
            return left
        
        result = parse_sum()
        
        if pos[0] < len(tokens):
            raise ValueError(f"Unexpected token: {tokens[pos[0]]}")
        
        return result
    
    try:
        result = parse_expression(tokens)
        return float(result)
    except ZeroDivisionError:
        raise
    except Exception as e:
        if isinstance(e, ValueError):
            raise
        raise ValueError(f"Invalid expression: {expression}")