import copy

def unir_listas_ordenadas(lista1, lista2):
    lista_unida = []
    for i in range(len(lista1)):
        nueva_sublista = []
        if '0' not in lista1[i]:
            nueva_sublista.extend(lista1[i])
        if '0' not in lista2[i]:
            nueva_sublista.extend(lista2[i])
        nueva_sublista.sort()  # Ordenar alfabéticamente
        lista_unida.append(nueva_sublista)
    return lista_unida

def get_actuals_to_evaluate(componente, entry):
    actuals = []
    position_rest = []
    for key, value in entry.items():
        if key not in componente[1]:
            actuals.insert(0, value["position"])
        else:
            position_rest.append(value["position"])
    if len(actuals) == 0:
        actuals.append("0")
    return actuals, position_rest


def get_actuals_to_marginalize(componente, entry):
    position_rest = []
    actuals = []
    for key, value in entry.items():
        if key in componente[1]:
            actuals.insert(0, value["position"])
        else:
            position_rest.insert(0, value["position"])
    if len(actuals) == 0:
        actuals.append("0")
    return actuals, position_rest


def get_futures_to_evaluate(componente, entry):
    futures = {}
    for key, value in entry.items():
        if key in componente[0]:
            futures[key] = value
    return futures


def sumar_vectores(vector1, vector2):
    if len(vector1) != len(vector2):
        raise ValueError("Los vectores deben tener el mismo tamaño")
    vector_suma = []
    for i in range(len(vector1)):
        vector_suma.append((vector1[i] + vector2[i]) / 2)
    return vector_suma


def generar_parejas_vacio(arr, vacios, estado):
    for elem in arr:
        if estado == "actual":
            pareja1 = [["0"], [elem]]
            if pareja1 not in vacios:
                vacios.append(pareja1)
        if estado == "futuro":
            pareja2 = [[elem], ["0"]]
            if pareja2 not in vacios:
                vacios.append(pareja2)
    return vacios


def marginalize_matrix(matrix, position):
    pos = int(position)
    new_matrix = {}
    for key, value in matrix.items():
        clon_comb = copy.deepcopy(value['combinaciones'])
        nuevas_combinaciones = []
        nuevos_valores = []
        next_position = 2 ** pos
        evaluated_positions = []
        for i in range(len(clon_comb)):
            if i not in evaluated_positions and i + next_position < len(clon_comb):
                nueva_comb = clon_comb[i][:pos] + clon_comb[i][pos + 1:]
                nuevas_combinaciones.append(nueva_comb)
                evaluated_positions.append(i)
                evaluated_positions.append(i + next_position)
                nuevos_valores.append(sumar_vectores(value['valores'][i], value['valores'][i + next_position]))
            elif i == len(clon_comb) - 1:
                new_matrix[key] = {"combinaciones": nuevas_combinaciones, "valores": nuevos_valores,"position": value['position']}
    print(f"MATRIX MARGINALIZADA", new_matrix)
    return new_matrix


def marginalizar_vacios(component, entry):
    for key, value in entry.items():
        result = {}
        if key == component[0][0]:
            v0 = 0
            v1 = 0
            val = []
            for idx in range(0, len(value["valores"])):
                v0 = v0 + value["valores"][idx][0]
                v1 = v1 + value["valores"][idx][1]
            val.append([v0 / len(value["valores"]), v1 / len(value["valores"])])
            result["componente"] = component
            result["resultado"] = {key: {"combinaciones": [], "valores": val}}
    return result


def generar_combinaciones(array):
    def backtrack(start, path):
        # Agregar la combinación actual a los resultados
        combinaciones.append(path)
        # Generar todas las combinaciones posibles comenzando desde 'start'
        for i in range(start, len(array)):
            backtrack(i + 1, path + [array[i]])
    combinaciones = []
    backtrack(0, [])
    return combinaciones[1:]  # Excluir la combinación vacía


def search_component_in_memory(memory, component):
    for element in memory:
        if element['componente'] == component:
            return element
    return {}

