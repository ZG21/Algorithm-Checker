import copy
def sumar_vectores(vector1, vector2):
    if len(vector1) != len(vector2):
        raise ValueError("Los vectores deben tener el mismo tamaño")
    vector_suma = []
    for i in range(len(vector1)):
        vector_suma.append((vector1[i] + vector2[i]) / 2)
    return vector_suma


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