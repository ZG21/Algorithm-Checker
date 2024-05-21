from cut_value_calculator import cut_value_calculator
from services.procesoProbabilistico import procesar_matriz, TMP, multiplicar_vectores, earth_mover_distance, combine_and_sort_keys,state_To_Compare
def add_subsets(key, values, current_subsets, lista_adyacencia, position_dict, estado_actual):

    lista_adyacencia_actual = {k: v for k, v in lista_adyacencia.items() if len(v) > 0}

    if not values:
        actuales = cut_value_calculator([key, '0'], lista_adyacencia_actual, 0,position_dict)["actual"].values()
        actualesR = cut_value_calculator([key, '0'], lista_adyacencia_actual, 0,position_dict)["actual_rest"].values()
        futuros = cut_value_calculator([key, '0'], lista_adyacencia_actual, 0, position_dict)["future"].values()
        futurosR = cut_value_calculator([key, '0'], lista_adyacencia_actual, 0, position_dict)["future_rest"].values()
        matriz_marginalizada = procesar_matriz(TMP,actuales,futuros)
        matriz_marginalizada_restante = procesar_matriz(TMP, actualesR, futurosR)
        matrix, costo = multiplicar_vectores(matriz_marginalizada, matriz_marginalizada_restante)
        matrix = costo,combine_and_sort_keys(matrix)
        estado_a_comparar = []
        for element in matrix[1]:
            if element["actual"] == estado_actual:
                estado_a_comparar.append(element)

        estado_original = state_To_Compare(TMP,estado_actual)
        costo = earth_mover_distance(estado_a_comparar,estado_original)
        result = cut_value_calculator([key, '0'], lista_adyacencia_actual, 0,position_dict)
        result["costo"] = costo
        current_subsets.append(result)
        return current_subsets
    actuales = cut_value_calculator([key, '0'], lista_adyacencia_actual, 0, position_dict)["actual"].values()
    actualesR = cut_value_calculator([key, '0'], lista_adyacencia_actual, 0, position_dict)["actual_rest"].values()
    futuros = cut_value_calculator([key, '0'], lista_adyacencia_actual, 0, position_dict)["future"].values()
    futurosR = cut_value_calculator([key, '0'], lista_adyacencia_actual, 0, position_dict)["future_rest"].values()
    matriz_marginalizada = procesar_matriz(TMP, actuales, futuros)
    matriz_marginalizada_restante = procesar_matriz(TMP, actualesR, futurosR)
    matrix, costo = multiplicar_vectores(matriz_marginalizada, matriz_marginalizada_restante)
    matrix = costo, combine_and_sort_keys(matrix)
    estado_a_comparar = []
    for element in matrix[1]:
        if element["actual"] == estado_actual:
            estado_a_comparar.append(element)

    estado_original = state_To_Compare(TMP, estado_actual)
    costo = earth_mover_distance(estado_a_comparar, estado_original)
    result = cut_value_calculator([key, '0'], lista_adyacencia_actual, 0, position_dict)
    result["costo"] = costo
    current_subsets.append(result)
    def add_values(idx, inside_subset):
        if idx == len(values):
            if inside_subset:
                subsetAlgo = [key] + inside_subset
                actuales = cut_value_calculator(subsetAlgo, lista_adyacencia_actual, 0, position_dict)[
                    "actual"].values()
                actualesR = cut_value_calculator(subsetAlgo, lista_adyacencia_actual, 0, position_dict)[
                    "actual_rest"].values()
                futuros = cut_value_calculator(subsetAlgo, lista_adyacencia_actual, 0, position_dict)["future"].values()
                futurosR = cut_value_calculator(subsetAlgo, lista_adyacencia_actual, 0, position_dict)[
                    "future_rest"].values()
                matriz_marginalizada = procesar_matriz(TMP, actuales, futuros)
                matriz_marginalizada_restante = procesar_matriz(TMP, actualesR, futurosR)
                matrix, costo = multiplicar_vectores(matriz_marginalizada, matriz_marginalizada_restante)
                matrix = costo, combine_and_sort_keys(matrix)
                estado_a_comparar = []
                for element in matrix[1]:
                    if element["actual"] == estado_actual:
                        estado_a_comparar.append(element)

                estado_original = state_To_Compare(TMP, estado_actual)
                result = cut_value_calculator(subsetAlgo, lista_adyacencia_actual, 0, position_dict)

                costo = earth_mover_distance(estado_a_comparar, estado_original)

                result["costo"] = costo
                current_subsets.append(result)
            return current_subsets
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