def add_combinations(key, values, current_combs):
    """
    Agrega todas las combinaciones posibles para una key dada y las agrega a la lista de combinaciones actuales.

    Argumentos:
    key (str): La key actual del diccionario.
    values (list): La lista de values asociada a la key.
    current_combs (list): La lista actual de combinaciones donde se agregarán las nuevas combinaciones.
    """
    # Si la lista de values está vacía, simplemente agregar la key con [0]
    if not values:
        current_combs.append([key, 0])
        return

    # Agregar la combinación de no elegir ningún valor
    current_combs.append([key, 0])

    # Función auxiliar para agregar recursivamente combinaciones de los values
    def add_values(idx, inside_comb):
        """
        Función auxiliar para agregar recursivamente combinaciones de los values.

        Argumentos:
        idx (int): El índice actual en la lista de values.
        inside_comb (list): La combinación actual de values para la key dada.
        """
        # Si el índice supera la longitud de values, agregar la combinación actual a current_combs
        if idx == len(values):
            # Solo si la combinación actual no está vacía, la agregamos a current_combs
            if inside_comb:
                current_combs.append([key] + inside_comb)
                print(f"IF INTERNO current_combs: {current_combs} inside_comb: {inside_comb}")
            return
        print(f"key: {key},\nvalues: {values},\ncurrent_combs: {current_combs},\nidx: {idx},\ninside_comb: {inside_comb}")
        print("----------------------------------------------------PRE---------------------------------------------------------------")
        # Agregar el valor actual al conjunto de combinación
        add_values(idx + 1, inside_comb + [values[idx]])
        # No agregar el valor actual, pasando al siguiente
        add_values(idx + 1, inside_comb)
        print(
            f"key: {key},\nvalues: {values},\ncurrent_combs: {current_combs},\nidx: {idx},\ninside_comb: {inside_comb}")
        print(
            "----------------------------------------------------POST---------------------------------------------------------------")
    # Iniciar la recursión
    print("INICIOOO")
    add_values(0, [])
    print("FINNNN")

def generate_combinations(diccionario):
    """
    Genera todas las combinaciones posibles a partir de un diccionario dado.

    Argumentos:
    diccionario (dict): El diccionario que contiene las keys y los values asociados.

    Retorna:
    list: Una lista de todas las combinaciones posibles generadas a partir del diccionario.
    """
    combinaciones_totales = []

    for key, values in diccionario.items():
        combinaciones_key = []
        add_combinations(key, values, combinaciones_key)
        combinaciones_totales.extend(combinaciones_key)
    return combinaciones_totales

