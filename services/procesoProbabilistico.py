from TMP import TMP
actual = [2,1]
futuro = [0]

actualR = [0]
futuroR = [1,2]
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
                    value_f = value_f + value[idx]
                    futuro = futuro + key[idx]
            #validacion para sacar llave actual y valor actual
            if key[-1] != "-" and key != "value":
                for idx in actuales:
                    actual = actual + key[idx]
                    value_a = value_a + value[idx]
            #validacion para sacar el valor de combinacion de estado actual dado estafo futuro
            elif key == "value":
                value_ = value

        #validacion para tomar estado actual y global
        if idx_matriz == 0:
            obj_global = [{actual: value_a, futuro + "-": value_f}, value_,1]
        else:
            obj_actual = {actual: value_a, futuro + "-": value_f}
            #print(f"momo act{obj_actual},{value_} glob{obj_global}, idx_matriz: {idx_matriz} lm{len(matriz)}")
            if obj_actual == obj_global[0] and idx_matriz < len(matriz) - 1:
                obj_global[1] = obj_global[1] + value_
                obj_global[2] = obj_global[2] + 1
            else:
                indice = buscar_indice(obj_global[0],resultados)
                #print(f"matriz{idx_matriz} -> lenm{len(matriz)}")

                #print("indice", indice)
                if indice != -1:
                    # Si actual está en resultado, sumar su valor con el nuevo valor
                    resultados[indice][1] = resultados[indice][1] + obj_global[1]
                    resultados[indice][2] = resultados[indice][2] + obj_global[2]
                    #print(f"Se sumó el valor{obj_global[1]} del elemento en resultado:", resultados)
                else:
                    # Si actual no está en resultado, agregarlo
                    resultados.append(obj_global)
                obj_global = [{actual: value_a, futuro + "-": value_f}, value_,1]

                #print("Se agregó el elemento a resultado:", resultados)
    resultados = dividir_y_modificar(resultados)
    return resultados

def buscar_indice(elemento, resultado):
    #print("bi", elemento,resultado)
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
        # Filtrar las llaves que no terminan en un guión
        for key, value in dict_part.items():
            if key.endswith('-'):
                dict_post_soted["future"][key] = value
            else:
                dict_post_soted["actual"][key] = value
        sorted_data.append({
            "actual":sorted_dict(dict_post_soted['actual']),
            "future":sorted_dict(dict_post_soted['future']),
            "value": valueData
            })
    return sorted_data


resultados = procesar_matriz(TMP, actual, futuro)
# print("Matriz marginalizada:")
# print(len(resultados), resultados)
resultados1 = procesar_matriz(TMP, actualR, futuroR)
# print("Matriz restante:")
# print(resultados1)
matrix, costo = multiplicar_vectores(resultados, resultados1)
# print("Resultado de la multiplicación matriz marginalizada y matriz restante:")
# print(len(matrix), costo,matrix)
resultado, costo = multiplicar_elementos(matrix, TMP)
# print("Resultado de la comparacion con la matriz original:")
sortedVector = combine_and_sort_keys(resultado)
print(f"Jeronimo sortedVector: {sortedVector}")
# print(len(resultado),sortedVector ,"\n",costo,resultado)
