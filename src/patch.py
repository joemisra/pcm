class Patch:
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def get_parameter(self, address):
        raise NotImplementedError

    def set_parameter(self, address, value):
        raise NotImplementedError

    def to_sysex(self):
        raise NotImplementedError

    @classmethod
    def from_sysex(cls, sysex_data):
        raise NotImplementedError


class Modulation:
    def __init__(self, source, destination, amount):
        self.source = source
        self.destination = destination
        self.amount = amount


class ModulationMatrix:
    def __init__(self):
        self.modulations = []

    def add_modulation(self, modulation):
        self.modulations.append(modulation)

    def get_modulation(self, index):
        return self.modulations[index]

    def set_modulation(self, index, modulation):
        self.modulations[index] = modulation


class Macro:
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters
