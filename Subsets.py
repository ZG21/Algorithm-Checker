from cut_value_calculator import cut_value_calculator
def add_subsets(key, values, current_subsets, lista_adyacencia, position_dict):
    if not values:
        current_subsets.append(cut_value_calculator([key, '0'], lista_adyacencia, 0,position_dict))
        return
    current_subsets.append(cut_value_calculator([key, '0'], lista_adyacencia, 0, position_dict))
    def add_values(idx, inside_subset):
        if idx == len(values):
            if inside_subset:
                subsetAlgo = [key] + inside_subset
                #current_subsets.append(subsetAlgo)
                current_subsets.append(cut_value_calculator(subsetAlgo, lista_adyacencia, 0,position_dict))
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

''''
1 cuando sgte valor es 0
    si valor esta en actuales
        agregamos en actuales todos los indices de los actuales menos el del valor
        buscar valor en lista adyacencias
        recorremos sus values y su valor correspndiente en indices se agrega a futuros
    si valor esta en futuros
        agregamos en futuros todos los indices del valor
        si valor no esta en value agrego a actuales el indice de la key donde no estuvo el valor
2 cuando sgte valor != 0
    agregamos indices de futuros en futuro 
    agregamos indices de actuales en actual
'''