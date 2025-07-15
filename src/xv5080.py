from src.jv1080 import JV1080Patch
from src.patch import ModulationMatrix, Macro

class XV5080Patch(JV1080Patch):
    def __init__(self, name, data):
        super().__init__(name, data)
        self.modulation_matrix = ModulationMatrix()
        self.macros = {}
    def get_parameter(self, address):
        value = self.data.get(address, 0)
        for mod in self.modulation_matrix.modulations:
            if mod.destination == address:
                source_value = self.get_parameter(mod.source)
                value += source_value * mod.amount
        return value

    def set_parameter(self, address, value):
        if address in self.macros:
            for p in self.macros[address].parameters:
                self.set_parameter(p, value)
        else:
            self.data[address] = value

    def to_sysex(self):
        # Placeholder implementation
        header = [0xF0, 0x41, 0x10, 0x00, 0x00, 0x08, 0x12]
        data = []
        for address, value in self.data.items():
            data.extend(self._address_to_bytes(address))
            data.extend(self._value_to_bytes(value))
        checksum = self._calculate_checksum(data)
        footer = [checksum, 0xF7]
        return header + data + footer

    def _address_to_bytes(self, address):
        return [
            (address >> 21) & 0x7F,
            (address >> 14) & 0x7F,
            (address >> 7) & 0x7F,
            address & 0x7F,
        ]

    def _value_to_bytes(self, value):
        return [value]

    def _calculate_checksum(self, data):
        checksum = 0
        for byte in data:
            checksum += byte
        return 128 - (checksum % 128)
