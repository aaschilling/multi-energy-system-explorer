from classes import *
import networkx as nx
import matplotlib.pyplot as plt

def build_mes(params, profiles):
    ######## Nodes ########
    p1 = Node("p1", "p")
    p2 = Node("p2", "p")
    h1 = Node("h1", "h")
    h2 = Node("h2", "h")
    g1 = Node("1g", "g")

    nodes = [h1, g1, p2, p1, h2, ]
    ######## Resources ########
    power_load = Prosumer("power_load", "p", p1, None, capex=0, opex=0, efficiency=1, capacity=1_000_000000, profile=profiles["electricity_load"])
    heat_load = Prosumer("heat_load", "h", h1, None, capex=0, opex=0, efficiency=1, capacity=1_000_000, profile=profiles["heat_load"])

    heat_pump_1 = Heat_Pump("heat_pump_1", "p", p2, h2, capex=params["heat_pump_capex"], opex=0, capacity=params["heat_pump_capacity"], efficiency=params["heat_pump_efficiency"])
    gas_boiler_1 = Gas_Boiler("gas_boiler_1", "g", g1, h2, capex=params["gas_boiler_capex"], opex=0, capacity=params["gas_boiler_capacity"], efficiency=params["gas_boiler_efficiency"])

    pv_1 = PV("pv_1", "p", from_node=None, to_node=p2, capex=params["pv_capex"], opex=params["pv_opex"], efficiency=1, capacity=params["pv_capacity"], profile=profiles["pv_profile"])
    power_import = Grid_Import("power_import", "p", None, p2, capex=0, opex=params["power_price"], efficiency=1, capacity=1_000_000_000)
    power_export = Grid_Import("power_export", "p", p2, None, capex=0, opex=0, efficiency=1, capacity=1_000_000_000) #wenn ohne export, dann muss pv_rule geändert werden. Daher einfach efficiency=1, cpapec und opex 0, dann isses auch egal, ob und wann es ne einspeisevergütung gibt.
    gas_import = Grid_Import("gas_import", "g", None, g1, capex=0, opex=params["gas_price"], efficiency=1, capacity=1_000_000_000)

    heat_storage = Heat_Storage(name="heat_storage", carrier="h", from_node=h2, to_node=h2, capex=params["heat_storage_capex"], opex = 0, efficiency=params["heat_storage_efficiency"], capacity=1000, soc_start=params["soc_start"])

    resources = [heat_load, gas_boiler_1, gas_import, heat_pump_1, power_import, power_export, power_load, pv_1, heat_storage]
 
    ######## Branches ########
    heat_network = Branch("heat_network", h2, h1, efficiency=params["heat_network_efficiency"])
    power_network = Branch("power_network", p2, p1, efficiency=params["power_network_efficiency"])
    
    branches = [heat_network, power_network]

    ## build connection
    for node in nodes:
        for r in resources:
            if r.to_node == node:
                node.add_incoming(r)
            if r.from_node == node:
                node.add_outgoing(r)
        for b in branches:
            if b.to_node == node:
                node.add_incoming(b)
            if b.from_node == node:
                node.add_outgoing(b)
    
    ######## timesteps ########
    timesteps = list(range(len(params["electricity_load"])))

    ######## MES ########
    mes = MES(name="mes", timesteps=timesteps, params=params)
    
    mes.add_nodes(nodes)
    mes.add_branches(branches)
    mes.add_resources(resources)
    #mes.build_dicts()

    #mes.check_MES()

    return mes


def plot_mes(mes):
    G = nx.DiGraph()
    # das wird total gut, dass überprüft werden kann, dass das modell so aussieht wie man es möchte :D
    raise NotImplementedError("To be implemented soon... i swear ;)")