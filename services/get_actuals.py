def get_actuals_to_evaluate(componente, entry):
    actuals = []
    position_rest = []
    for key, value in entry.items():
        if key not in componente[1]:
            actuals.insert(0, value["position"])
        else:
            position_rest.append(value["position"])
    if len(actuals) == 0:
        actuals.append("0")
    return actuals, position_rest


def get_actuals_to_marginalize(componente, entry):
    position_rest = []
    actuals = []
    for key, value in entry.items():
        if key in componente[1]:
            actuals.insert(0, value["position"])
        else:
            position_rest.insert(0, value["position"])
    if len(actuals) == 0:
        actuals.append("0")
    return actuals, position_rest