def get_futures_to_evaluate(componente, entry):
    futures = {}
    for key, value in entry.items():
        if key in componente[0]:
            futures[key] = value
    return futures