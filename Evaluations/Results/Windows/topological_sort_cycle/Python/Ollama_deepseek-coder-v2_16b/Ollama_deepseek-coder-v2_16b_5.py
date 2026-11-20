def topological_order(graph: dict[str, list[str]]) -> list[str] | None:
    from collections import defaultdict, deque

    # Calculate in-degrees for each node
    in_degree = defaultdict(int)
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    # Find all nodes with zero in-degree
    zero_in_degree_nodes = deque([node for node in graph if node not in in_degree])

    # If there are no nodes with zero in-degree, there is a cycle
    if not zero_in_degree_nodes:
        return None

    # Kahn's algorithm
    topo_order = []
    while zero_in_degree_nodes:
        node = zero_in_degree_nodes.popleft()
        topo_order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                zero_in_degree_nodes.append(neighbor)

    # If the number of nodes in the topological order is less than the number of nodes in the graph, there is a cycle
    if len(topo_order) != len(graph):
        return None

    return topo_order