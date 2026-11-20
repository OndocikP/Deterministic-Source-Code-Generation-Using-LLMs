class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.order = []

    def get(self, key: int) -> int:
        if key in self.cache:
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache[key] = value
            self.order.remove(key)
        else:
            if len(self.cache) >= self.capacity:
                oldest_key = self.order.pop(0)
                del self.cache[oldest_key]
            self.cache[key] = value
        self.order.append(key)

def simulate_lru_cache(capacity: int, operations: list[tuple]) -> list[int]:
    lru_cache = LRUCache(capacity)
    results = []
    for operation in operations:
        if operation[0] == 'put':
            lru_cache.put(operation[1], operation[2])
        elif operation[0] == 'get':
            results.append(lru_cache.get(operation[1]))
    return results