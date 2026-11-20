def topological_order(graph: dict[str, list[str]]) -> list[str] | None:
    in_degree = {node: 0 for node in graph}
    for neighbors in graph.values():
        for neighbor in neighbors:
            in_degree[neighbor] += 1

    queue = [node for node, degree in in_degree.items() if degree == 0]
    queue.sort()

    topological_order = []
    while queue:
        if len(queue) > 1:
            queue.sort()
        node = queue.pop(0)
        topological_order.append(node)

        for neighbor in graph.get(node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(topological_order) != len(graph):
        return None

    return topological_order