from cut_value_calculator import cut_value_calculator
def add_subsets(key, values, current_subsets, lista_adyacencia, position_dict):
    lista_adyacencia_actual = {k: v for k, v in lista_adyacencia.items() if len(v) > 0}
    if not values:
        current_subsets.append(cut_value_calculator([key, '0'], lista_adyacencia_actual, 0,position_dict))
        return
    current_subsets.append(cut_value_calculator([key, '0'], lista_adyacencia_actual, 0, position_dict))
    def add_values(idx, inside_subset):
        if idx == len(values):
            if inside_subset:
                subsetAlgo = [key] + inside_subset
                current_subsets.append(cut_value_calculator(subsetAlgo, lista_adyacencia_actual, 0,position_dict))
            return
        add_values(idx + 1, inside_subset + [values[idx]])
        add_values(idx + 1, inside_subset)
    add_values(0, [])

def separar_dict_y_crear_posiciones(original_dict):
    # Separar en dos diccionarios
    con_valores = {k: v for k, v in original_dict.items() if v}
    sin_valores = {k: v for k, v in original_dict.items() if not v}
    # Crear diccionarios de posiciones
    posiciones_con_valores = {k: i for i, k in enumerate(con_valores.keys())}
    posiciones_sin_valores = {k: i for i, k in enumerate(sin_valores.keys())}
    #Crear el diccionario final
    resultado = {
        "actual": posiciones_con_valores,
        "future": posiciones_sin_valores
    }
    return resultado