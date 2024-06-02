TMP = datos_actualizados = [
    {"ABC": "000", "ABC-": "000", "value": 1},
    {"ABC": "000", "ABC-": "001", "value": 0},
    {"ABC": "000", "ABC-": "010", "value": 0},
    {"ABC": "000", "ABC-": "011", "value": 0},
    {"ABC": "000", "ABC-": "100", "value": 0},
    {"ABC": "000", "ABC-": "101", "value": 0},
    {"ABC": "000", "ABC-": "110", "value": 0},
    {"ABC": "000", "ABC-": "111", "value": 0},
    {"ABC": "001", "ABC-": "000", "value": 0},
    {"ABC": "001", "ABC-": "001", "value": 0},
    {"ABC": "001", "ABC-": "010", "value": 0},
    {"ABC": "001", "ABC-": "011", "value": 0},
    {"ABC": "001", "ABC-": "100", "value": 1},
    {"ABC": "001", "ABC-": "101", "value": 0},
    {"ABC": "001", "ABC-": "110", "value": 0},
    {"ABC": "001", "ABC-": "111", "value": 1},
    {"ABC": "010", "ABC-": "000", "value": 0},
    {"ABC": "010", "ABC-": "001", "value": 0},
    {"ABC": "010", "ABC-": "010", "value": 0},
    {"ABC": "010", "ABC-": "011", "value": 0},
    {"ABC": "010", "ABC-": "100", "value": 0},
    {"ABC": "010", "ABC-": "101", "value": 1},
    {"ABC": "010", "ABC-": "110", "value": 0},
    {"ABC": "010", "ABC-": "111", "value": 0},
    {"ABC": "011", "ABC-": "000", "value": 0},
    {"ABC": "011", "ABC-": "001", "value": 0},
    {"ABC": "011", "ABC-": "010", "value": 0},
    {"ABC": "011", "ABC-": "011", "value": 0},
    {"ABC": "011", "ABC-": "100", "value": 0},
    {"ABC": "011", "ABC-": "101", "value": 1},
    {"ABC": "011", "ABC-": "110", "value": 0},
    {"ABC": "011", "ABC-": "111", "value": 0},
    {"ABC": "100", "ABC-": "000", "value": 0},
    {"ABC": "100", "ABC-": "010", "value": 0},
    {"ABC": "100", "ABC-": "001", "value": 1},
    {"ABC": "100", "ABC-": "011", "value": 0},
    {"ABC": "100", "ABC-": "100", "value": 0},
    {"ABC": "100", "ABC-": "101", "value": 0},
    {"ABC": "100", "ABC-": "110", "value": 0},
    {"ABC": "100", "ABC-": "111", "value": 0},
    {"ABC": "101", "ABC-": "000", "value": 0},
    {"ABC": "101", "ABC-": "001", "value": 0},
    {"ABC": "101", "ABC-": "010", "value": 0},
    {"ABC": "101", "ABC-": "011", "value": 0},
    {"ABC": "101", "ABC-": "100", "value": 0},
    {"ABC": "101", "ABC-": "101", "value": 0},
    {"ABC": "101", "ABC-": "110", "value": 0},
    {"ABC": "101", "ABC-": "111", "value": 1},
    {"ABC": "110", "ABC-": "000", "value": 0},
    {"ABC": "110", "ABC-": "001", "value": 0},
    {"ABC": "110", "ABC-": "010", "value": 0},
    {"ABC": "110", "ABC-": "011", "value": 0},
    {"ABC": "110", "ABC-": "100", "value": 1},
    {"ABC": "110", "ABC-": "101", "value": 0},
    {"ABC": "110", "ABC-": "110", "value": 0},
    {"ABC": "110", "ABC-": "111", "value": 0},
    {"ABC": "111", "ABC-": "000", "value": 0},
    {"ABC": "111", "ABC-": "001", "value": 0},
    {"ABC": "111", "ABC-": "010", "value": 0},
    {"ABC": "111", "ABC-": "011", "value": 0},
    {"ABC": "111", "ABC-": "100", "value": 0},
    {"ABC": "111", "ABC-": "101", "value": 0},
    {"ABC": "111", "ABC-": "110", "value": 1},
    {"ABC": "111", "ABC-": "111", "value": 0}
]
actual = ["1","2"]
futuro = ["2"]

"""
1 cuando sgte valor es 0
    si valor esta en actuales
        agregamos en actuales todos los indices de los actuales menos el del valor
        buscar valor en lista adyacencias
        recorremos sus values y su valor correspndiente en indices se agrega a futuros
    si valor esta en futuros
        agregamos en futuros todos los indices del valor
        si valor no esta en value agrego a actuales el indice de la key donde no estuvo el valor
2 cuando sgte valor != 0
    agregamos indices de futuros en futuro 
    agregamos indices de actuales en actual
"""

actualR = ["1","2"]
futuroR = ["0"]
def procesar_matriz(matriz, actuales, futuros):
    resultados=[]
    esta_en_resultado = False
    obj_global = {}
    obj_actual = {}
    for idx_matriz,elem in enumerate(matriz):
        futuro = ""
        value_f = ""
        actual = ""
        value_a = ""
        value_ = 0
        #Recorrido de elementos de cada objeto de la matriz, llave y valor
        for key, value in elem.items():
            #validacion para sacar llave futura y valor futuro
            if key[-1] == "-":
                for idx in futuros:
                    value_f = value_f + value[int(idx)]
                    futuro = futuro + key[int(idx)]
            #validacion para sacar llave actual y valor actual
            if key[-1] != "-" and key != "value":
                for idx in actuales:
                    actual = actual + key[int(idx)]
                    value_a = value_a + value[int(idx)]
            #validacion para sacar el valor de combinacion de estado actual dado estafo futuro
            elif key == "value":
                value_ = value

        #validacion para tomar estado actual y global
        if idx_matriz == 0:
            obj_global = [{actual: value_a, futuro + "-": value_f}, value_,1]
        else:
            obj_actual = {actual: value_a, futuro + "-": value_f}
            if obj_actual == obj_global[0] and idx_matriz < len(matriz) - 1:
                obj_global[1] = obj_global[1] + value_
                obj_global[2] = obj_global[2] + 1
            else:
                indice = buscar_indice(obj_global[0],resultados)

                if indice != -1:
                    # Si actual está en resultado, sumar su valor con el nuevo valor
                    resultados[indice][1] = resultados[indice][1] + obj_global[1]
                    resultados[indice][2] = resultados[indice][2] + obj_global[2]
                else:
                    # Si actual no está en resultado, agregarlo
                    resultados.append(obj_global)
                obj_global = [{actual: value_a, futuro + "-": value_f}, value_,1]

    resultados = dividir_y_modificar(resultados)
    return resultados

def buscar_indice(elemento, resultado):
    for i, item in enumerate(resultado):
        if item[0] == elemento:
            return i
    return -1

def dividir_y_modificar(arreglo_de_arreglos):
    resultado = []
    for subarreglo in arreglo_de_arreglos:
        if len(subarreglo) == 3 and subarreglo[2] != 0:
            resultado.append([subarreglo[0], subarreglo[1] / subarreglo[2]])
    return resultado

def multiplicar_vectores(vector1, vector2):
    resultado = []
    costo = 0
    for elem1 in vector1:
        for elem2 in vector2:
            multiplicacion = {}

            # Combinar las claves y valores de los diccionarios
            for key, value in elem1[0].items():
                multiplicacion[key] = value
            for key, value in elem2[0].items():
                multiplicacion[key] = value
            # Multiplicar los valores
            multiplicacion_valor = elem1[1] * elem2[1]
            costo = costo + multiplicacion_valor
            resultado.append([multiplicacion, multiplicacion_valor])

    return resultado, costo

def multiplicar_elementos(vector, TMP):
    resultado = []
    costo = 0
    for i in range(len(vector)):
        elem1 = vector[i]
        elem2 = TMP[i]
        multiplicacion = elem1[0].copy()  # Copiar el diccionario del elemento del vector
        multiplicacion_valor = elem1[1] * elem2['value']
        costo = costo + multiplicacion_valor
        resultado.append([multiplicacion, multiplicacion_valor])

    return resultado, costo

def sorted_dict(dict):
    # Ordenar las claves alfabéticamente
    claves_ordenadas = sorted(dict.keys())
    # Función para ordenar las claves internamente y ajustar los valores
    def ordenar_clave_y_valor(clave, valor):
        # Si la clave contiene un guion, lo manejamos de manera especial
        if '-' in clave:
            # Separar la parte alfabética y el guion
            parte_alfabetica = ''.join(sorted(c for c in clave if c.isalpha()))
            valor_ordenado = ''.join([valor[clave.index(c)] for c in parte_alfabetica])
            return parte_alfabetica, valor_ordenado
        elif len(clave) > 1 and clave != ''.join(sorted(clave)):
            clave_ordenada = ''.join(sorted(clave))
            valor_ordenado = ''.join([valor[clave.index(c)] for c in sorted(clave)])
            return clave_ordenada, valor_ordenado
        else:
            return clave, valor

    # Concatenar las claves y los valores correspondientes
    clave_concatenada = ''
    valor_concatenado = ''
    contiene_guion = False

    for clave in claves_ordenadas:
        clave_ordenada, valor_ordenado = ordenar_clave_y_valor(clave, dict[clave])
        clave_concatenada += clave_ordenada
        valor_concatenado += valor_ordenado
        if '-' in clave:
            contiene_guion = True

    # Añadir el guion al final si alguna clave tenía guion
    if contiene_guion:
        clave_concatenada += '-'

    # Crear el nuevo diccionario con la clave y valor concatenados
    nuevo_diccionario = {clave_concatenada: valor_concatenado}

    return nuevo_diccionario

