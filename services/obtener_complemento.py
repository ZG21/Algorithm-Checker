def obtener_complemento(componente_original, subcomponente):
    complemento = []
    for original, sub in zip(componente_original, subcomponente):
        # Encontrar elementos en original que no están en sub
        elementos_complemento = [elemento for elemento in original if elemento not in sub]
        # Si el resultado está vacío, agregar "0"
        if not elementos_complemento:
            elementos_complemento = ["0"]
        complemento.append(elementos_complemento)
    return complemento