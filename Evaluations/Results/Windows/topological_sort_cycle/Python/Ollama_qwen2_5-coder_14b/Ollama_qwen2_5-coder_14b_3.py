def topological_order(graph: dict[str, list[str]]) -> list[str] | None:
    in_degree = {node: 0 for node in graph}
    for neighbors in graph.values():
        for neighbor in neighbors:
            if neighbor in in_degree:
                in_degree[neighbor] += 1

    zero_in_degree = [node for node, degree in in_degree.items() if degree == 0]
    zero_in_degree.sort()

    order = []
    while zero_in_degree:
        node = zero_in_degree.pop(0)
        order.append(node)
        for neighbor in graph.get(node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                zero_in_degree.append(neighbor)
                zero_in_degree.sort()

    if len(order) == len(graph):
        return order
    else:
        return None