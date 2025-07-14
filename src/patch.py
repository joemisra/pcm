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
