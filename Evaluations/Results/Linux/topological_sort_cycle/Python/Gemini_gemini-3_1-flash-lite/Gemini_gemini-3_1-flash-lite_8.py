import heapq

def topological_order(graph: dict[str, list[str]]) -> list[str] | None:
    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        all_nodes.update(neighbors)
    
    in_degree = {node: 0 for node in all_nodes}
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1
            
    pq = [node for node in all_nodes if in_degree[node] == 0]
    heapq.heapify(pq)
    
    result = []
    while pq:
        u = heapq.heappop(pq)
        result.append(u)
        
        if u in graph:
            for v in graph[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    heapq.heappush(pq, v)
                    
    if len(result) == len(all_nodes):
        return result
    return None