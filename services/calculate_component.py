from services.search_component_in_memory import search_component_in_memory
from services.get_actuals import get_actuals_to_evaluate, get_actuals_to_marginalize
from services.get_futures_to_evaluate import get_futures_to_evaluate
from services.marginalized_process import marginalize_matrix,marginalizar_vacios
from services.expand_matrix import expand_matrix
from services.generate_full_combs import generate_full_combs

def calculate_cost_component(component, componente_original, new_entry, memory, state,entrada, componente):
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
                result_empty = result_comple_memory
    print(f"EMPTY RESULT result_empty: {result_empty}")
    return result_empty
    # Obtenemos el valor segun el estado para el complemento y el componente
    # Hacemos prod tensor complemento y componente en ese estado
    # (NO SE) Hacemos EMD con la extended matrix en ese estado