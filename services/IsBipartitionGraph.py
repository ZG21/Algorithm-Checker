import logging

logger = logging.getLogger("myapp")
logging.basicConfig(level=logging.INFO)
# Inicializar conjuntos y un conjunto para llevar registro de los nodos visitados
componentes = []
set1, set2, visited, componente = set(), set(), set(), set()
# Aca funciones para revisar si un grafo es conexo o disconexo y devolver las componentes
def convertir_a_lista_de_adyacencia(graph):
    lista_adyacencia = {node['id']: [] for node in graph['nodes']}
    for edge in graph['edges']:
        lista_adyacencia[edge['source']].append(edge['target'])
        # Asumiendo un grafo no dirigido:
        lista_adyacencia[edge['target']].append(edge['source'])
    return lista_adyacencia
# DFS1 esta realizando la operacion que me devuelve las componentes del grafo
# es decir los subgrafos
def dfs1(node, graph, visited, component):
    visited.add(node)
    component.append(node)
    for neighbour in graph.get(node, []):
        if neighbour not in visited:
            dfs1(neighbour, graph, visited, component)

def is_bipartite_dfs(node, graph, color, c, set1, set2):
    if node in color:
        return color[node] == c
    color[node] = c
    if c:
        set1.add(node)
    else:
        set2.add(node)
    for neighbour in graph.get(node, []):
        if not is_bipartite_dfs(neighbour, graph, color, not c, set1, set2):
            return False
    return True

def find_components_and_check_bipartite(graph):
    visited = set()
    components = []
    color = {}
    sets = []  # Lista para almacenar los conjuntos de nodos bipartitos
    is_bipartite = True

    for node in graph:
        if node not in visited:
            component = []
            set1, set2 = set(), set()  # Conjuntos para los dos "colores"
            dfs1(node, graph, visited, component)
            components.append(component)
            if not is_bipartite_dfs(node, graph, color, True, set1, set2):
                is_bipartite = False
                break  # Un componente no bipartito es suficiente para detener el proceso
            sets.append([set1, set2])  # Agregar los conjuntos de este componente

    return components, is_bipartite, sets
# Fin funciones conexo/disconexo

def updateNodeStyles(graph, set1, set2):
    # Iterar a través de todos los nodos en el grafo
    logger.info(f"conjuntos : {set1} :: {set2}")
    for node in graph["nodes"]:
        # Determinar el conjunto al que pertenece el nodo
        if node["id"] in set1:
            # Asegurar que la propiedad 'style' existe
            if 'style' not in node:
                node['style'] = {}
            # Establecer el color de fondo y el color del borde a rojo para el conjunto 1
            node['style']['backgroundColor'] = 'red'
            node['style']['borderColor'] = 'red'
        elif node["id"] in set2:
            # Asegurar que la propiedad 'style' existe
            if 'style' not in node:
                node['style'] = {}
            # Establecer el color de fondo y el color del borde a verde para el conjunto 2
            node['style']['backgroundColor'] = 'green'
            node['style']['borderColor'] = 'green'
        return graph