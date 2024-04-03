import logging

logger = logging.getLogger("myapp")
logging.basicConfig(level=logging.INFO)
# Inicializar conjuntos y un conjunto para llevar registro de los nodos visitados
set1, set2, visited = set(), set(), set()

def dfs(node, current_set,graph):
    # Marcar el nodo como visitado
    visited.add(node)
    # Agregar el nodo al conjunto actual
    current_set.add(node)
    # Determinar el conjunto opuesto
    opposite_set = set2 if current_set is set1 else set1
    # Recorrer todos los nodos adyacentes
    for neighbour in graph.get(node, []):
        # Si el vecino no ha sido visitado, aplicar DFS recursivamente
        if neighbour not in visited:
            dfs(neighbour, opposite_set,graph)
    return {"Conjunto 1": set1, "Conjunto 2":set2}
def isBipartitionGraph(g):
    # Convertir la lista de aristas en un diccionario para facilitar la búsqueda de adyacencias
    graph = {}
    resps = []
    for edge in g["edges"]:
        graph.setdefault(edge['source'], []).append(edge['target'])
        graph.setdefault(edge['target'], []).append(edge['source'])
    # Aplicar DFS a cada nodo no visitado
    for node in g["nodes"]:
        if node['id'] not in visited:
            resps.append(dfs(node['id'], set1, graph))
    updateNodeStyles(g,set1,set2)
    return {"resp":resps, "graph": updateNodeStyles(g,set1,set2)}


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