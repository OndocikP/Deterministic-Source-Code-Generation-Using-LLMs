from collections import OrderedDict

def simulate_lru_cache(capacity: int, operations: list[tuple]) -> list[int]:
    cache = OrderedDict()
    results = []

    for operation in operations:
        op_type = operation[0]

        if op_type == 'put':
            key, value = operation[1], operation[2]
            if key in cache:
                cache.move_to_end(key)
                cache[key] = value
            else:
                if len(cache) >= capacity:
                    # Evict the least recently used item (the first item)
                    cache.popitem(last=False)
                cache[key] = value
        
        elif op_type == 'get':
            key = operation[1]
            if key in cache:
                value = cache[key]
                # Move the accessed item to the end to mark it as most recently used
                cache.move_to_end(key)
                results.append(value)
            else:
                results.append(-1)
                
    return results