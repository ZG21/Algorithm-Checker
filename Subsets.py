from cut_value_calculator import cut_value_calculator
def add_subsets(key, values, current_subsets, lista_adyacencia):
    if not values:
        #current_subsets.append([key, '0'])
        current_subsets.append(cut_value_calculator([key, '0'], lista_adyacencia, 0))
        return
    #current_subsets.append([key, '0'])
    current_subsets.append(cut_value_calculator([key, '0'], lista_adyacencia, 0))
    def add_values(idx, inside_subset):
        if idx == len(values):
            if inside_subset:
                subsetAlgo = [key] + inside_subset
                #current_subsets.append(subsetAlgo)
                current_subsets.append(cut_value_calculator(subsetAlgo, lista_adyacencia, 0))
            return
        add_values(idx + 1, inside_subset + [values[idx]])
        add_values(idx + 1, inside_subset)
    add_values(0, [])


