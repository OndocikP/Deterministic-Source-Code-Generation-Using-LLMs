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
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest_key = self.order.pop(0)
            del self.cache[oldest_key]
        self.cache[key] = value
        self.order.append(key)

def simulate_lru_cache(capacity: int, operations: list[tuple]) -> list[int]:
    cache = LRUCache(capacity)
    results = []
    for op, *args in operations:
        if op == 'get':
            results.append(cache.get(args[0]))
        elif op == 'put':
            cache.put(*args)
    return results