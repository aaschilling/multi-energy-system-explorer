from pyomo.environ import *
from classes import *


def optimize_system(mes):
    model = ConcreteModel("mes")

    # Sets
    model.T = Set(initialize=mes.timesteps, ordered=True)
    model.O = Set(initialize=[o.name for o in mes.objects])  # all objects
    model.R = Set(initialize=[r.name for r in mes.resources])  # resources
    model.N = Set(initialize=[n.name for n in mes.nodes])  # nodes
    model.B = Set(initialize=[b.name for b in mes.branches])  # branches
    model.S = Set(initialize=[s.name for s in mes.storages])  # branches

    # Mapping-Dicts, langfrisitg in mes Klasse erstellen
    object_dict = {o.name: o for o in mes.objects}
    resource_dict = {r.name: r for r in mes.resources}
    node_incoming = {n.name: [o.name for o in n.incoming] for n in mes.nodes}
    node_outgoing = {n.name: [o.name for o in n.outgoing] for n in mes.nodes}
    opex_dict = {r.name: r.opex for r in mes.resources}
    efficiencies_dict = {o.name: getattr(o, "efficiency", 1) for o in mes.objects}
    capacity_dict = {o.name: getattr(o, "capacity", 1) for o in mes.objects}
    eta_c_dict = {s.name: s.eta_c for s in mes.storages}
    eta_d_dict = {s.name: s.eta_d for s in mes.storages}
    eta_lambda_loss_dict = {s.name: s.lambda_loss for s in mes.storages}
    soc_start_dict = {s.name: s.soc for s in mes.storages}
    max_charge_dict = {s.name: getattr(s, "max_charge", 250) for s in mes.storages}
    max_discharge_dict = {s.name: getattr(s, "max_discharge", 250) for s in mes.storages}
    eta_c_dict = {s.name: getattr(s, "eta_charge", 1.0) for s in mes.storages}
    eta_d_dict = {s.name: getattr(s, "eta_discharge", 1.0) for s in mes.storages}


    #Params
    model.opex = Param(model.R, initialize=opex_dict, domain=Any)
    model.efficiency = Param(model.O, initialize=efficiencies_dict, default=1)
    model.capacity = Param(model.O, initialize=capacity_dict, default=0)
    
    # Parameter Speicher
    model.lambda_loss = Param(model.S, initialize=eta_lambda_loss_dict)  # Speicherverlust pro Zeitschritt als Prozent das noch übrig ist
    model.soc_start = Param(model.S, initialize=soc_start_dict, default=0.0) #anfangszustand speicher, standardmäßig null
    model.max_charge = Param(model.S, initialize=max_charge_dict, default=0) #maximale Ladeleistung pro Stunde
    model.max_discharge = Param(model.S, initialize=max_discharge_dict, default=0) #maximale Entladeleistung pro Stunde
    model.eta_c = Param(model.S, initialize=eta_c_dict, default=1.0) #Ladeeffizienz
    model.eta_d = Param(model.S, initialize=eta_d_dict, default=1.0) #Entladeeffizienz

    # Variablen
    model.inflow  = Var(model.O, model.T, domain=NonNegativeReals) #f.a. Objekte
    model.outflow = Var(model.O, model.T, domain=NonNegativeReals) #f.a. Objekte
    
    #Speichervariablen
    model.soc = Var(model.S, model.T, domain=NonNegativeReals) #Speicherzustand der Speicher
    model.u_charge = Var(model.S, model.T, domain=Binary)    # 1 wenn laden erlaubt/aktiv
    model.u_discharge = Var(model.S, model.T, domain=Binary) # 1 wenn entladen erlaubt/aktiv
    
    # outflow Constraints
    def conversion_rule(m, o, t):
        obj = object_dict[o]
        if hasattr(obj, "soc"):
            return m.outflow[o, t] <= m.max_charge[o]
        else:    
            return m.outflow[o, t] == m.inflow[o, t] * m.efficiency[o]              # verstecktes inflow = outflow für nodes?
    model.conversion = Constraint(model.O, model.T, rule=conversion_rule)

    # Bilanzbedingungen:
    def balance_rule(m, n, t):
        inflow  = sum(m.outflow[o, t]  for o in node_incoming[n])
        outflow = sum(m.inflow[o, t] for o in node_outgoing[n])
        return inflow == outflow
    model.balance = Constraint(model.N, model.T, rule=balance_rule)

    def node_flow_rule(m, n, t):
        return m.inflow[n, t] == sum(m.inflow[o, t]  for o in node_incoming[n]) # durch conversion rule ist inflow = outflow, also muss nur inflow definiert werden
    model.node_inflow_constraint = Constraint(model.N, model.T, rule=node_flow_rule)

    # Demand
    def demand_rule(m, r, t): 
        res = resource_dict[r]
        if type(res) is Prosumer: # noch durch ein demand dicts ersetzen? Dann mit neuem pyomo Param
            return m.inflow[r, t] == res.profile[t]
        return Constraint.Skip
    model.demand_constraint = Constraint(model.R, model.T, rule=demand_rule)
    
    # PV 
    def pv_rule(m, r, t):
        res = resource_dict[r]
        if type(res) is  PV:
            return m.outflow[r, t] == res.profile[t]            #Achtung! Wenn keine Netzeinspeisung führt das zur Unlösbarkeit!, dann hier <=
        return Constraint.Skip
    model.pv_constraint = Constraint(model.R, model.T, rule=pv_rule)
    
    
    # Storage 
    #  Lade/Entladeleistung bei Binär=0 auf 0 beschränken
    def charge_capacity_if_on_rule(m, s, t):
        return m.inflow[s, t] <= m.max_charge[s] * m.u_charge[s, t]
    model.charge_capacity_if_on = Constraint(model.S, model.T, rule=charge_capacity_if_on_rule)

    def discharge_capacity_if_on_rule(m, s, t):
        return m.outflow[s, t] <= m.max_discharge[s] * m.u_discharge[s, t]
    model.discharge_capacity_if_on = Constraint(model.S, model.T, rule=discharge_capacity_if_on_rule)

    # Verhindert gleichzeitiges Laden und Entladen
    def no_simultaneous_charge_discharge_rule(m, s, t):
        return m.u_charge[s, t] + m.u_discharge[s, t] <= 1
    model.no_simultaneous_charge_discharge = Constraint(model.S, model.T, rule=no_simultaneous_charge_discharge_rule)

    # soc berechnen
    def calc_soc_rule(m, s, t):
        if t != m.T.first():
            prev_t = m.T.prev(t)
            return m.soc[s, t] == (m.soc[s, prev_t]*m.lambda_loss[s]) + m.eta_c[s]*m.inflow[s, t] - (1.0/m.eta_d[s])*m.outflow[s, t]
        else:
            return Constraint.Skip
    model.calc_soc_constraint = Constraint(model.S, model.T, rule=calc_soc_rule)
      
    # maximaler SOC
    def soc_bounds_rule(m, s, t):
        return m.soc[s, t] <= m.capacity[s]
    model.soc_bounds = Constraint(model.S, model.T, rule=soc_bounds_rule)    

    def soc_start_end_rule(m, s, t):
        if t == m.T.first():
            return m.soc[s, t] == m.soc_start[s]
        elif t == m.T.last():
            return m.soc[s, t] == m.soc_start[s] # am Ende selber speicherzustand, sonst kommt ja Energie aus dem Nichts :D
        else:
            return Constraint.Skip
    model.soc_start_end_constraint = Constraint(model.S, model.T, rule=soc_start_end_rule)
    
    # Capacity
    def capacity_rule(m, r, t):
        res = resource_dict[r]
        if hasattr(res, "capacity"):
            return m.outflow[r, t] <= m.capacity[r]
        else:
            Constraint.Skip
    model.capacity_constraint = Constraint(model.R, model.T, rule=capacity_rule)
    
    # Zielfunktion
    model.opex_cost = Objective(
        expr = sum(model.inflow[r, t] * model.opex[r] for r in model.R for t in model.T),
        sense = minimize
    )

    # Solver
    solver = SolverFactory("gurobi")
    solver.options["TimeLimit"] = 300
    result = solver.solve(model, tee=True)

    return model, result