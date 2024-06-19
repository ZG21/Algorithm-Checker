from services.earth_mover_distance import earth_mover_distance
from services.prod_tensor import tensor_full_mat
from services.search_component_in_memory import search_component_in_memory
from services.get_futures_to_evaluate import get_futures_to_evaluate
from services.get_actuals import get_actuals_to_evaluate, get_actuals_to_marginalize
from services.marginalized_process import marginalizar_vacios, marginalize_matrix
from services.generate_full_combs import generate_full_combs
from services.expand_matrix import expand_matrix
from services.obtener_complemento import obtener_complemento
from services.prod_tensor import producto_tensor, vector_to_emd
from services.filtrar_componentes_repetidos import filtrar_componentes_repetidos
from services.IsBipartitionGraph import convertir_a_lista_de_adyacencia,find_components_and_check_bipartite
from services.Subsets import add_subsets
from services.delete_edge import delete_edge
from itertools import product
import copy



def calculate_cost_component(component, componente_original, new_entry, memory, state,entrada):
    print(f"--------------componente {component} {componente_original}----------------------------")
    #print(f"--------------new entry {new_entry}----------------------------")
    result_empty = {}
    pos_res = []
    subsetMarginalized = {}
    future_to_eval = {}
    actual_position_to_omit1, pos_res = [], []
    actuals_, pos_r = [], []
    comp_mat = {}
    expancion = {}
    result_actual_empty = {}
    expand_result_act = {}
    combsSubset = []
    resultado_comp = {}
    result_comple = {}
    cop_unido = []
    combinado = []
    component_in_memory = {}
    complement = []
    complement_in_memory = {}
    result_prod_tensor = {}
    component_prodTensor_in_memory = {}
    sorted_subarrays = []
    # Componente no esta en la memoria
    component_in_memory = search_component_in_memory(memory, component)
    print(f"CALC-COMPONENT-MEMO: {component_in_memory}\n")
    if len(component_in_memory) == 0:
        # Tomamos las tablas futuras a evaluar y los actuales a marginalizar en la tabla
        future_to_eval = get_futures_to_evaluate(component, new_entry)
        actual_position_to_omit1, pos_res = get_actuals_to_marginalize(component, new_entry)
        # Componenetes de un solo elemento
        if len(component[0]) == 1 and len(component[1]) == 1:
            # Cuando la componente futuro es vacio
            if component[0][0] == "0":
                actuals_, pos_r = get_actuals_to_evaluate(componente, entrada)
                future_to_eval = get_futures_to_evaluate(componente, entrada)
                print(f"WHEN 0 EN FUT future_to_eval { future_to_eval} \n actuals_ {actuals_} \n new_entry {new_entry} \n")
                for pos in actuals_:
                    if len(comp_mat) == 0:
                        comp_mat = marginalize_matrix(future_to_eval, pos)
                    else:
                        comp_mat = marginalize_matrix(comp_mat, pos)
                expancion = expand_matrix(comp_mat, entrada, pos_r)
                print(f"COMP ORG M_EXPAND componen_original: {componente_original} \n m_expand: {expancion} \n")
                result_empty = {"componente": component, "resultado": expancion}
            # Cuando la componente actual es vacio
            elif component[1][0] == "0":
                result_actual_empty = marginalizar_vacios(component, future_to_eval)
                print(f"WHEN 0 IN ACT result_actual_empty {result_actual_empty}")
                expand_result_act = expand_matrix(result_actual_empty["resultado"], future_to_eval, pos_res)
                print(f"COMP ORG M_EXPAND componen_original: {result_actual_empty} \n m_expand: {expand_result_act} \n")
                result_empty = expand_result_act
            else:
                # Cuando la componente actual y fututo tiene 1 valor
                for p in actual_position_to_omit1:
                    if len(subsetMarginalized) == 0:
                        subsetMarginalized = marginalize_matrix(future_to_eval, p)
                    else:
                        subsetMarginalized = marginalize_matrix(subsetMarginalized, p)
                m_expand = expand_matrix(subsetMarginalized, future_to_eval, pos_res)
                result_empty = {"componente": component, "resultado": m_expand}
        # Cuando alguna de las componentes tiene mas de un valor
        else:
            combsSubset = generate_full_combs(component)
            print("PEW PEW", combsSubset)
            # para las componentes con mas de un elemento sacamos sus subcomponetes y los calculamos
            for element in combsSubset:
                # Buscampos la componente en la memoria
                component_in_memory = search_component_in_memory(memory, element)
                complement = obtener_complemento(component, element)
                if (complement[0][0] == "0") or (complement[1][0] == "0"):
                    if len(complement[0])>1 or len(complement[1])>1:
                        print("IN COMPONENTE", element, f"Y COMPLENTO {complement} NO SE PUEDEN COMO CORTE")
                    else:
                        # SI la subcomponente NO esta en la memoria se calcula y se guarda
                        if len(component_in_memory) == 0:
                            r_comp = calculate_cost_component(element, component, extended_matrix, memory, state,entrada)
                            resultado_comp = r_comp
                            memory.append(resultado_comp)
                        else:
                            resultado_comp = component_in_memory
                        # Para cada subcomponente le bucamos el valor de su complemento o o calculamos si no esta
                        complement_in_memory = search_component_in_memory(memory, complement)
                        if len(complement_in_memory) == 0:
                            print("COMPLE NO ESTA")
                            print(f"memory {memory}\n comple {complement} elem {element} subsar {complement_in_memory}")
                            result = calculate_cost_component(complement, componente_original, extended_matrix, memory, state,entrada)
                            memory.append(result)
                            result_comple = result
                        else:
                            result_comple = complement_in_memory
                        result_prod_tensor = producto_tensor(resultado_comp, result_comple)
                        component_prodTensor_in_memory = search_component_in_memory(memory, result_prod_tensor["componente"])
                        print(F"PROD TENSOR ESTA EN MEMORY len(component_prodTensor_in_memory): { len(component_prodTensor_in_memory)} \n result_prod_tensor: {result_prod_tensor}")
                        if len(component_prodTensor_in_memory) == 0:
                            memory.append(result_prod_tensor)
                            result_empty = result_prod_tensor
                        else:
                            # TOMAMOS EL ELEMENTO EN MEMORIA
                            key_memory = next(iter(component_prodTensor_in_memory['resultado']))
                            print("CALC KEY IN MEMORY", key_memory)
                            memory_element = component_prodTensor_in_memory["resultado"][key_memory]
                            position_state = memory_element["combinaciones"].index(state)
                            value_memo = sum(memory_element["valores"][position_state])
                            value_result_comp = sum(result_prod_tensor["resultado"][key_memory]["valores"][position_state])
                            if value_memo > value_result_comp:
                                memory.remove(component_prodTensor_in_memory)
                                memory.append(result_prod_tensor)
                                result_empty = result_prod_tensor
                            else:
                                result_empty = component_prodTensor_in_memory
                        # Producto tensor entre componente y complemento
                        # Validar si el componente del producto tensor esta en memoria SI->guarda menor NO ->Guarda valor
                        # Result empty va a ser el menor entre el prod tensor y el valor de ese producto en la memoria
    # El elemento esta en la memoria
    else:
        # Cuando la componente esta en la memoria, calcula el complemento
        complement = obtener_complemento(componente_original, component)
        print("SI ESTA EL VALOR AHORA SU COMPLEM", complement, "COMP ORI", componente_original)
        complement_in_memory = search_component_in_memory(memory, complement)
        if len(complement_in_memory) == 0:
            print("COMPLE NO ESTA")
            result = calculate_cost_component(complement, componente_original, extended_matrix, memory, state,entrada)
            memory.append(result)
            result_comple = result
            result_prod_tensor = producto_tensor(resultado_comp, result_comple)
            component_prodTensor_in_memory = search_component_in_memory(memory, result_prod_tensor["componente"])
            print(f"COM ESTA EN MEMORY component_prodTensor_in_memory: {component_prodTensor_in_memory}")
            if len(component_prodTensor_in_memory) == 0:
                memory.append(result_prod_tensor)
                result_empty = result_prod_tensor
            else:
                # TOMAMOS EL ELEMENTO EN MEMORIA
                key_memory = next(iter(component_prodTensor_in_memory['resultado']))
                print("KEY IN MEMORY", key_memory)
                memory_element = component_prodTensor_in_memory["resultado"][key_memory]
                position_state = memory_element["combinaciones"].index(state)
                value_memo = sum(memory_element["valores"][position_state])
                value_result_comp = sum(result_prod_tensor["resultado"][key_memory]["valores"][position_state])
                if value_memo > value_result_comp:
                    memory.remove(component_prodTensor_in_memory)
                    memory.append(result_prod_tensor)
                    result_empty = result_prod_tensor
                else:
                    result_empty = component_prodTensor_in_memory
        else:
            result_comple = complement_in_memory
            result_comple_memory = search_component_in_memory(memory, result_comple["componente"])
            if len(result_comple_memory) == 0:
                result = calculate_cost_component(complement, componente_original, extended_matrix, memory, state,entrada)
                memory.append(result)
                result_empty = result
            else:
                complement_in_entry = get_futures_to_evaluate(complement, entrada)
                result_empty = {"componente": complement, "resultado": complement_in_entry}
    print(f"EMPTY RESULT result_empty: {result_empty}")
    return result_empty
    # Obtenemos el valor segun el estado para el complemento y el componente
    # Hacemos prod tensor complemento y componente en ese estado
    # (NO SE) Hacemos EMD con la extended matrix en ese estado

