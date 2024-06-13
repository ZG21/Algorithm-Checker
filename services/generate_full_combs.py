
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