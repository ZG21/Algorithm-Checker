from typing import Union
from fastapi import FastAPI
from services.IsBipartitionGraph import find_components_and_check_bipartite,convertir_a_lista_de_adyacencia

from Subsets import add_subsets

import logging
from GraphsExaples import graph1

logger = logging.getLogger("myapp")
logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.get("/")
def IsBipartition():
    graph = dict()
    logger.info("Accediendo a la ruta raíz")
    graph = graph1
    logger.info(f"Marlon components graph : ")
    lista_adyacencia = convertir_a_lista_de_adyacencia(graph1)
    subsets = []
    print(f"El grafo, listas de adyacencia: {lista_adyacencia}")

    for key, values in lista_adyacencia.items():
        subsets_iteration = []
        add_subsets(key, values, subsets_iteration, graph)
        subsets.extend(subsets_iteration)
    print(f"Jeronimo Subsets {subsets}")
    # Encontrar componentes y verificar bipartición
    componentes, es_bipartito, sets = find_components_and_check_bipartite(lista_adyacencia)

    return {"Grafo": graph1["name"],
            "Es_Bipartito": es_bipartito,
            "Conjuntos_bipartition": sets,
            "Componentes/Subgrafos": componentes
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
array = []
def test(idx, obj_act, array):
    if len(array) == 0:
        return
    while obj_act == test[idx - 1]:
        test(ob_act)
    


[
    {"ABC": "000", "ABC'": "000", "value": 0},
    {"ABC": "000", "ABC'": "001", "value": 0},
    {"ABC": "000", "ABC'": "010", "value": 0},
    {"ABC": "000", "ABC'": "011", "value": 1},
    {"ABC": "000", "ABC'": "100", "value": 1},
    {"ABC": "000", "ABC'": "101", "value": 0},
    {"ABC": "000", "ABC'": "110", "value": 0},
    {"ABC": "000", "ABC'": "111", "value": 0},
    {"ABC": "001", "ABC'": "000", "value": 0},
    {"ABC": "001", "ABC'": "001", "value": 1},
    {"ABC": "001", "ABC'": "010", "value": 0},
    {"ABC": "001", "ABC'": "011", "value": 1},
    {"ABC": "001", "ABC'": "100", "value": 1},
    {"ABC": "001", "ABC'": "101", "value": 1},
    {"ABC": "001", "ABC'": "110", "value": 1},
    {"ABC": "001", "ABC'": "111", "value": 1},
    {"ABC": "010", "ABC'": "000", "value": 0},
    {"ABC": "010", "ABC'": "001", "value": 0},
    {"ABC": "010", "ABC'": "010", "value": 0},
    {"ABC": "010", "ABC'": "011", "value": 1},
    {"ABC": "010", "ABC'": "100", "value": 1},
    {"ABC": "010", "ABC'": "101", "value": 0},
    {"ABC": "010", "ABC'": "110", "value": 0},
    {"ABC": "010", "ABC'": "111", "value": 1},
    {"ABC": "011", "ABC'": "000", "value": 1},
    {"ABC": "011", "ABC'": "001", "value": 0},
    {"ABC": "011", "ABC'": "010", "value": 0},
    {"ABC": "011", "ABC'": "011", "value": 1},
    {"ABC": "011", "ABC'": "100", "value": 1},
    {"ABC": "011", "ABC'": "101", "value": 1},
    {"ABC": "011", "ABC'": "110", "value": 1},
    {"ABC": "011", "ABC'": "111", "value": 1},
    {"ABC": "100", "ABC'": "000", "value": 0},
    {"ABC": "100", "ABC'": "001", "value": 0},
    {"ABC": "100", "ABC'": "010", "value": 0},
    {"ABC": "100", "ABC'": "011", "value": 1},
    {"ABC": "100", "ABC'": "100", "value": 0},
    {"ABC": "100", "ABC'": "101", "value": 0},
    {"ABC": "100", "ABC'": "110", "value": 1},
    {"ABC": "100", "ABC'": "111", "value": 1},
    {"ABC": "101", "ABC'": "000", "value": 1},
    {"ABC": "101", "ABC'": "001", "value": 0},
    {"ABC": "101", "ABC'": "010", "value": 0},
    {"ABC": "101", "ABC'": "011", "value": 1},
    {"ABC": "101", "ABC'": "100", "value": 1},
    {"ABC": "101", "ABC'": "101", "value": 1},
    {"ABC": "101", "ABC'": "110", "value": 1},
    {"ABC": "101", "ABC'": "111", "value": 1},
    {"ABC": "110", "ABC'": "000", "value": 0},
    {"ABC": "110", "ABC'": "001", "value": 0},
    {"ABC": "110", "ABC'": "010", "value": 0},
    {"ABC": "110", "ABC'": "011", "value": 0},
    {"ABC": "110", "ABC'": "100", "value": 1},
    {"ABC": "110", "ABC'": "101", "value": 0},
    {"ABC": "110", "ABC'": "110", "value": 1},
    {"ABC": "110", "ABC'": "111", "value": 0},
    {"ABC": "111", "ABC'": "000", "value": 0},
    {"ABC": "111", "ABC'": "001", "value": 0},
    {"ABC": "111", "ABC'": "010", "value": 0},
    {"ABC": "111", "ABC'": "011", "value": 0},
    {"ABC": "111", "ABC'": "100", "value": 1},
    {"ABC": "111", "ABC'": "101", "value": 0},
    {"ABC": "111", "ABC'": "110", "value": 1},
    {"ABC": "111", "ABC'": "111", "value": 0}
]
