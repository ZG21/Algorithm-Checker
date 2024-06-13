
def search_component_in_memory(memory, component):
    for element in memory:
        if element['componente'] == component:
            return element
    return {}