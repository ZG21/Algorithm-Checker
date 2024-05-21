import random

import copy
def cut_value_calculator(subsets, lista_adyacencia, idx,position_dict):
    #print("MOMO add", position_dict, "\n", lista_adyacencia, "\n", subsets,"\n",idx)
    result = {}
    actual = {}
    actual_rest = {}
    future = {}
    future_rest = {}
    if len(subsets) == 2 and subsets[1] == '0':
        deep_position_dict = copy.deepcopy(position_dict)
        position_dict_actual=deep_position_dict["actual"]
        if subsets[0] not in lista_adyacencia.keys() :
            future[subsets[0]] = position_dict["future"][subsets[0]]
            future_rest = {key: value for key, value in position_dict["future"].items() if key != subsets[0]}
            for key, values in lista_adyacencia.items():
                if subsets[0] not in values:
                    actual[f"{key}"] = position_dict_actual[f"{key}"]
                else:
                    actual_rest[f"{key}"] = position_dict_actual[f"{key}"]
            result = {"subsets": subsets, "actual": actual, "actual_rest":actual_rest, "future": future, "future_rest": future_rest}
            return result
        else:
            for value in lista_adyacencia[subsets[0]]:
                future[value] = position_dict["future"][value]
            future_rest = {key: value for key, value in position_dict["future"].items() if key not in lista_adyacencia[subsets[0]]}
            llaves_filtradas = [key for key, value in lista_adyacencia.items() if key != subsets[0]]
            for value in llaves_filtradas:
                actual[f"{value}"] = position_dict_actual[f"{value}"]
            actual_rest = {key: value for key, value in position_dict_actual.items() if key not in llaves_filtradas}
            result = {"subsets": subsets, "actual": actual, "actual_rest":actual_rest, "future": future, "future_rest": future_rest}
        return result
    elif len(subsets) >= 2 and subsets[1] != 0:
        values_by_subset_key = lista_adyacencia[f"{subsets[0]}"]
        for value in values_by_subset_key:
            future[value] = position_dict["future"][value]
            future_rest = {key: value for key, value in position_dict["future"].items() if key not in values_by_subset_key}
            deep_position_dict = copy.deepcopy(position_dict)
            position_dict_actual=deep_position_dict["actual"]
            if value not in subsets:
                for key_C, values_C in lista_adyacencia.items():
                    if key_C not in subsets and value in values_C:
                        actual[f"{key_C}"] = position_dict_actual[f"{key_C}"]
                    else:
                        actual_rest[f"{key_C}"] = position_dict_actual[f"{key_C}"]
            else:
                if len(subsets) -1 == len(values_by_subset_key):
                    actual[f"{subsets[0]}"] = position_dict_actual[f"{subsets[0]}"]
                    actual_rest = {key: value for key, value in position_dict_actual.items() if key != subsets[0]}
        result = {"subsets": subsets, "actual": actual, "actual_rest":actual_rest, "future": future, "future_rest": future_rest}
        return result
