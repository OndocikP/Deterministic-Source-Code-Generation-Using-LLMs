def simulate_lru_cache(capacity: int, operations: list[tuple]) -> list[int]:
    cache = {}
    order = []  # Doubly linked list simulation using a list of keys
    
    results = []
    
    for op in operations:
        if op[0] == 'put':
            key, value = op[1], op[2]
            if key in cache:
                # Move existing key to the end (most recently used)
                order.remove(key)
                order.append(key)
                cache[key] = value
            else:
                # If cache is full, remove the least recently used (first element)
                if len(cache) >= capacity:
                    lru_key = order.pop(0)
                    del cache[lru_key]
                
                # Add new key to the end
                order.append(key)
                cache[key] = value
        
        elif op[0] == 'get':
            key = op[1]
            if key in cache:
                # Move accessed key to the end (most recently used)
                order.remove(key)
                order.append(key)
                results.append(cache[key])
            else:
                results.append(-1)
    
    return results