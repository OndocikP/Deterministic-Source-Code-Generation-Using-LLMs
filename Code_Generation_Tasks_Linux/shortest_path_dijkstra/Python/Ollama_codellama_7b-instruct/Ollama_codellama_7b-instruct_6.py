def shortest_path_cost(graph: dict, start: str, end: str) -> int | None:
    if start not in graph or end not in graph:
        return None
    priority_queue = [(0, start)]
    visited = set()
    while priority_queue:
        cost, node = heapq.heappop(priority_queue)
        if node == end:
            return cost
        for neighbor, weight in graph[node].items():
            if neighbor not in visited:
                heapq.heappush(priority_queue, (cost + weight, neighbor))
    return None