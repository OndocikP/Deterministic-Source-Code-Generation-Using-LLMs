def topological_order(graph: dict[str, list[str]]) -> list[str] | None:
    if not graph:
        return []
    
    nodes = set()
    for neighbors in graph.values():
        nodes.update(neighbors)
    nodes = list(nodes)
    
    in_degree = {node: 0 for node in nodes}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1
    
    queue = []
    for node in sorted(nodes):
        if in_degree[node] == 0:
            queue.append(node)
    
    result = []
    while queue:
        node = min(queue)
        queue.remove(node)
        result.append(node)
        for neighbor in graph.get(node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(result) != len(nodes):
        return None
    
    return result