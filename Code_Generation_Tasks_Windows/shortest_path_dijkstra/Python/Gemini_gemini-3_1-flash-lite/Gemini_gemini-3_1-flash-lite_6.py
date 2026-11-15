import heapq

def shortest_path_cost(graph: dict, start: str, end: str) -> int | None:
    if start not in graph or end not in graph:
        return None
    
    if start == end:
        return 0
    
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_node]:
            continue
            
        if current_node == end:
            return int(current_distance)
            
        for neighbor, weight in graph.get(current_node, {}).items():
            distance = current_distance + weight
            
            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
                
    return None