def calculate_cost_component(component, componente_original, new_entry, memory, state,entrada):
    print(f"--------------componente {component} {componente_original}----------------------------")
    #print(f"--------------new entry {new_entry}----------------------------")
    result_empty = {}
    pos_res = []
    subsetMarginalized = {}
    future_to_eval = {}
    actual_position_to_omit1, pos_res = [], []
    actuals_, pos_r = [], []
    comp_mat = {}
    expancion = {}
    result_actual_empty = {}
    expand_result_act = {}
    combsSubset = []
    resultado_comp = {}
    result_comple = {}
    cop_unido = []
    combinado = []
    component_in_memory = {}
    complement = []
    complement_in_memory = {}
    result_prod_tensor = {}
    component_prodTensor_in_memory = {}
    sorted_subarrays = []
    # Componente no esta en la memoria
    component_in_memory = search_component_in_memory(memory, component)
    print(f"CALC-COMPONENT-MEMO: {component_in_memory}\n")
    if len(component_in_memory) == 0:
        # Tomamos las tablas futuras a evaluar y los actuales a marginalizar en la tabla
        future_to_eval = get_futures_to_evaluate(component, new_entry)
        actual_position_to_omit1, pos_res = get_actuals_to_marginalize(component, new_entry)
        # Componenetes de un solo elemento
        if len(component[0]) == 1 and len(component[1]) == 1:
            # Cuando la componente futuro es vacio
            if component[0][0] == "0":
                actuals_, pos_r = get_actuals_to_evaluate(componente, entrada)
                future_to_eval = get_futures_to_evaluate(componente, entrada)
                print(f"WHEN 0 EN FUT future_to_eval { future_to_eval} \n actuals_ {actuals_} \n new_entry {new_entry} \n")
                for pos in actuals_:
                    if len(comp_mat) == 0:
                        comp_mat = marginalize_matrix(future_to_eval, pos)
                    else:
                        comp_mat = marginalize_matrix(comp_mat, pos)
                expancion = expand_matrix(comp_mat, entrada, pos_r)
                print(f"COMP ORG M_EXPAND componen_original: {componente_original} \n m_expand: {expancion} \n")
                result_empty = {"componente": component, "resultado": expancion}
            # Cuando la componente actual es vacio
            elif component[1][0] == "0":
                result_actual_empty = marginalizar_vacios(component, future_to_eval)
                print(f"WHEN 0 IN ACT result_actual_empty {result_actual_empty}")
                expand_result_act = expand_matrix(result_actual_empty["resultado"], future_to_eval, pos_res)
                print(f"COMP ORG M_EXPAND componen_original: {result_actual_empty} \n m_expand: {expand_result_act} \n")
                result_empty = expand_result_act
            else:
                # Cuando la componente actual y fututo tiene 1 valor
                for p in actual_position_to_omit1:
                    if len(subsetMarginalized) == 0:
                        subsetMarginalized = marginalize_matrix(future_to_eval, p)
                    else:
                        subsetMarginalized = marginalize_matrix(subsetMarginalized, p)
                m_expand = expand_matrix(subsetMarginalized, future_to_eval, pos_res)
                result_empty = {"componente": component, "resultado": m_expand}
        # Cuando alguna de las componentes tiene mas de un valor
        else:
            combsSubset = generate_full_combs(component)
            print("PEW PEW", combsSubset)
            # para las componentes con mas de un elemento sacamos sus subcomponetes y los calculamos
            for element in combsSubset:
                # Buscampos la componente en la memoria
                component_in_memory = search_component_in_memory(memory, element)
                complement = obtener_complemento(component, element)
                if (complement[0][0] == "0") or (complement[1][0] == "0"):
                    if len(complement[0])>1 or len(complement[1])>1:
                        print("IN COMPONENTE", element, f"Y COMPLENTO {complement} NO SE PUEDEN COMO CORTE")
                    else:
                        # SI la subcomponente NO esta en la memoria se calcula y se guarda
                        if len(component_in_memory) == 0:
                            r_comp = calculate_cost_component(element, component, extended_matrix, memory, state,entrada)
                            resultado_comp = r_comp
                            memory.append(resultado_comp)
                        else:
                            resultado_comp = component_in_memory
                        # Para cada subcomponente le bucamos el valor de su complemento o o calculamos si no esta
                        complement_in_memory = search_component_in_memory(memory, complement)
                        if len(complement_in_memory) == 0:
                            print("COMPLE NO ESTA")
                            print(f"memory {memory}\n comple {complement} elem {element} subsar {complement_in_memory}")
                            result = calculate_cost_component(complement, componente_original, extended_matrix, memory, state,entrada)
                            memory.append(result)
                            result_comple = result
                        else:
                            result_comple = complement_in_memory
                        result_prod_tensor = producto_tensor(resultado_comp, result_comple)
                        component_prodTensor_in_memory = search_component_in_memory(memory, result_prod_tensor["componente"])
                        print(F"PROD TENSOR ESTA EN MEMORY len(component_prodTensor_in_memory): { len(component_prodTensor_in_memory)} \n result_prod_tensor: {result_prod_tensor}")
                        if len(component_prodTensor_in_memory) == 0:
                            memory.append(result_prod_tensor)
                            result_empty = result_prod_tensor
                        else:
                            # TOMAMOS EL ELEMENTO EN MEMORIA
                            key_memory = next(iter(component_prodTensor_in_memory['resultado']))
                            print("CALC KEY IN MEMORY", key_memory)
                            memory_element = component_prodTensor_in_memory["resultado"][key_memory]
                            position_state = memory_element["combinaciones"].index(state)
                            value_memo = sum(memory_element["valores"][position_state])
                            value_result_comp = sum(result_prod_tensor["resultado"][key_memory]["valores"][position_state])
                            if value_memo > value_result_comp:
                                memory.remove(component_prodTensor_in_memory)
                                memory.append(result_prod_tensor)
                                result_empty = result_prod_tensor
                            else:
                                result_empty = component_prodTensor_in_memory
                        # Producto tensor entre componente y complemento
                        # Validar si el componente del producto tensor esta en memoria SI->guarda menor NO ->Guarda valor
                        # Result empty va a ser el menor entre el prod tensor y el valor de ese producto en la memoria
    # El elemento esta en la memoria
    else:
        # Cuando la componente esta en la memoria, calcula el complemento
        complement = obtener_complemento(componente_original, component)
        print("SI ESTA EL VALOR AHORA SU COMPLEM", complement, "COMP ORI", componente_original)
        complement_in_memory = search_component_in_memory(memory, complement)
        if len(complement_in_memory) == 0:
            print("COMPLE NO ESTA")
            result = calculate_cost_component(complement, componente_original, extended_matrix, memory, state,entrada)
            memory.append(result)
            result_comple = result
            result_prod_tensor = producto_tensor(resultado_comp, result_comple)
            component_prodTensor_in_memory = search_component_in_memory(memory, result_prod_tensor["componente"])
            print(f"COM ESTA EN MEMORY component_prodTensor_in_memory: {component_prodTensor_in_memory}")
            if len(component_prodTensor_in_memory) == 0:
                memory.append(result_prod_tensor)
                result_empty = result_prod_tensor
            else:
                # TOMAMOS EL ELEMENTO EN MEMORIA
                key_memory = next(iter(component_prodTensor_in_memory['resultado']))
                print("KEY IN MEMORY", key_memory)
                memory_element = component_prodTensor_in_memory["resultado"][key_memory]
                position_state = memory_element["combinaciones"].index(state)
                value_memo = sum(memory_element["valores"][position_state])
                value_result_comp = sum(result_prod_tensor["resultado"][key_memory]["valores"][position_state])
                if value_memo > value_result_comp:
                    memory.remove(component_prodTensor_in_memory)
                    memory.append(result_prod_tensor)
                    result_empty = result_prod_tensor
                else:
                    result_empty = component_prodTensor_in_memory
        else:
            result_comple = complement_in_memory
            result_comple_memory = search_component_in_memory(memory, result_comple["componente"])
            if len(result_comple_memory) == 0:
                result = calculate_cost_component(complement, componente_original, extended_matrix, memory, state,entrada)
                memory.append(result)
                result_empty = result
            else:
                result_empty = result_comple_memory
    print(f"EMPTY RESULT result_empty: {result_empty}")
    return result_empty
    # Obtenemos el valor segun el estado para el complemento y el componente
    # Hacemos prod tensor complemento y componente en ese estado
    # (NO SE) Hacemos EMD con la extended matrix en ese estado

