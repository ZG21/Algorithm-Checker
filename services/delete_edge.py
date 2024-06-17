import copy
def delete_edge(lista_adyacencia, componente):
    copy_lista_adyacencia = copy.deepcopy(lista_adyacencia)
    for key, values in copy_lista_adyacencia.items():
        if key == componente[0][0]:
            if componente[1][0] in values:
                values.remove(componente[1][0])
    return copy_lista_adyacencia