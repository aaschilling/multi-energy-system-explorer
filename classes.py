
######## Main Classes ########
class Node:
    """
    Network buses, junctions, and manifolds
    """

    def __init__(self, name, carrier):
        self.name:str = name                             #identifier
        self.carrier:str = carrier                       #identifier
        self.incoming:list = []                          #allocation, incoming branches
        self.outgoing:list = []                          #allocation, outgoing branches

    def add_incoming(self, branch):
        if branch not in self.incoming:             
            self.incoming.append(branch)

    def add_outgoing(self, branch):
        if branch not in self.outgoing:             
            self.outgoing.append(branch)
    

class Branch:
    """
    Network lines and pipes, Intra-carrier power conversion units
    """

    def __init__(self, name, from_node, to_node, efficiency=1.0, price=0):
        self.name:str = name                      #identifier
        self.from_node:str = from_node            #allocation
        self.to_node:str = to_node                #allocation
        self.efficiency:int = efficiency          #operation param
        self.upper_limit:int = []                 #operation param
        self.lower_limit:int = []                 #operation param
        self.incoming:list = []
        self.outcoming:list = []
        self.price:int = price                    #operation
        

class Resource:
    """
    Abstract Class: Inter-carrier power conversion units, Energy storage units, Prosumers
    """
    def __init__(self, name, carrier, from_node, to_node, capex, opex, efficiency, capacity):
        self.name:str = name                            #identifier
        self.carrier:str = carrier                      #identifier
        self.from_node:str = from_node                  #allocation
        self.to_node:str = to_node                      #allocation.
        self.capex:int = capex
        self.opex:int = opex
        self.efficiency:int = efficiency
        self.capacity:int = capacity 


######## Children Classes ########
class Prosumer(Resource):
    """
    Child of Resource: Prosumer like Demands, PV-Unit, etc
    """
    def __init__(self, name, carrier, from_node, to_node, capex, opex, efficiency, capacity, profile):
        super().__init__(name, carrier, from_node, to_node, capex, opex, efficiency, capacity)
        self.profile = profile

class PV(Prosumer):
    def __init__(self, name, carrier, from_node, to_node, capex, opex, efficiency, capacity, profile):
        super().__init__(name, carrier, from_node, to_node, capex, opex, efficiency, capacity, profile)
        self.profile = {timestep: norm_power * capacity for timestep, norm_power in profile.items()}


class Grid_Import(Resource):
    def __init__(self, name, carrier, from_node, to_node, capex, opex, efficiency, capacity,):
        super().__init__(name, carrier, from_node, to_node, capex, opex, efficiency, capacity,)
        self.importer = True

#conversion
class Inter_Carrier_Conversion(Resource):
    def __init__(self, name, carrier, from_node, to_node, capex, opex, efficiency, capacity):
        super().__init__(name, carrier, from_node, to_node, capex, opex, efficiency, capacity)

class SISO(Inter_Carrier_Conversion):
    def __init__(self, name, carrier, from_node, to_node, capex, opex, efficiency, capacity):
        super().__init__(name, carrier, from_node, to_node, capex, opex, efficiency, capacity)


class SIDO(Inter_Carrier_Conversion):
    def __init__(self, name, carrier, from_node, to_node, capex, opex, efficiency, capacity):
        super().__init__(name, carrier, from_node, to_node, capex, opex, efficiency, capacity)

#real technologies
class Heat_Pump(SISO):
    def __init__(self, name, carrier, from_node, to_node, capex, opex, efficiency, capacity):
        super().__init__(name, carrier, from_node, to_node, capex, opex, efficiency, capacity)

class P2H(SISO):
    def __init__(self, name, carrier, from_node, to_node, capex, opex, efficiency, capacity):
        super().__init__(name, carrier, from_node, to_node, capex, opex, efficiency, capacity)

class Gas_Boiler(SISO):
    def __init__(self, name, carrier, from_node, to_node, capex, opex, efficiency, capacity):
        super().__init__(name, carrier, from_node, to_node, capex, opex, efficiency, capacity)


# storage
class Storage(Resource):
    def __init__(self, name, carrier, from_node, to_node, capex, opex, efficiency, capacity):
        super().__init__(name, carrier, from_node, to_node, capex, opex, efficiency, capacity)
        

class SICA_Storage(Storage):
    def __init__(self, name, carrier, from_node, to_node, capex, opex, efficiency, capacity):
        super().__init__(name, carrier, from_node, to_node, capex, opex, efficiency, capacity)

class DUCA_Storage(Storage):
    def __init__(self, name, carrier, from_node, to_node, capex, opex, efficiency, capacity):
        super().__init__(name, carrier, from_node, to_node, capex, opex, efficiency, capacity)

class Heat_Storage(SICA_Storage):
    def __init__(self, name, carrier, from_node, to_node, capex, opex, efficiency, capacity, soc_start=1):
        super().__init__(name, carrier, from_node, to_node, capex, opex, efficiency, capacity)
        self.soc = soc_start * capacity
        self.eta_c = 0.99
        self.eta_d = 0.99
        self.lambda_loss = efficiency

class MES:
    """
    the MES as one object for optimizing
    """
    def __init__(self, name, timesteps, params):
        self.name:str = name
        self.params:dict = params
        self.timesteps:list = timesteps
        self.nodes:list = []
        self.branches:list = []
        self.resources:list = []
        self.objects:list = []
        self.storages:list = []
        self.dicts:dict = {}
        
    
    def add_nodes(self, nodes:list):
        if type(nodes) is not list: 
            raise TypeError("expects list")
        else:
            for n in nodes:
                self.nodes.append(n)
                self.objects.append(n)

    def add_branches(self, branches:list):
        if type(branches) is not list: 
            raise TypeError("expects list")
        else:
            for b in branches:
                self.branches.append(b)
                self.objects.append(b)

    def add_resources(self, resources:list):
        if type(resources) is not list: 
            raise TypeError("expects list")
        else:
            for r in resources:
                self.resources.append(r)
                self.objects.append(r)
                if isinstance(r, Storage):
                    self.storages.append(r)

    def build_dicts(self):
    # dicts for optimization
        dicts = {}
        self.dicts = dicts 
        raise NotImplementedError("To be implemented soon... i swear ;)")

    def check_MES(self):
        raise NotImplementedError("To be implemented soon... i swear ;)")
    

    
