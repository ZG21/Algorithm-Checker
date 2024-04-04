graph = dict()
graph = {
        "name": "grafo 1",
        "nodes": [
  { "id": '1', "type": 'default', "data": { "label": '' }, "position": { "x": 100, "y": 50 }, "style": { "backgroundColor": 'white', "borderColor": 'white' } },
  { "id": '2', "type": 'default', "data": { "label": '' }, "position": { "x": 200, "y": 50 }, "style": { "backgroundColor": 'white', "borderColor": 'white' } },
  { "id": '3', "type": 'default', "data": { "label": '' }, "position": { "x": 300, "y": 50 }, "style": { "backgroundColor": 'white', "borderColor": 'white' } },
  { "id": '4', "type": 'default', "data": { "label": '' }, "position": { "x": 100, "y": 150 }, "style": { "backgroundColor": 'white', "borderColor": 'white' } },
  { "id": '5', "type": 'default', "data": { "label": '' }, "position": { "x": 300, "y": 150 }, "style": { "backgroundColor": 'white', "borderColor": 'white' } },
  { "id": '6', "type": 'default', "data": { "label": '' }, "position": { "x": 200, "y": 250 }, "style": { "backgroundColor": 'white', "borderColor": 'white' } },
],
        "edges": [
  { "id": "e1-2", "source": "1", "target": "2" },
  { "id": "e2-3", "source": "2", "target": "3" },
  { "id": "e1-4", "source": "1", "target": "4" },
 {"id": "e1-5", "source": "1", "target": "5"},
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

graph1 = dict()
graph1 = {
        "name": "grafo EJEM TALLER2",
        "nodes": [
  { "id": '1', "type": 'default', "data": { "label": 'A' }, "position": { "x": 100, "y": 50 }, "style": { "backgroundColor": 'white', "borderColor": 'white' } },
  { "id": '2', "type": 'default', "data": { "label": 'B' }, "position": { "x": 200, "y": 50 }, "style": { "backgroundColor": 'white', "borderColor": 'white' } },
  { "id": '3', "type": 'default', "data": { "label": 'C' }, "position": { "x": 300, "y": 50 }, "style": { "backgroundColor": 'white', "borderColor": 'white' } },
  { "id": '4', "type": 'default', "data": { "label": 'X' }, "position": { "x": 100, "y": 150 }, "style": { "backgroundColor": 'white', "borderColor": 'white' } },
  { "id": '5', "type": 'default', "data": { "label": 'Y' }, "position": { "x": 200, "y": 150 }, "style": { "backgroundColor": 'white', "borderColor": 'white' } },
  { "id": '6', "type": 'default', "data": { "label": 'Z' }, "position": { "x": 300, "y": 150 }, "style": { "backgroundColor": 'white', "borderColor": 'white' } },
{ "id": '7', "type": 'default', "data": { "label": 'D' }, "position": { "x": 700, "y": 170 }, "style": { "backgroundColor": 'white', "borderColor": 'white' } },
{ "id": '8', "type": 'default', "data": { "label": 'U' }, "position": { "x": 800, "y": 250 }, "style": { "backgroundColor": 'white', "borderColor": 'white' } },
{ "id": '9', "type": 'default', "data": { "label": 'V' }, "position": { "x": 900, "y": 250 }, "style": { "backgroundColor": 'white', "borderColor": 'white' } },
],
        "edges": [
  { "id": "e2-4", "source": "2", "target": "4" },
{ "id": "e2-5", "source": "2", "target": "5" },
  { "id": "e1-4", "source": "1", "target": "4" },
 {"id": "e1-5", "source": "1", "target": "5"},
  { "id": "e3-5", "source": "3", "target": "5" },
  { "id": "e2-6", "source": "2", "target": "6" },
{ "id": "e7-8", "source": "7", "target": "8" },
{ "id": "e7-9", "source": "7", "target": "9" }
],
        "nodesNumber": 6,
        "isConnected": True,
        "isComplete": False,
        "isWeighted": False,
        "isDirected": False
    }