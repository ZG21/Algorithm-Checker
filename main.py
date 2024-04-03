from typing import Union
from fastapi import FastAPI
from services.IsBipartitionGraph import isBipartitionGraph
import logging

logger = logging.getLogger("myapp")
logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.get("/graph")
def read_root():
    graph = dict()
    logger.info("Accediendo a la ruta raíz")
    graph = {
        "name": "grafo 1",
        "nodes": [
  { "id": '1', "type": 'default', "data": { "label": '' }, "position": { "x": 100, "y": 50 }, "style": { "backgroundColor": 'red', "borderColor": 'red' } },
  { "id": '2', "type": 'default', "data": { "label": '' }, "position": { "x": 200, "y": 50 } },
  { "id": '3', "type": 'default', "data": { "label": '' }, "position": { "x": 300, "y": 50 }, "style": { "backgroundColor": 'red', "borderColor": 'red' } },
  { "id": '4', "type": 'default', "data": { "label": '' }, "position": { "x": 100, "y": 150 } },
  { "id": '5', "type": 'default', "data": { "label": '' }, "position": { "x": 300, "y": 150 }, "style": { "backgroundColor": 'red', "borderColor": 'red' } },
  { "id": '6', "type": 'default', "data": { "label": '' }, "position": { "x": 200, "y": 250 } },
],
        "edges": [
  { "id": "e1-2", "source": "1", "target": "2" },
  { "id": "e2-3", "source": "2", "target": "3" },
  { "id": "e1-4", "source": "1", "target": "4" },
  { "id": "e4-6", "source": "4", "target": "6" },
  { "id": "e6-5", "source": "6", "target": "5" },
  { "id": "e5-3", "source": "5", "target": "3" },
  { "id": "e2-6", "source": "2", "target": "6" }
],
        "nodesNumber": 6,
        "isConnected": True,
        "isComplete": False,
        "isWeighted": False,
        "isDirected": False
    }
    return {"Graph": isBipartitionGraph(graph)}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/graph")
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