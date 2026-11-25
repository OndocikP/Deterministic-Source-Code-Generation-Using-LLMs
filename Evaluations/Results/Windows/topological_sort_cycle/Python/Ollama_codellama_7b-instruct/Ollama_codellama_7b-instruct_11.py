def topological_order(graph: dict[str, list[str]]) -> list[str] | None:
    """
    Returns a topological ordering for a directed graph, or None if the graph contains a cycle.
    """
    # Create a copy of the input graph to avoid mutating it
    graph_copy = {node: graph[node] for node in graph}

    # Initialize the output list
    ordering = []

    # Loop until the graph is empty
    while graph_copy:
        # Find all nodes with zero in-degree
        zero_in_degree_nodes = [node for node in graph_copy if graph_copy[node][0] == 0]

        # If there are no nodes with zero in-degree, the graph contains a cycle
        if not zero_in_degree_nodes:
            return None

        # Choose the lexicographically smallest node with zero in-degree
        smallest_node = min(zero_in_degree_nodes, key=lambda x: x)

        # Add the smallest node to the output list
        ordering.append(smallest_node)

        # Remove the smallest node and its edges from the graph
        del graph_copy[smallest_node]
        for neighbor in graph_copy:
            if smallest_node in graph_copy[neighbor]:
                graph_copy[neighbor].remove(smallest_node)

    # Return the topological ordering
    return ordering