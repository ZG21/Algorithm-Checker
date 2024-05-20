import random

import copy
def cut_value_calculator(subsets, graph, idx,position_dict):
    #print(f"Jeronimo subsets {subsets} idx {idx} position_dict {position_dict}")
    result = {}
    if len(subsets) == 2 and subsets[1] == '0':
        if len(graph[subsets[0]]) > 0:
            new_graph = copy.deepcopy(graph)
            if subsets[0] in new_graph:
                del new_graph[subsets[0]]
            result = {'subset': subsets, 'graph': new_graph}
            return result
        else:
            #print(f"Jeronimo subsets {subsets} idx {idx} position_dict {position_dict}")
            new_graph = copy.deepcopy(graph)
            for key, values in graph.items():
                for value in values:
                    if subsets[0] == value[0]:
                        new_graph[key].remove(value)
                        result = {'subset': subsets, 'graph': new_graph}
                del new_graph[subsets[0]]
                return results
    elif len(subsets) >= 2 and subsets[1] != 0:
        new_graph = copy.deepcopy(graph)
        actual = {}
        future = {}
        print(f"jeronimo position_dict",position_dict,"subsets",subsets)
        for key, values in graph.items():
            if len(values) > 0:
                if key in subsets:
                   for value in values:
                       #print(f"Jeronimo  value {value} position_dict {position_dict["future"]}")
                       future[value] = position_dict["future"][value]
                       deep_position_dict = copy.deepcopy(position_dict)
                       position_dict_actual=deep_position_dict["actual"]
                       if value not in subsets:
                            #print(f"Jeronimo pruebaa position_dict_actual {position_dict_actual}")
                            if key in position_dict_actual:
                                print(f"Jeronimo position_dict_actual {position_dict_actual }, key {key}")
                                del position_dict_actual[f"{key}"]
                            actual = position_dict_actual
                       else:
                           #print(f"Jeronimo value {value} position_dict {position_dict_actual[f"{key}"]}")
                           actual = {f"{key}": position_dict_actual[f"{key}"]}
                           print(f"Jeronimo actual {actual}")
        """
        
               if len(values) > 0:
                print(f"Jeronimo subsets {subsets} key {key} values {values}")
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
                       
                    else:
                        for value in values:
                            if value[0] != subsets[1]:
                                new_graph[key].remove(value)
                        del new_graph[key]
                        result['graph'] = new_graph
                        result = {'subset': subsets, 'graph': new_graph}"""
        print("----------------------------------------------------------------------------------------------------------------------")
        return result




'''''
 if len(values) > 0:
                print(f"Jeronimo subsets {subsets} key {key} values {values}")
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

'''
