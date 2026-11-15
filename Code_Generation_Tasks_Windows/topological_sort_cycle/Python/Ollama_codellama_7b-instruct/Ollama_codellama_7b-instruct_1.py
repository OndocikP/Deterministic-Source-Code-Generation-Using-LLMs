def topological_order(graph: dict[str, list[str]]) -> list[str] | None:
    """
    Returns a topological ordering for a directed graph, or None if the graph contains a cycle.
    """
    # Create a copy of the input graph to avoid mutating it
    graph_copy = {node: graph[node] for node in graph}

    # Initialize the output list and the set of nodes with zero in-degree
    output = []
    zero_in_degree = set()

    # Loop until all nodes have been visited
    while graph_copy:
        # Find all nodes with zero in-degree
        for node in graph_copy:
            if len(graph_copy[node]) == 0:
                zero_in_degree.add(node)

        # If there are no nodes with zero in-degree, the graph contains a cycle
        if not zero_in_degree:
            return None

        # Add the lexicographically smallest node with zero in-degree to the output
        smallest_node = min(zero_in_degree, key=lambda x: x)
        output.append(smallest_node)

        # Remove the smallest node and its edges from the graph
        del graph_copy[smallest_node]
        for neighbor in graph_copy:
            if smallest_node in graph_copy[neighbor]:
                graph_copy[neighbor].remove(smallest_node)

        # Remove the smallest node from the set of nodes with zero in-degree
        zero_in_degree.remove(smallest_node)

    # Return the topological ordering
    return output