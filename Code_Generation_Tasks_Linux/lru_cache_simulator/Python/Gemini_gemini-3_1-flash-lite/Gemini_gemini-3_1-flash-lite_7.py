def simulate_lru_cache(capacity: int, operations: list[tuple]) -> list[int]:
    cache = {}
    results = []
    
    for op in operations:
        if op[0] == 'put':
            key, value = op[1], op[2]
            if key in cache:
                cache.pop(key)
            elif len(cache) >= capacity:
                first_key = next(iter(cache))
                cache.pop(first_key)
            cache[key] = value
        elif op[0] == 'get':
            key = op[1]
            if key in cache:
                value = cache.pop(key)
                cache[key] = value
                results.append(value)
            else:
                results.append(-1)
                
    return results