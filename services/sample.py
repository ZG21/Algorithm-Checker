from GraphsExaples import graph1
from parcial import generate_combinations
from IsBipartitionGraph import find_components_and_check_bipartite,convertir_a_lista_de_adyacencia

#print("Marlon component", componentsOfGraph(graph1))
# Convertimos el grafo y verificamos si es desconexo
lista_adyacencia = convertir_a_lista_de_adyacencia(graph1)
print(f"El grafo, listas de adyacencia: {lista_adyacencia}")
# Encontrar componentes y verificar bipartición
componentes, es_bipartito, sets = find_components_and_check_bipartite(lista_adyacencia)

if es_bipartito:
    print(".")
else:
    print(".")

if len(componentes) > 1:
    combinaciones = generate_combinations(lista_adyacencia)
    print(f"diccionario: {lista_adyacencia}")
    print(f"combinaciones: {combinaciones}")
else:
    print(".")
#es_desconexo = es_grafo_desconexo(lista_adyacencia)
#print(f"El grafo es desconexo: {es_desconexo}")
#request = requests.get('http://127.0.0.1:8000/')

#print(request.json())