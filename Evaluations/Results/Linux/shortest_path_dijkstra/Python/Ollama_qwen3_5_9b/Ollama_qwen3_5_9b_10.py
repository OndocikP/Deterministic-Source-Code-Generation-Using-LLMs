import heapq

def shortest_path_cost(graph: dict, start: str, end: str) -> int | None:
    if start not in graph or end not in graph:
        return None
    
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    pq = [(0, start)]
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        if current_dist > distances[current_node]:
            continue
        
        if current_node == end:
            return current_dist
        
        for neighbor, weight in graph.get(current_node, {}).items():
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    return None