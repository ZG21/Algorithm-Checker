import copy


def expand_matrix(matrix_marginalized, matrix_original, positions_rest):
    copy_matrix_original = {}
    copy_matrix_marginalized = {}
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