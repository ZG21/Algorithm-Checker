def filtrar_componentes_repetidos(datos):
    componentes_vistos = set()
    datos_filtrados = []
    for item in datos:
        componentes_tuple = tuple(map(tuple, item['componente']))
        if componentes_tuple not in componentes_vistos:
            componentes_vistos.add(componentes_tuple)
            datos_filtrados.append(item)
    return datos_filtrados