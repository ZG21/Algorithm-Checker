import copy
def delete_edge(lista_adyacencia, componente):
    copy_lista_adyacencia = copy.deepcopy(lista_adyacencia)
    for key, values in copy_lista_adyacencia.items():
        if key == componente[0][0]:
            if componente[1][0] in values:
                values.remove(componente[1][0])
    return copy_lista_adyacencia


def eliminar_duplicados(lista):
    lista_sin_duplicados = []
    edges_ya_vistos = set()

    for d in lista:
        # Convertir las listas internas de 'Edge' en tuplas para que sean hashables
        edge_tuple = tuple(map(tuple, d['Edge']))

        if edge_tuple not in edges_ya_vistos:
            # Añadir el Edge al conjunto de vistos
            edges_ya_vistos.add(edge_tuple)
            # Añadir el elemento original a la lista sin duplicados
            lista_sin_duplicados.append(d)

    return lista_sin_duplicados