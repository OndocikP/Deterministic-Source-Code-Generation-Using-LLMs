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
            self.size = 0
            self.head = None
            self.tail = None
            self.cache = {}

        def put(self, key: int, value: int) -> None:
            if key in self.cache:
                node = self.cache[key]
                node.value = value
                self._move_to_front(node)
            else:
                node = Node(key, value)
                self.cache[key] = node
                self._add_to_front(node)
                self.size += 1
                if self.size > self.capacity:
                    self._remove_last()

        def get(self, key: int) -> int:
            if key in self.cache:
                node = self.cache[key]
                self._move_to_front(node)
                return node.value
            else:
                return -1

        def _add_to_front(self, node: Node) -> None:
            node.prev = None
            node.next = self.head
            if self.head is not None:
                self.head.prev = node
            self.head = node
            if self.tail is None:
                self.tail = node

        def _remove_last(self) -> None:
            node = self.tail
            self.tail = node.prev
            if self.tail is not None:
                self.tail.next = None
            del self.cache[node.key]
            self.size -= 1

        def _move_to_front(self, node: Node) -> None:
            self._remove_node(node)
            self._add_to_front(node)

        def _remove_node(self, node: Node) -> None:
            if node.prev is not None:
                node.prev.next = node.next
            if node.next is not None:
                node.next.prev = node.prev
            if node == self.head:
                self.head = node.next
            if node == self.tail:
                self.tail = node.prev

    cache = LRUCache(capacity)
    outputs = []
    for op in operations:
        if op[0] == 'put':
            cache.put(op[1], op[2])
        else:
            outputs.append(cache.get(op[1]))
    return outputs