def simulate_lru_cache(capacity: int, operations: list[tuple]) -> list[int]:
    cache = {}
    order = []
    result = []

    for op in operations:
        if op[0] == 'put':
            key = op[1]
            value = op[2]
            if key in cache:
                cache[key] = value
                order.remove(key)
            else:
                if len(cache) >= capacity:
                    lru_key = order.pop(0)
                    del cache[lru_key]
                cache[key] = value
            order.append(key)
        elif op[0] == 'get':
            key = op[1]
            if key in cache:
                order.remove(key)
                order.append(key)
                result.append(cache[key])
            else:
                result.append(-1)
    return result