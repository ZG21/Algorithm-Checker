from typing import Union
from fastapi import FastAPI
from services.IsBipartitionGraph import find_components_and_check_bipartite,convertir_a_lista_de_adyacencia
from services.Subsets import separar_dict_y_crear_posiciones
from services.procesoProbabilistico import cut_edge_calculator, procesar_matriz,TMP,earth_mover_distance,state_To_Compare,multiplicar_vectores,combine_and_sort_keys


from services.Subsets import add_subsets

import logging
from GraphsExaples import graph1
from itertools import product

logger = logging.getLogger("myapp")
logging.basicConfig(level=logging.INFO)

app = FastAPI()

def generatorComb(n):
    # Generar todas las combinaciones binarias de longitud n
    combinaciones = list(product([0, 1], repeat=n))
    # Crear la clave dinámica con letras del alfabeto
    clave = ",".join(chr(65 + i) for i in range(n))  # 65 es el código ASCII de 'A'
    # Formatear el resultado como un diccionario
    resultado = {
        clave: [list(combinacion) for combinacion in combinaciones]
    }
    return resultado

def generate_full_matrix(nodes_matrix, len_graph):
    # Extraer la matriz de combinaciones binarias
    var_matrix = list(var_matrix.values())[0]
    # Crear la matriz completa
    full_matrix = []
    # Iterar sobre cada matriz de nodos en nodes_matrix
    for node_key, node_matrix in nodes_matrix.items():
        if len(node_matrix) != len(var_matrix):
            raise ValueError(f"El tamaño de la matriz de nodos para '{node_key}' no coincide con el tamaño de var_matrix")
        # Crear filas combinando var_matrix con la matriz de nodos correspondiente
        for i in range(len(var_matrix)):
            full_matrix.append(var_matrix[i] + node_matrix[i])
    return full_matrix

@app.get("/bipartition-and-calculeProbality")
def IsBipartition():
    # estado_actual = {state: value}
    graph = dict()
    logger.info("Accediendo a la ruta raíz")
    graph = graph1
    logger.info(f"Marlon components graph : ")
    print(f"Jeronimo components graph : {graph1}")
    print(f"Jeronimo generate comb: {generatorComb(graph['nodesNumber'])}")
    var_matrix = generatorComb(graph['nodesNumber'])
    nodes_matrix = {
        "A": [[1,0],[0,1],[0,1],[0,1]],
        "B": [[1,0],[1,0],[0,1],[1,0]]
    }
    test = generate_full_matrix(nodes_matrix, graph['nodesNumber'])
    lista_adyacencia = convertir_a_lista_de_adyacencia(graph1)
    position_dict = separar_dict_y_crear_posiciones(lista_adyacencia)
    subsets = []
    subsets_iteration = []
    for key, values in lista_adyacencia.items():
        print(f"Jeronimo key: {key}")
        # subsets = add_subsets(key, values, subsets_iteration, lista_adyacencia,position_dict, estado_actual)
        #procesar_matriz(TMP,subsets_iteration.)

    # Función de comparación para ordenar por el valor de la llave "value"
    def comparar_por_valor(objeto):
        return objeto["costo"]

    # Ordenar la lista de objetos por el valor de la llave "value"
    subsetSorted = sorted(subsets, key=comparar_por_valor)
    cost_delete_edge = []
    #2 parte taller 3
    for element in subsetSorted:
        for key, val in element.items():
            if key == "subsets" and len(val) == 2 and val[1] != "0":

                cut_edge_calculator(val,lista_adyacencia,position_dict)
                actuales = cut_edge_calculator(val,lista_adyacencia,position_dict)[
                    "actual"]
                actualesR = cut_edge_calculator(val,lista_adyacencia,position_dict)[
                    "actual_rest"]
                futuros = cut_edge_calculator(val,lista_adyacencia,position_dict)["future"]
                futurosR = cut_edge_calculator(val,lista_adyacencia,position_dict)[
                    "future_rest"]
                matriz_marginalizada = procesar_matriz(TMP, actuales, futuros)
                matriz_marginalizada_restante = procesar_matriz(TMP, actualesR, futurosR)
                matrix, costo = multiplicar_vectores(matriz_marginalizada, matriz_marginalizada_restante)
                matrix = costo, combine_and_sort_keys(matrix)
                estado_a_comparar = []
                for element in matrix[1]:
                    if element["actual"] == estado_actual:
                        estado_a_comparar.append(element)

                estado_original = state_To_Compare(TMP, estado_actual)
                costo = earth_mover_distance(estado_a_comparar, estado_original)
                result2 = cut_edge_calculator(val,lista_adyacencia,position_dict)
                result2["costo"] = costo
                cost_delete_edge.append(result2)

    def comparar_por_valor(objeto):
        return objeto["costo"]

    # Ordenar la lista de objetos por el valor de la llave "value"
    Result_cost_edges_sorted = sorted(cost_delete_edge, key=comparar_por_valor)
    componentes, es_bipartito, sets = find_components_and_check_bipartite(lista_adyacencia)

    return {"Grafo": graph1["name"],
            "Es_Bipartito": es_bipartito,
            "Conjuntos_bipartition": sets,
            "Componentes/Subgrafos": componentes,
            "corte_minimo_costo": subsetSorted[0],
            "componentes": subsetSorted,
            "costo_eliminacion_edges": Result_cost_edges_sorted,

            }


