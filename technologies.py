def update_dict(params, params_dict):
    params_dict.update(params)
    return params_dict


params_dict = { "heat_pump_efficiency": 3,
    "gas_boiler_efficiency": 0.9,
    "heat_network_efficiency": 1,
    "power_network_efficiency": 1,

    "electricity_load": 0,
    "heat_load": 0,
    "pv_profile": 0,

    "power_price": 25,
    "gas_price": 0.1,

    "heat_pump_capex": 2500,
    "heat_storage_capex": 500,
    "gas_boiler_capex": 500,
    "pv_capex": 1100,

    "heat_pump_capacity": 1_000_000_000_000,
    "gas_boiler_capacity": 1_000_000_000_000,
    "pv_capacity": 1_000_000_000_000,
}