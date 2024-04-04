import requests
from GraphsExaples import graph1
from IsBipartitionGraph import find_components_and_check_bipartite,convertir_a_lista_de_adyacencia

#print("Marlon component", componentsOfGraph(graph1))
# Convertimos el grafo y verificamos si es desconexo
lista_adyacencia = convertir_a_lista_de_adyacencia(graph1)
print(f"El grafo, listas de adyacencia: {lista_adyacencia}")
# Encontrar componentes y verificar bipartición
componentes, es_bipartito, sets = find_components_and_check_bipartite(lista_adyacencia)

if es_bipartito:
    print("El grafo es bipartito.")
else:
    print("El grafo no es bipartito.")

if len(componentes) > 1:
    print("El grafo es disconexo y sus componentes son:", componentes," Conjuntos bipartitos",sets)
else:
    print("El grafo es conexo.")
#es_desconexo = es_grafo_desconexo(lista_adyacencia)
#print(f"El grafo es desconexo: {es_desconexo}")
#request = requests.get('http://127.0.0.1:8000/')

#print(request.json())