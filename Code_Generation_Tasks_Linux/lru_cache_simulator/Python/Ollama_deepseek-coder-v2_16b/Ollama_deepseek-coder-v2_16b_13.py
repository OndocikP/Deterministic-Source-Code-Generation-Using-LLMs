from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        else:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value

    def put(self, key: int, value: int):
        if key in self.cache:
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value

def simulate_lru_cache(capacity: int, operations: list[tuple]) -> list[int]:
    lru = LRUCache(capacity)
    results = []
    for operation in operations:
        if operation[0] == 'get':
            results.append(lru.get(operation[1]))
        elif operation[0] == 'put':
            lru.put(operation[1], operation[2])
    return results