# TODO Ortanizar el código en funciones separadas

def generate_full_combs(component):
    numeradores = generar_combinaciones(component[0])
    denominadores = generar_combinaciones(component[1])
    full_comb = []
    vacios_actuales = []
    vacios_futuros = []
    for comb in numeradores:
        for comb2 in denominadores:
            if len(comb) > 1:
                vacios_futuros = generar_parejas_vacio(comb, vacios_futuros, "futuro")
            if len(comb2) > 1:
                vacios_actuales = generar_parejas_vacio(comb2, vacios_actuales, "actual")
            if not (comb == component[0] and comb2 == component[1]):
                full_comb.append([comb, comb2])
    full_comb.extend(vacios_actuales)
    full_comb.extend(vacios_futuros)
    return full_comb


def obtener_complemento(componente_original, subcomponente):
    complemento = []
    for original, sub in zip(componente_original, subcomponente):
        # Encontrar elementos en original que no están en sub
        elementos_complemento = [elemento for elemento in original if elemento not in sub]
        # Si el resultado está vacío, agregar "0"
        if not elementos_complemento:
            elementos_complemento = ["0"]
        complemento.append(elementos_complemento)
    return complemento


def expand_matrix(matrix_marginalized, matrix_original, positions_rest):
    copy_matrix_original = {}
    copy_matrix_marginalized = {}
    print(f"EXPAND MAT matrix_marginalized {matrix_marginalized} \n matrix_original {matrix_original} \n positions_rest {positions_rest}")
    # Recorrer la matriz marginalizada
    for key, value in matrix_marginalized.items():
        # Tomamos de la entrada anterior a la matriz marginalizada como matriz original
        # tomando tambien las tablas que coinciden con nuestra matriz marginalizada
        if key in matrix_original:
            copy_matrix_original = copy.deepcopy(matrix_original[key])
            # Recorremos las combinaciones de nuestra MM
            if len(value["combinaciones"]) == 0:
                result = {}
                result["componente"] = [[key], ["0"]]
                result["resultado"] = {key: {"combinaciones": matrix_original[key]["combinaciones"],"valores": matrix_marginalized[key]["valores"] * len(matrix_original[key]["combinaciones"])}}
                return result
            else:
                for idx in range(0, len(value["combinaciones"])):
                    comb_marginalized = value["combinaciones"][idx]
                    # Recorremos tambien las combinaciones de nuestra Matriz original
                    for idx2 in range(0, len(matrix_original[key]["combinaciones"])):
                        comb_original = matrix_original[key]["combinaciones"][idx2]
                        # Solo en el momento que encuentre que los elementos de MM[idx] son iguales a los de nuestra Mo[idx2]
                        # cambiamos su valor en MO[idx2] por el del valor de la MM[idx]
                        val = True
                        for pos in positions_rest:
                            for element in comb_marginalized:
                                if element != comb_original[pos]:
                                    val = False
                        if val == True:
                            copy_matrix_original["valores"][idx2] = value["valores"][idx]
                        copy_matrix_marginalized[key] = copy_matrix_original
    return copy_matrix_marginalized


