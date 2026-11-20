def topological_order(graph: dict[str, list[str]]) -> list[str] | None:
    # Collect all nodes from both keys and values to ensure isolated nodes are included
    all_nodes = set()
    for node in graph:
        all_nodes.add(node)
        for neighbor in graph[node]:
            all_nodes.add(neighbor)
    
    if not all_nodes:
        return []
    
    # Calculate in-degrees for all nodes without mutating the input graph
    in_degree = {node: 0 for node in all_nodes}
    
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1
    
    # Use a sorted list as a priority queue to always pick the lexicographically smallest node
    import heapq
    zero_in_degree = [node for node, degree in in_degree.items() if degree == 0]
    heapq.heapify(zero_in_degree)
    
    result = []
    
    while zero_in_degree:
        current_node = heapq.heappop(zero_in_degree)
        result.append(current_node)
        
        # Process neighbors of the current node
        if current_node in graph:
            for neighbor in graph[current_node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    heapq.heappush(zero_in_degree, neighbor)
    
    # If the result does not contain all nodes, there is a cycle
    if len(result) != len(all_nodes):
        return None
    
    return result