# TODO Ortanizar el código en funciones separadas




def final_process( extended_matrix, memory, state, entrada, element, componente, emd_memory, component_original, lista_adyacencia, corte_min_estrategia2, cost_edges):
    print("MOMO COMPOOO", componente)
    #print("rarezas component: ", component_original)
    # Obtenemos el componente
    subset_in_memory = search_component_in_memory(memory, element)
    # Obtenemos el complemento
    result_emd= 0
    complement = obtener_complemento(componente, element)
    complementSubset_in_memory = search_component_in_memory(memory, subset_in_memory)
    result_subcomponent = {}
    result_comple_memory = {}
    complement_in_entry = get_futures_to_evaluate(complement, entrada)
    # SI el complemento cumple estas condiciones de genera una k-particion
    if not ((len(complement[0])>1 and (complement[0][0] == "0")) or (len(complement[1])>1 and (complement[1][0] == "0"))):
        if len(subset_in_memory) == 0:
            result_subcomponent = calculate_cost_component(element, componente, extended_matrix, memory, state, entrada)
            memory.append(result_subcomponent)
        else:
            result_subcomponent = subset_in_memory
        if len(complementSubset_in_memory) == 0:
            result_subcomplement = calculate_cost_component(complement, componente, extended_matrix, memory, state, entrada)
            result_subcomplement_in_memory = search_component_in_memory(memory,result_subcomplement["componente"])
            if len(result_subcomplement_in_memory) == 0:
                memory.append(result_subcomplement)
                result_comple_memory = result_subcomplement
            else:
                result_comple_memory = result_subcomplement_in_memory
        else:
            result_comple_memory = complementSubset_in_memory

        result = producto_tensor({"componente": complement, "resultado": complement_in_entry},result_subcomponent)
        cut_one = result_subcomponent["componente"]
        cut_two = complement
        print(f"SUBSET IN entry {complement_in_entry} \n {result_subcomponent} \n{cut_one} {cut_two} ")
        if cut_one != cut_two:
            final_cut_tensor = producto_tensor(result,{"componente": complement, "resultado": complement_in_entry})
            vector_tensor = vector_to_emd(final_cut_tensor["resultado"], state)
            vector_original_component = vector_to_emd(component_original["resultado"],state)
            result_emd = earth_mover_distance(vector_tensor, vector_original_component)
            print(f"CORTES cut_one:{cut_one} cut_two: {cut_two}")
            print(f"RESULTADO FINAL {result_emd}")
            if len(emd_memory) == 0:
                emd_memory["cortes"] = [cut_one,cut_two]
                emd_memory["resultado"] = result_emd
            else:
                if emd_memory["resultado"] > result_emd:
                    print("ACTUALIZAAAAA\n")
                    emd_memory["cortes"] = [cut_one,cut_two]
                    emd_memory["resultado"] = result_emd
                else:
                    print("NO COMPARAAA")
        cost_edges.append({"Edge": cut_one, "resultado":result_emd})
        if len(lista_adyacencia) != 0:
            componentes, es_bipartito, sets = find_components_and_check_bipartite(lista_adyacencia)
            if (len(corte_min_estrategia2) == 0 or emd_memory["resultado"] < corte_min_estrategia2["resultado"] or
                corte_min_estrategia2["resultado"] != 0) and es_bipartito:
                print("IN estrategia 2")
                print(f"CORTES cut_one:{cut_one} cut_two: {cut_two}")
                corte_min_estrategia2["componente"] = cut_one
                corte_min_estrategia2["complemento"] = cut_two
                corte_min_estrategia2["resultado"] = emd_memory["resultado"]
                return lista_adyacencia
            else:
                return delete_edge(lista_adyacencia,componente)
        
        #Proceso para EMD
        #Producto tensor entre las componen
        print("RESULT EMD", component_original, "\n componente", result )
        
        print(f"MOMO !!!! Component {result_subcomponent}\nComplement {result_subcomplement}")