# Función para combinar y ordenar claves y valores
def combine_and_sort_keys(data):
    sorted_data = []
    dict_post_soted = {
        "future": {},
        "actual": {},
    }
    for item in data:
        dict_part, valueData = item
        combine_actual_key = ""
        combine_actual_val = ""
        combine_future_key = ""
        combine_future_val = ""
        actual_dic = {}
        future_dic = {}
        # Filtrar las llaves que no terminan en un guión
        for key, value in dict_part.items():
            if key.endswith('-'):
                dict_post_soted["actual"][key] = value
                keys = dict_post_soted["actual"].keys()
                nueva_cadena1 = "".join([combine_future_val, dict_post_soted["actual"][key]])
                combine_future_val = nueva_cadena1
                combine_future_key += ''.join(key).replace('-', '')
                future_dic = {combine_future_key+"-": nueva_cadena1}
            else:
                dict_post_soted["actual"][key] = value
                keys = dict_post_soted["actual"].keys()
                nueva_cadena = "".join([combine_actual_val, dict_post_soted["actual"][key]])
                combine_actual_val = nueva_cadena
                combine_actual_key += ''.join(key)
                actual_dic = {combine_actual_key: nueva_cadena}
        sorted_data.append({
            "actual":sorted_dict(actual_dic),
            "future":sorted_dict(future_dic),
            "value": valueData
            })
    return sorted_data
def state_To_Compare(TMP,state_to_compare):
    estado_a_comparar = []
    for element in TMP:
        for key,val in element.items():
            if key[-1] != "-" and key != "value" and val == state_to_compare[key]:
                estado_a_comparar.append(element)
    return estado_a_comparar

def cut_edge_calculator(subsets, lista_adyacencia,position_dict):
  future = {}
  future_rest={}
  actuales={}
  actuales_rest = {}
  futureInd = []
  future_restInd = []
  actualesInd = []
  actuales_restInd = []
  for element in lista_adyacencia:
      if len(subsets) == 2 and subsets[1] != 0:
            values_by_subset_key = lista_adyacencia[f"{subsets[0]}"]
            future = {key: value for key, value in position_dict["future"].items() if key in subsets}
            future_rest = {key: value for key, value in position_dict["future"].items() if key not in subsets}
            actuales = {key: value for key, value in position_dict["actual"].items() if key not in subsets}
            actuales_rest = {key: value for key, value in position_dict["actual"].items() if key in subsets}

  for key, val in future.items():
      futureInd.append(f"{val}")
  for key, val in future_rest.items():
      future_restInd.append(f"{val}")
  for key, val in actuales.items():
      actualesInd.append(f"{val}")
  for key, val in actuales_rest.items():
      actuales_restInd.append(f"{val}")

  result = {"subsets": subsets, "actual": actualesInd,  "future": futureInd, "future_rest":future_restInd, "actual_rest": actuales_restInd}
  return result

def earth_mover_distance(a, b):
    # Encontrar la longitud máxima entre las dos listas
    max_length = max(len(a), len(b))

    # Rellenar las listas más cortas con objetos con valor 0 hasta que tengan el mismo tamaño
    if len(a) < max_length:
        a.extend([{"value": 0}] * (max_length - len(a)))
    if len(b) < max_length:
        b.extend([{"value": 0}] * (max_length - len(b)))

    emd = [0] * max_length
    total_distance = 0
    for i in range(1, max_length):
        emd[i] = (a[i - 1]["value"] + emd[i - 1]) - b[i - 1]["value"]
        total_distance += abs(emd[i])

    return total_distance


resultados = procesar_matriz(TMP, actual, futuro)
resultados1 = procesar_matriz(TMP, actualR, futuroR)
matrix, costo = multiplicar_vectores(resultados, resultados1)
resultado, costo = multiplicar_elementos(matrix, TMP)