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
        current_node = queue.pop(0)
        topological_order_list.append(current_node)
        
        if current_node in graph:
            neighbors = sorted(graph[current_node])
            for neighbor in neighbors:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    # Maintain lexicographical order for next additions to the queue
                    # Since we are using a list as a queue and need lexicographical order,
                    # we must ensure that when multiple nodes become ready, we process the smallest one first.
                    # A standard queue (FIFO) won't guarantee this if we just append.
                    # We will collect all ready nodes and sort them before appending/processing.
                    pass # We handle sorting implicitly by how we manage the queue/next candidates

    # Re-implementing the queue management to strictly adhere to lexicographical smallest first
    
    in_degree = {node: 0 for node in nodes}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    # Use a min-heap or a sorted list to simulate the priority queue (lexicographically smallest first)
    import heapq
    pq = []
    for node in nodes:
        if in_degree[node] == 0:
            heapq.heappush(pq, node)

    topological_order_list = []
    
    while pq:
        current_node = heapq.heappop(pq)
        topological_order_list.append(current_node)
        
        if current_node in graph:
            # Process neighbors in lexicographical order to ensure deterministic behavior 
            # if multiple neighbors become ready simultaneously (though the heap handles the selection)
            for neighbor in sorted(graph[current_node]):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    heapq.heappush(pq, neighbor)

    if len(topological_order_list) != len(nodes):
        return None
    
    return topological_order_list