@app.get("/eliminateEdge-and-calculeProbality/{state}/{value}")
def EliminateEdge(state: str, value: str):
    estado_actual = {state: value}
    graph = dict()
    graph = graph1
    lista_adyacencia = convertir_a_lista_de_adyacencia(graph1)
    position_dict = separar_dict_y_crear_posiciones(lista_adyacencia)
    subsets = []
    subsets_iteration = []
    for key, values in lista_adyacencia.items():
        subsets = add_subsets(key, values, subsets_iteration, lista_adyacencia, position_dict, estado_actual)

    def comparar_por_valor(objeto):
        return objeto["costo"]

    # Ordenar la lista de objetos por el valor de la llave "value"
    subsetSorted = sorted(subsets, key=comparar_por_valor)

    componentes, es_bipartito, sets = find_components_and_check_bipartite(lista_adyacencia)

    return {"Grafo": graph1["name"],
            "Es_Bipartito": es_bipartito,
            "Conjuntos_bipartition": sets,
            "Componentes/Subgrafos": componentes,
            "corte_minimo_costo": subsetSorted[0],
            "componentes": subsetSorted
            }

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/graphs")
def read_graph():
    graph = dict()
    logger.info("Accediendo a la ruta raíz")
    graph = {
        "name": "grafo 1",
        "nodes": [
            {"id": '1', "type": 'default', "data": {"label": ''}, "position": {"x": 100, "y": 50},
             "style": {"backgroundColor": 'red', "borderColor": 'red'}},
            {"id": '2', "type": 'default', "data": {"label": ''}, "position": {"x": 200, "y": 50}},
            {"id": '3', "type": 'default', "data": {"label": ''}, "position": {"x": 300, "y": 50},
             "style": {"backgroundColor": 'red', "borderColor": 'red'}},
            {"id": '4', "type": 'default', "data": {"label": ''}, "position": {"x": 100, "y": 150}},
            {"id": '5', "type": 'default', "data": {"label": ''}, "position": {"x": 300, "y": 150},
             "style": {"backgroundColor": 'red', "borderColor": 'red'}},
            {"id": '6', "type": 'default', "data": {"label": ''}, "position": {"x": 200, "y": 250}},
        ],
        "edges": [
            {"id": "e1-2", "source": "1", "target": "2"},
            {"id": "e2-3", "source": "2", "target": "3"},
            {"id": "e1-4", "source": "1", "target": "4"},
            {"id": "e4-6", "source": "4", "target": "6"},
            {"id": "e6-5", "source": "6", "target": "5"},
            {"id": "e5-3", "source": "5", "target": "3"},
            {"id": "e2-6", "source": "2", "target": "6"}
        ],
        "nodesNumber": 6,
        "isConnected": True,
        "isComplete": False,
        "isWeighted": False,
        "isDirected": False
    }
    return {"Graph": isBipartitionGraph(graph)}