lista_adyacencia ={
'a': ['A', 'B'],
'b': ['A', 'B'],
}

entrada = {
    "A": {
        "combinaciones": [[0, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 0], [1, 0, 1, 0], [0, 1, 1, 0], [1, 1, 1, 0], [0, 0, 0, 1], [1, 0, 0, 1], [0, 1, 0, 1], [1, 1, 0, 1], [0, 0, 1, 1], [1, 0, 1, 1], [0, 1, 1, 1], [1, 1, 1, 1]],
        "valores": [[0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [0, 1],[0, 1], [0, 1], [0, 1]],
        "position": 0
    },
    "B": {
        "combinaciones": [[0, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 0], [1, 0, 1, 0], [0, 1, 1, 0], [1, 1, 1, 0],[0, 0, 0, 1], [1, 0, 0, 1], [0, 1, 0, 1], [1, 1, 0, 1], [0, 0, 1, 1], [1, 0, 1, 1], [0, 1, 1, 1], [1, 1, 1, 1]],
        "valores": [[0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [1, 0],[1, 0], [1, 0], [1, 0]],
        "position": 0
    },
    "C": {
        "combinaciones": [[0, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 0], [1, 0, 1, 0], [0, 1, 1, 0], [1, 1, 1, 0],[0, 0, 0, 1], [1, 0, 0, 1], [0, 1, 0, 1], [1, 1, 0, 1], [0, 0, 1, 1], [1, 0, 1, 1], [0, 1, 1, 1], [1, 1, 1, 1]],
        "valores": [[0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [1, 0], [0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [1, 0], [0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [1, 0], [0.7, 0.3],[0.7, 0.3], [0.7, 0.3], [1, 0]],
        "position": 0
    },
   "D": {
        "combinaciones": [[0, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 0], [1, 0, 1, 0], [0, 1, 1, 0], [1, 1, 1, 0],[0, 0, 0, 1], [1, 0, 0, 1], [0, 1, 0, 1], [1, 1, 0, 1], [0, 0, 1, 1], [1, 0, 1, 1], [0, 1, 1, 1], [1, 1, 1, 1]],
        "valores": [[0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [1, 0], [0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [1, 0], [0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [1, 0], [0.7, 0.3], [0.7, 0.3], [0.7, 0.3], [1, 0]],
        "position": 0
    }

}
# Componente abc
componente = [["A", "B", "C"], ["a", "b", "c"]]
futures_to_evaluate = {}
component_matrix = {}
state = [1, 0, 0, 0]
futures_to_evaluate = get_futures_to_evaluate(componente, entrada)
actual_position_to_omit, pos_r = get_actuals_to_evaluate(componente, entrada)
print("MOMO EOEOEO", actual_position_to_omit,pos_r)
for pos in actual_position_to_omit:
    if len(component_matrix) == 0:
        component_matrix = marginalize_matrix(futures_to_evaluate, pos)
    else:
        component_matrix = marginalize_matrix(component_matrix, pos)
extended_matrix = expand_matrix(component_matrix, entrada, pos_r)
print("MOMO uwu",extended_matrix)
component_original = tensor_full_mat(extended_matrix, componente, entrada)
combs = generate_full_combs(componente)
memory = []
print(f"EXTENDED MAT: {extended_matrix}\n")


# Componente ab
componente1 = [["A", "B"], ["a", "b"]]
component_matrix1 = {}
futures_to_evaluate1 = get_futures_to_evaluate(componente1, entrada)
actual_position_to_omit1, pos_r1 = get_actuals_to_evaluate(componente1, entrada)
print("EXO", futures_to_evaluate1)
for pos in actual_position_to_omit1:
    if len(component_matrix1) == 0:
        component_matrix1 = marginalize_matrix(futures_to_evaluate1, pos)
    else:
        component_matrix1 = marginalize_matrix(component_matrix1, pos)
extended_matrix1 = expand_matrix(component_matrix1, extended_matrix, pos_r1)
print("MOMO uwu 2",extended_matrix1)
component_original1 = tensor_full_mat(extended_matrix1, componente1, extended_matrix)
#combs1 = generate_full_combs(componente1)
combs1 = []
memory = []
print(f"EXTENDED MAT: {extended_matrix1}\n combs1{combs1}")

emd_memory = {}
corte_minimo = {}
cost_edges = []

for key, values in lista_adyacencia.items():
    subsets_iteration = []
    add_subsets(key, values, subsets_iteration, lista_adyacencia)
    combs1.extend(subsets_iteration)

for element in combs1:
    str_elem_future = "".join(element[0])
    str_elem_actual = "".join(element[1])
    print("ELEEEEMEEEENTOOOOO",element)
    memory = filtrar_componentes_repetidos(memory)
    if len(emd_memory) == 0:
        lista_adyacencia = final_process(extended_matrix1,memory,state,extended_matrix,element,componente1,emd_memory, component_original1, lista_adyacencia, corte_minimo, cost_edges)
    else:
        if emd_memory["resultado"] != 0:
            for corte in emd_memory["cortes"]:
                str_cut_future = "".join(corte[0])
                str_cut_actual = "".join(corte[1])
                print(f"Parametros{emd_memory} str_elem_future {str_elem_future} \n str_elem_actual {str_elem_actual} \n str_cut_future {str_cut_future} \n str_cut_actual {str_cut_actual} ")
                if not (str_cut_actual in str_elem_actual and str_cut_future in str_elem_future):
                    print("INNNNN",emd_memory, element)
                    lista_adyacencia = final_process(extended_matrix1,memory,state,extended_matrix,element,componente1,emd_memory, component_original1, lista_adyacencia, corte_minimo,cost_edges)
    # producto_tensor(result_subcomponent,result_complement)
    # # Obtenemos el valor segun el estado para el complemento y el componente
    # # Hacemos prod tensor complemento y componente en ese estado
    # # Hacemos EMD con la extended matrix en ese estado

print("MEMORIA:", memory)
print("MEMORIA EMD:", emd_memory)

def eliminar_duplicados(lista):
    lista_sin_duplicados = []
    edges_ya_vistos = set()

    for d in lista:
        # Convertir las listas internas de 'Edge' en tuplas para que sean hashables
        edge_tuple = tuple(map(tuple, d['Edge']))
        
        if edge_tuple not in edges_ya_vistos:
            # Añadir el Edge al conjunto de vistos
            edges_ya_vistos.add(edge_tuple)
            # Añadir el elemento original a la lista sin duplicados
            lista_sin_duplicados.append(d)

    return lista_sin_duplicados
cost_edges1 = eliminar_duplicados(cost_edges)

print("Costo edges", cost_edges1)