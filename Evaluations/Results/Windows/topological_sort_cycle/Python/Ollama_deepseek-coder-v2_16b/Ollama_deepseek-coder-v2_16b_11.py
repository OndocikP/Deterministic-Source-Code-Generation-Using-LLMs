def topological_order(graph: dict[str, list[str]]) -> list[str] | None:
    from collections import defaultdict, deque

    in_degree = defaultdict(int)
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    zero_in_degree_queue = deque([node for node in graph if in_degree[node] == 0])
    topological_order_list = []

    while zero_in_degree_queue:
        node = zero_in_degree_queue.popleft()
        topological_order_list.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                zero_in_degree_queue.append(neighbor)

    if len(topological_order_list) == len(graph):
        return topological_order_list
    else:
        return None