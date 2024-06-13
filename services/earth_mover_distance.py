def earth_mover_distance(a, b):
    print("EMD", a, b)
    # Encontrar la longitud máxima entre las dos listas
    max_length = max(len(a), len(b))
    # Rellenar las listas más cortas con ceros hasta que tengan el mismo tamaño
    if len(a) < max_length:
        a.extend([0.0] * (max_length - len(a)))
    if len(b) < max_length:
        b.extend([0.0] * (max_length - len(b)))
    emd = [0.0] * max_length
    total_distance = 0.0
    for i in range(max_length):
        if i == 0:
            emd[i] = a[i] - b[i]
        else:
            emd[i] = (a[i] + emd[i - 1]) - b[i]
        total_distance += abs(emd[i])
        print(f"emd[{i}] = {emd[i]}")
    return total_distance