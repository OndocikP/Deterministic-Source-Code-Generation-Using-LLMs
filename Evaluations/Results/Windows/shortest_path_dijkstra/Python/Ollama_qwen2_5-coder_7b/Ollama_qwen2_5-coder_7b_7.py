import heapq

def shortest_path_cost(graph: dict, start: str, end: str) -> int | None:
    if start not in graph or end not in graph:
        return None
    
    priority_queue = [(0, start)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    while priority_queue:
        current_cost, current_node = heapq.heappop(priority_queue)
        
        if current_node == end:
            return current_cost
        
        if current_cost > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node].items():
            distance = current_cost + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return None