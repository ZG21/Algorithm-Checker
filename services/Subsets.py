import copy

def calculate_subset(subsets, graph, idx):
    result = {}
    new_graph = copy.deepcopy(graph)
    for key, values in graph.items():
        if len(values) > 0:
            if key not in subsets:
                while idx <= len(values) - 1:
                    for i in range(1, len(subsets)):
                        if (idx <= len(values) - 1) and values[idx][0] == subsets[i]:
                            new_graph[key].remove(values[idx])
                            if subsets[i] in new_graph:
                                del new_graph[subsets[i]]
                    idx += 1
                result = subsets
                if idx >= len(values): idx = 0
            else:
                if len(subsets) > len(values) and key in new_graph:
                    del new_graph[key]
                else:
                    for value in values:
                        if value[0] != subsets[1]:
                            new_graph[key].remove(value)
                    del new_graph[key]
                    result = subsets
    return result

def add_subsets(key, values, current_subsets, graph):
    if not values:
        return
    for value in values:
        subsetAlgo = [[value], [key]]  # Cada elemento es una lista
        result = calculate_subset(subsetAlgo, graph, 0)
        if result:  # Asegurarnos de que result no sea None
            current_subsets.append(result)