def obtener_keys_tensor(matrix_a, matrix_b):
    full_key= ""
    print(f"OBTENER KEYS")
    for key in matrix_a["resultado"].keys():
        print("KEY A", key)
        if key not in full_key:
            full_key += key
    for key in matrix_b["resultado"].keys():
        print("KEY B", key)
        if key not in full_key:
            full_key += key
    print("FULL KEY", full_key)
    return sorted(full_key)


def producto_tensor(matrix_a, matrix_b):
    print(f"PROD TENSOR matrix_a:{matrix_a} \n matrix_b: {matrix_b}")
    componente_unido = []
    full_keys = ''.join(obtener_keys_tensor(matrix_a, matrix_b))
    for comp1, comp2 in zip(matrix_a['componente'], matrix_b['componente']):
        # Filtrar los elementos que son ceros
        combi = [x for x in comp1 + comp2 if x != '0']
        print("PROD TENSOR COMBI", combi)
        componente_unido.append(combi)
    sorted_subarrays = [sorted(comp) for comp in componente_unido]
    print("COMPONENTE UNIDO", sorted_subarrays)
    key_matrix_a = next(iter(matrix_a['resultado']))
    key_matrix_b = next(iter(matrix_b['resultado']))
    combinaciones = matrix_a["resultado"][key_matrix_a]["combinaciones"]
    new_val = []
    print("COMBINACIONES", combinaciones)
    for idx in range(0, len(combinaciones)):
        value_mat_a = matrix_a["resultado"][key_matrix_a]["valores"][idx]
        value_mat_b = matrix_b["resultado"][key_matrix_b]["valores"][idx]
        v0 = value_mat_a[0] * value_mat_b[0]
        v1 = value_mat_a[1] * value_mat_b[1]
        new_val.append([v0, v1])
    result = {}
    result["componente"] = sorted_subarrays
    # Ordenar los caracteres
    sorted_chars = sorted([key_matrix_a, key_matrix_b])
    # Unir los caracteres
    key_sorted = ''.join(sorted_chars)
    result["resultado"] = {full_keys: {"combinaciones": combinaciones, "valores": new_val}}
    return result


