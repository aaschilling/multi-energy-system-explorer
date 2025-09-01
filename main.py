from MES import *
from optimize import *
from classes import *
from technologies import * 
from functions import *


######## define params ########
electricity_load = load_profile("ElectricityLoad_2016.xlsx") # in kW
heat_load = load_profile("HeatLoad_2016.xlsx")               # in kW
pv_profile =  load_profile("pv_daten_Berlin.csv")            # curve normalized to 1. To be multiplied with capacity. Everything in kW

profiles = {
    "electricity_load": electricity_load,
    "heat_load": heat_load,
    "pv_profile": pv_profile
}

params = {
    "heat_pump_capex": 1100,                  # €/kWh Capacity
    "heat_pump_efficiency": 3,                # JAZ
    "heat_pump_capacity": 100,                # 100 kW
    
    "gas_boiler_capex": 1500,                 # €/kWh Capacity capex not yet used
    "gas_boiler_efficiency": 0.9,
    "gas_boiler_capacity": 400,
    
    "heat_storage_capex": 500,                # €/kWh Capacity
    "heat_storage_capacity": 1000,            # 1000 kW
    "heat_storage_efficiency": 0.9999,         # verlust pro stunde
    "soc_start":0.5,
    
    "pv_capex": 1100,                         # €/kWh Capacity
    "pv_capacity": 1000,                      # in kW
    "pv_opex": 0.0688,                        # vorberechnet aus invest und 20a für alle erzeugten stunden... alsoo faaalsch :D

    "power_price": 0.25,                      # €/kWh
    "gas_price": 0.1,                         # €/kWh

    "heat_network_efficiency": 1,
    "power_network_efficiency": 1,

    "electricity_load": electricity_load,
    "heat_load": heat_load,
    "pv_profile": pv_profile
}


#Update Params:
params_dict = update_dict(params=params, params_dict=params_dict)

#Build the energy system, maybe later check it and plot it?
mes = build_mes(params=params, profiles=profiles)

#Find optimal state
model, result = optimize_system(mes)

#save result in to a excel file
save_results(model=model, result=result, mes=mes, file_name="python_results")

#stay strong :D
print("at least it went through <3")
