def topological_order(graph: dict[str, list[str]]) -> list[str] | None:
    nodes = set(graph.keys())
    for neighbors in graph.values():
        for neighbor in neighbors:
            nodes.add(neighbor)

    in_degree = {node: 0 for node in nodes}
    
    for node in graph:
        for neighbor in graph[node]:
            if neighbor in in_degree:
                in_degree[neighbor] += 1

    queue = []
    for node in sorted(list(nodes)):
        if in_degree[node] == 0:
            queue.append(node)

    topological_order_list = []
    
    while queue:
        # Lexicographically smallest node is already at the front because we use a sorted list/queue
        # and only add new zero in-degree nodes in sorted order.
        u = queue.pop(0)
        topological_order_list.append(u)
        
        if u in graph:
            for v in graph[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    # Insert new zero in-degree nodes while maintaining lexicographical order
                    # This simulates a min-heap behavior for the queue
                    import bisect
                    bisect.insort(queue, v)

    if len(topological_order_list) != len(nodes):
        return None
    
    return topological_order_list