def filtrar_componentes_repetidos(datos):
    componentes_vistos = set()
    datos_filtrados = []
    for item in datos:
        componentes_tuple = tuple(map(tuple, item['componente']))
        if componentes_tuple not in componentes_vistos:
            componentes_vistos.add(componentes_tuple)
            datos_filtrados.append(item)
    return datos_filtrados

def tensor_full_mat(matrix, componente):
    print("TENSOR FULL MAT", matrix)
    full_values = []
    first_key = next(iter(matrix))
    full_cominaciones = matrix[first_key]['combinaciones']
    for key, value in matrix.items():
        if len(full_values) == 0:
            full_values = value["valores"]
        else:
            for idx in range(0,len(full_cominaciones)):
                v0 = value["valores"][idx][0] * full_values[idx][0]
                v1 = value["valores"][idx][1] * full_values[idx][1]
                full_values[idx] = [v0,v1]
                print(f"VALUES v0: {v0} v1: {v1}")
        print(f"FULL VALUES {full_values}")
    print(f"Jeronimmo full_combs {full_cominaciones}")
entrada = {
    "a": {
        "combinaciones": [[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1]],
        "valores": [[0, 1], [1, 0], [0, 1], [1, 0], [1, 0], [0, 1], [1, 0], [1, 0]],
        "position": 0
    },
    "b": {
        "combinaciones": [[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1]],
        "valores": [[0, 1], [1, 0], [0, 1], [1, 0], [1, 0], [0, 1], [0, 1], [1, 0]],
        "position": 1
    },
    "c": {
        "combinaciones": [[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1]],
        "valores": [[0, 1], [1, 0], [0, 1], [0, 1], [1, 0], [1, 0], [1, 0], [1, 0]],
        "position": 2
    }
}
# Componente ab/ab
componente = [["a", "b"], ["a", "b"]]
futures_to_evaluate = {}
component_matrix = {}
state = [0, 0, 0]
futures_to_evaluate = get_futures_to_evaluate(componente, entrada)
actual_position_to_omit, pos_r = get_actuals_to_evaluate(componente, entrada)
for pos in actual_position_to_omit:
    if len(component_matrix) == 0:
        component_matrix = marginalize_matrix(futures_to_evaluate, pos)
    else:
        component_matrix = marginalize_matrix(component_matrix, pos)
extended_matrix = expand_matrix(component_matrix, entrada, pos_r)
tensor_full_mat(extended_matrix, componente)
# combs = generate_full_combs(componente)
# print("FULL COMBS", combs)
# memory = []
# print(f"EXTENDED MAT: {extended_matrix}\n")

# for element in combs:
#     # Obtenemos el componente
#     memory = filtrar_componentes_repetidos(memory)
#     subset_in_memory = search_component_in_memory(memory, element)
#     # Obtenemos el complemento
#     complement = obtener_complemento(componente, element)
#     complementSubset_in_memory = search_component_in_memory(memory, subset_in_memory)
#     # SI el complemento cumple estas condiciones de genera una k-particion
#     if not ((len(complement[0])>1 and (complement[0][0] == "0")) or (len(complement[1])>1 and (complement[1][0] == "0"))):
#         if len(subset_in_memory) == 0:
#             result_subcomponent = calculate_cost_component(element, componente, extended_matrix, memory, state, entrada)
#             memory.append(result_subcomponent)
#             result_comple_memory = {}
#             if len(complementSubset_in_memory) == 0:
#                 result_subcomplement = calculate_cost_component(complement, componente, extended_matrix, memory, state, entrada)
#                 result_subcomplement_in_memory = search_component_in_memory(memory,result_subcomplement["componente"])
#                 if len(result_subcomplement_in_memory) == 0:
#                     memory.append(result_subcomplement)
#                     result_comple_memory = result_subcomplement
#                 else:
#                     result_comple_memory = result_subcomplement_in_memory
#             else:
#                 result_comple_memory = complementSubset_in_memory
#             #Proceso para EMD
#             #Producto tensor entre las componen
#             print("RESULT EMD", result_comple_memory, "\n componente", result_subcomponent)
#             print("MEMORY:", memory)
#             print(f"MOMO !!!! Component {result_subcomponent}\nComplement {result_subcomplement}")
#     # producto_tensor(result_subcomponent,result_complement)
#     # # Obtenemos el valor segun el estado para el complemento y el componente
#     # # Hacemos prod tensor complemento y componente en ese estado
#     # # Hacemos EMD con la extended matrix en ese estado

# print("MEMORIA:", memory)