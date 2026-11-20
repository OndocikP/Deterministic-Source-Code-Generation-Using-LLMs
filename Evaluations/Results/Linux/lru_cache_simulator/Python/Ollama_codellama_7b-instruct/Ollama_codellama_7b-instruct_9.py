def simulate_lru_cache(capacity: int, operations: list[tuple]) -> list[int]:
    class Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.prev = None
            self.next = None

    class LRUCache:
        def __init__(self, capacity: int):
            self.capacity = capacity
            self.head = None
            self.tail = None
            self.cache = {}

        def get(self, key: int) -> int:
            if key in self.cache:
                node = self.cache[key]
                self._remove_node(node)
                self._add_node(node)
                return node.value
            else:
                return -1

        def put(self, key: int, value: int) -> None:
            if key in self.cache:
                node = self.cache[key]
                node.value = value
                self._remove_node(node)
                self._add_node(node)
            else:
                node = Node(key, value)
                self._add_node(node)
                self.cache[key] = node
                self._evict()

        def _add_node(self, node: Node) -> None:
            if self.head is None:
                self.head = node
                self.tail = node
            else:
                node.prev = self.tail
                self.tail.next = node
                self.tail = node

        def _remove_node(self, node: Node) -> None:
            if node == self.head:
                self.head = node.next
            if node == self.tail:
                self.tail = node.prev
            if node.prev is not None:
                node.prev.next = node.next
            if node.next is not None:
                node.next.prev = node.prev

        def _evict(self) -> None:
            if len(self.cache) > self.capacity:
                node = self.tail
                self._remove_node(node)
                del self.cache[node.key]

    cache = LRUCache(capacity)
    outputs = []
    for op in operations:
        if op[0] == 'put':
            cache.put(op[1], op[2])
        else:
            outputs.append(cache.get(op[1]))
    return outputs