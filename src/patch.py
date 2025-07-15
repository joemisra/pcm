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
        if source == destination:
            raise ValueError("Source and destination cannot be the same")
        self.source = source
        self.destination = destination
        self.amount = amount


class ModulationMatrix:
    def __init__(self):
        self.modulations = []

    def add_modulation(self, modulation):
        self.modulations.append(modulation)

    def remove_modulation(self, index):
        del self.modulations[index]

    def get_modulation(self, index):
        return self.modulations[index]

    def set_modulation(self, index, modulation):
        self.modulations[index] = modulation


class Macro:
    def __init__(self, name, parameters, min_value=0, max_value=127):
        self.name = name
        self.parameters = parameters
        self.min_value = min_value
        self.max_value = max_value
