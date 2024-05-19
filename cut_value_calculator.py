import random

import copy
def cut_value_calculator(subsets, graph, idx):
    result = {}
    if len(subsets) == 2 and subsets[1] == '0':
        if len(graph[subsets[0]]) > 0:
            new_graph = copy.deepcopy(graph)
            if subsets[0] in new_graph:
                del new_graph[subsets[0]]
            result = {'subset': subsets, 'graph': new_graph}
            return result
        else:
            highest = 0
            new_graph = copy.deepcopy(graph)
            for key, values in graph.items():
                for value in values:
                    if subsets[0] == value[0]:
                        new_graph[key].remove(value)
                        result = {'subset': subsets, 'graph': new_graph}
                del new_graph[subsets[0]]
                return result
    elif len(subsets) >= 2 and subsets[1] != 0:
        new_graph = copy.deepcopy(graph)
        for key, values in graph.items():
            if len(values) > 0:
                if key not in subsets:
                    while idx <= len(values) - 1:
                        for i in range(1, len(subsets)):
                            if (idx <= len(values)-1) and values[idx][0] == subsets[i]:
                                new_graph[key].remove(values[idx])
                                if subsets[i] in new_graph:
                                    del new_graph[subsets[i]]
                                result['graph'] = new_graph
                        idx += 1
                    result = {'subset': subsets, 'graph': new_graph}
                    if idx >= len(values): idx = 0
                else:
                    if len(subsets) > len(values) and key in new_graph:
                        del new_graph[key]
                    else:
                        for value in values:
                            if value[0] != subsets[1]:
                                new_graph[key].remove(value)
                        del new_graph[key]
                        result['graph'] = new_graph
                        result = {'subset': subsets, 'graph': new_graph}
        return result

