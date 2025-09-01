import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_results(python_file="python_results.xlsx", matlab_file="Results.xlsx"):
    # Python Ergebnisse
    py = pd.read_excel(python_file)
    py.set_index("timestep", inplace=True)

    # Matlab Ergebnisse
    matlab = pd.read_excel(matlab_file)
    matlab.set_index("timestep", inplace=True)

    return py, matlab

def compare_storage(py, matlab, storage_name="soc_heat_storage", matlab_col="E_HSto"):
    """Vergleicht Speicherfüllstände"""
    plt.figure()
    plt.plot(matlab.index, matlab[matlab_col], label="Matlab Speicher [kWh]")
    plt.plot(py.index, py[storage_name], "--", label="Python Speicher [kWh]")
    plt.xlabel("Zeitschritt")
    plt.ylabel("Speicherinhalt [kWh]")
    plt.legend()
    plt.grid(True)
    plt.title("Vergleich Speicherfüllstand")
    plt.show()

def compare_flows(py, matlab, flow_name_py, flow_name_matlab):
    """Vergleicht Flüsse (z.B. Gasboiler-Leistung)"""
    plt.figure()
    plt.plot(matlab.index, matlab[flow_name_matlab], label=f"Matlab {flow_name_matlab}")
    plt.plot(py.index, py[flow_name_py], "--", label=f"Python {flow_name_py}")
    plt.xlabel("Zeitschritt")
    plt.ylabel("Leistung [kW]")
    plt.legend()
    plt.grid(True)
    plt.title(f"Vergleich: {flow_name_py} vs {flow_name_matlab}")
    plt.show()

def calc_difference(py, matlab, flow_name_py, flow_name_matlab):
    matlab_val = matlab[flow_name_matlab]
    py_val = py[flow_name_py]
    diff = matlab_val - py_val
    diff_mean = diff.mean()
    abweichung = np.std(diff)

    return diff_mean, abweichung

if __name__ == "__main__":
    py, matlab = load_results()

    compare_storage(py, matlab, storage_name="soc_heat_storage", matlab_col="E_HSto")
    compare_flows(py, matlab, flow_name_py="inflow_gas_boiler_1", flow_name_matlab="Pgas_Boi")
    print(calc_difference(py, matlab, flow_name_py="inflow_gas_boiler_1", flow_name_matlab="Pgas_Boi"))
    compare_flows(py, matlab, flow_name_py="inflow_heat_pump_1", flow_name_matlab="Pel_HeP")
    compare_flows(py, matlab, flow_name_py="outflow_pv_1", flow_name_matlab="PV")

#Matlab Variablennamen

# timestep,Pel_im,Pel_ex,Pgas_im,Pel_HeP,Pht_HeP,Pgas_Boi,Pht_Boi,E_HSto,Pcha_HSto,Pdis_HSto,HeatDemand,ElecDemand,PV
