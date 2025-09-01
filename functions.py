import pandas as pd
from pyomo.environ import value

def save_results(model, result, mes, file_name="python_results"):
    #Ergebnisse speichern:
    timesteps = list(model.T)    
    results_outflow = {}
    results_inflow = {}

    for o_name in model.O:
        results_outflow[o_name] = [value(model.outflow[o_name, t]) for t in timesteps]
        results_inflow[o_name] = [value(model.inflow[o_name, t]) for t in timesteps]

    # Ergebnisse in DataFrame sammeln
    results_df = pd.DataFrame(index=timesteps)

    # Outflows
    for o_name, values in results_outflow.items():
        results_df[f"outflow_{o_name}"] = values

    # Inflows
    for o_name, values in results_inflow.items():
        results_df[f"inflow_{o_name}"] = values

    # Speicherstände (falls SOC existiert)
    for sto in model.S:
        soc_values = [value(model.soc[sto, t]) for t in timesteps]
        results_df[f"soc_{sto}"] = soc_values

    # Ergebnisse speichern
    if file_name.split(".")[1] != "xlsx":
        file_name += ".xlsx"
    results_df.to_excel(file_name, index_label="timestep")

    print("Ergebnisse wurden in 'python_results.xlsx' gespeichert ✅")

def load_profile(name:str):
    if name.split(".")[1] == "xlsx":
        df = pd.read_excel(name)
    elif name.split(".")[1] == "csv":
        df = pd.read_csv(name)
    else:
        raise TypeError("Please provide .xlsx or .csv with profile in second column")
    
    df = df.reset_index(drop=True)

    if df.shape[1] < 2:
        profile = df.iloc[:, 0].to_dict()
    else:
        profile = df.iloc[:, 1].to_dict()

    return profile

def check_profiles(profiles):
    lengths = {key: len(value) for key, value in profiles.items()}
    all_lengths = list(lengths.values())
    lengths_same = all(length == all_lengths[0] for length in all_lengths)

    return lengths_same