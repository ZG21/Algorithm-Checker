import copy
def obtener_keys_tensor(matrix_a, matrix_b):
    full_key= ""
    print(f"OBTENER KEYS")
    for key in matrix_a.keys():
        print("KEY A", key)
        if key not in full_key:
            full_key += key
    for key in matrix_b.keys():
        print("KEY B", key)
        if key not in full_key:
            full_key += key
    print("FULL KEY", full_key)
    return sorted(full_key)


def producto_tensor(matrix_a, matrix_b):
    print(f"PROD TENSOR matrix_a:{matrix_a} \n matrix_b: {matrix_b}")
    componente_unido = []
    full_keys = ''.join(obtener_keys_tensor(matrix_a["resultado"], matrix_b["resultado"]))
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


def tensor_subset(subset, full_combinaciones):
    key_full_tensor_mat = ""
    full_values= []
    subset_list = list(subset.items())
    for i in range(len(subset_list)):
        key, value = subset_list[i]
        matrix_a = {key:value}
        if i + 1 < len(subset_list):
            next_key, next_value = subset_list[i + 1]
            matrix_b= {next_key:next_value}
            key_full_tensor_mat += "".join(obtener_keys_tensor(matrix_a,matrix_b))
        print(f"KEY TENSOR_SUBSET: {key_full_tensor_mat+key} ------")
        if len(full_values) == 0:
            full_values = value["valores"]
        else:
            for idx in range(0,len(full_combinaciones)):
                v0 = value["valores"][idx][0] * full_values[idx][0]
                v1 = value["valores"][idx][1] * full_values[idx][1]
                full_values[idx] = [v0,v1]
        print(f"FULL VALUES {full_values}")
    return {key_full_tensor_mat:{"combinaciones": full_combinaciones, "valores": full_values  }}


def tensor_full_mat(subset,componente, original_entry):
    result_tensor_subset = {}
    key_full_tensor_mat = ""
    first_key = next(iter(subset))
    full_combinaciones = subset[first_key]['combinaciones']
    rest_original_entry = copy.deepcopy(original_entry)
    # Obtiene las tablas sin afectar de la tabla original
    for element in componente[0]:
        if element in rest_original_entry.keys():
            del rest_original_entry[element]
    # Producto Tensor de las tablas de nuestro subsistema
    result_tensor_subset = tensor_subset(subset,full_combinaciones)
    for key, value in rest_original_entry.items():
        result_tensor_subset[key] = value
        result_tensor_subset = tensor_subset(result_tensor_subset,full_combinaciones)
    return {"componente":componente, "resultado": result_tensor_subset}

def vector_to_emd(matrix, state):
    vector_result = []
    for key, value in matrix.items():
        print(f"VALUE value: {value}")
        idx = value["combinaciones"].index(state)
        vector_result = value["valores"][idx]
    return vector_result
 # Obtenemos el componente