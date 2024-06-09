import copy
def get_actuals_to_evaluate(componente, entry):
    #print("comp act",componente)
    actuals = []
    position_rest = []
    for key, value in entry.items():
        if key not in componente[1]:
          actuals.insert(0,value["position"])
        else:
            position_rest.insert(0,value["position"])
    if len(actuals) == 0:
        actuals.append("0")
    return actuals, position_rest

def get_actuals_to_marginalize(componente, entry):
    #print("comp act",componente)
    position_rest = []
    
    actuals = []
    for key, value in entry.items():
        if key in componente[1]:
          actuals.insert(0,value["position"])
        else:
            position_rest.insert(0,value["position"])
    if len(actuals) == 0:
        actuals.append("0")
    return actuals, position_rest

def get_futures_to_evaluate(componente, entry):
    #print("comp future", componente)
    futures = {}
    for key, value in entry.items():
        if key in componente[0]:
          futures[key] = value
    return futures

def sumar_vectores(vector1, vector2):
    if len(vector1) != len(vector2):
        raise ValueError("Los vectores deben tener el mismo tamaño")
    vector_suma = []
    for i in range(len(vector1)):
        vector_suma.append((vector1[i] + vector2[i])/2)
    return vector_suma

def generar_parejas_vacio(arr, vacios):
    for elem in arr:
        pareja1 = [["0"], [elem]]
        pareja2 = [[elem], ["0"]]

        if pareja1 not in vacios:
            vacios.append(pareja1)

        if pareja2 not in vacios:
            vacios.append(pareja2)
    return vacios

def marginalize_matrix(matrix, position):
  pos = int(position)
  new_matrix = {}
  print("POs", pos,type(pos), matrix)
  for key, value in matrix.items():
    #print("Marginaliza", value ,key, "\n", matrix)
    clon_comb = copy.deepcopy(value['combinaciones'])
    nuevas_combinaciones = []
    nuevos_valores = []
    next_position = 2**pos
    evaluated_positions = []
    for i in range(len(clon_comb)):
      if i not in evaluated_positions and i + next_position < len(clon_comb):
        nueva_comb = clon_comb[i][:pos] + clon_comb[i][pos + 1:]
        nuevas_combinaciones.append(nueva_comb)
        evaluated_positions.append(i)
        evaluated_positions.append(i + next_position)
        nuevos_valores.append(sumar_vectores(value['valores'][i], value['valores'][i+next_position]))

      elif i == len(clon_comb)-1:
        new_matrix[key] = {"combinaciones": nuevas_combinaciones, "valores": nuevos_valores, "position": value['position']}
  return new_matrix

def marginalizar_vacios(component, entry, new_entry):
    print(f"marg vacio")

def generar_combinaciones(array):
    def backtrack(start, path):
        # Agregar la combinación actual a los resultados
        combinaciones.append(path)
        # Generar todas las combinaciones posibles comenzando desde 'start'
        for i in range(start, len(array)):
            backtrack(i + 1, path + [array[i]])

    combinaciones = []
    backtrack(0, [])
    return combinaciones[1:]  # Excluir la combinación vacía

def calculate_cost_component(component, original_entry,new_entry, memory):
    print(f"--------------componente {component}----------------------------")
    if len(component[0]) == 1 and len(component[1]) == 1:
        if component[0][0] == "0":
            marginalizar_vacios(component, entrada, new_entry)
        elif component[1][0] == "0":
            marginalizar_vacios(component, entrada, new_entry)
        else:
            future_to_eval = get_futures_to_evaluate(component, new_entry)
            actual_position_to_omit1 = get_actuals_to_marginalize(component, new_entry)
            subsetMarginalized = {}
            print(f"actual omit{actual_position_to_omit1} futures: {future_to_eval}")
            for pos in actual_position_to_omit1:
                if len(subsetMarginalized) == 0:
                    subsetMarginalized = marginalize_matrix(future_to_eval, pos)
                else:
                    subsetMarginalized = marginalize_matrix(subsetMarginalized, pos)
            memory.append(subsetMarginalized)
            print(f"Momo state {future_to_eval} \n"
                  f"Resultado: {subsetMarginalized}")
    else:
        subsNums = generar_combinaciones(component[0])
        subsDens = generar_combinaciones(component[1])
        print(f"Momo solo comp {component}")

def generate_full_combs(component):
    numeradores = generar_combinaciones(component[0])
    denominadores = generar_combinaciones(component[1])
    full_comb = []
    vacios = []
    for comb in numeradores:
        for comb2 in denominadores:
            if len(comb) == 1 and len(comb2) == 1:
                vacios = generar_parejas_vacio(comb, vacios)
            if not(comb == component[0] and comb2 == component[1]):
                full_comb.append([comb, comb2])

    full_comb.extend(vacios)
    return full_comb

entrada = {
        "a":{
        "combinaciones": [[0,0,0],[1,0,0],[0,1,0],[1,1,0],[0,0,1],[1,0,1],[0,1,1],[1,1,1]],
        "valores":[[1,0],[1,0],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1]],
        "position": 0
        },
        "b":{
        "combinaciones": [[0,0,0],[1,0,0],[0,1,0],[1,1,0],[0,0,1],[1,0,1],[0,1,1],[1,1,1]],
        "valores":[[1,0],[1,0],[1,0],[1,0],[1,0],[0,1],[1,0],[0,1]],
        "position": 1
        },
        "c":{
        "combinaciones": [[0,0,0],[1,0,0],[0,1,0],[1,1,0],[0,0,1],[1,0,1],[0,1,1],[1,1,1]],
        "valores":[[1,0],[0,1],[0,1],[1,0],[1,0],[0,1],[0,1],[1,0]],
        "position": 2
        }
}
# Componente ab/ab
componente = [["a","b"],["a","b"]]
futures_to_evaluate = {}
original_matrix = {}
full_rows = 2**len(componente[0])
print("Jeronimo full_rows", full_rows)
futures_to_evaluate = get_futures_to_evaluate(componente, entrada)
actual_position_to_omit, pos_r = get_actuals_to_evaluate(componente, entrada)
print(f"Jeronimo position_r: {pos_r}  ")
for pos in actual_position_to_omit:
    if len(original_matrix) == 0:
        original_matrix = marginalize_matrix(futures_to_evaluate, pos)
    else:
        original_matrix = marginalize_matrix(original_matrix, pos)
print(f"jeronimo original_matrix: {original_matrix}")

combs = generate_full_combs(componente)
# memory = []
# for element in combs:
#     calculate_cost_component(element, entrada,original_matrix, memory)

